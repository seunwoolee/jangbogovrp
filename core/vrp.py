from __future__ import print_function

from datetime import date
from typing import Dict, Union, List, Tuple

from django.db.models import Q, Sum
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from company.models import Company
from customer.models import Order, MutualDistance, Customer
from delivery.models import RouteM, RouteD

Customers = List[Tuple]


class VRP:
    def __init__(self, code: str, delivery_date: date):
        self.code = code
        self.delivery_date = delivery_date
        self.customers: list = []

    def create_data_model(self):
        """Stores the data for the problem."""
        data = {}
        customers: Customers = list(Order.objects.values_list('customer').filter(
            Q(date=self.delivery_date), Q(company__code=self.code), Q(is_am=True)).annotate(group_price=Sum('price')))

        customers_ids: list = []
        customers_prices: list = []

        for customer in customers:
            customers_ids.append(customer[0])
            customers_prices.append(customer[1])

        starting_position: Customer = Customer.objects.filter(customer_id='admin').first()  # TODO 하드코딩
        customers_ids.insert(0, starting_position.id)
        customers_prices.insert(0, 0)
        each_price = round(sum(customers_prices) * 1.2 / 4)
        from_to_arrs: list = []

        for start in customers_ids:
            from_to_arr: list = []
            for end in customers_ids:
                if start == end:
                    from_to_arr.append(0)
                    continue

                distance: int = MutualDistance.objects.filter(Q(start__id=start), Q(end__id=end)).first().distance
                from_to_arr.append(distance)
            from_to_arrs.append(from_to_arr)

        data['distance_matrix'] = from_to_arrs
        data['demands'] = customers_prices
        data['vehicle_capacities'] = [each_price, each_price, each_price, each_price]
        data['num_vehicles'] = 4
        data['depot'] = 0

        self.customers = customers_ids
        return data

    def create_routes(self, data, manager, routing, solution) -> List[List]:
        """Prints solution on console."""
        result: list = []
        max_route_distance = 0
        for vehicle_id in range(data['num_vehicles']):
            route: list = []
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            while not routing.IsEnd(index):
                route.append(manager.IndexToNode(index))
                plan_output += ' {} -> '.format(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)

            route.append(0) # 마지막 목적지 insert
            result.append(route)

            plan_output += '{}\n'.format(manager.IndexToNode(index))
            plan_output += 'Distance of the route: {}m\n'.format(route_distance)
            print(plan_output)
            max_route_distance = max(route_distance, max_route_distance)
        print('Maximum of the route distances: {}m'.format(max_route_distance))
        print(result)
        return result

    def vrp(self, data: dict):
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                               data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        if not solution:
            raise Exception('not found solution')

        return self.create_routes(data, manager, routing, solution)

    def save_route(self, routes: List[List]):
        route_m = RouteM.objects.create(
            company=Company.objects.get(code=self.code),
            date=self.delivery_date,
            is_am=True, # TODO 하드코딩
            count_car=4, # TODO 하드코딩
            price=100000, # TODO 하드코딩
            count_location=len(self.customers)
        )
        route_m.save()

        for route_number, route in enumerate(routes):
            for index in route:
                customer = Customer.objects.get(id=self.customers[index])
                RouteD.objects.create(
                    route_m=route_m,
                    customer=customer,
                    route_number=route_number+1,
                    route_index=index+1,
                )
