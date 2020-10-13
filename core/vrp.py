from __future__ import print_function
import math
from geopy.distance import geodesic

from typing import Dict, Union, List, Tuple

from django.db.models import Q, Sum
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from company.models import Company
from customer.models import Order, MutualDistance, Customer
from delivery.models import RouteM, RouteD

Customers = List[Tuple]


class VRP:
    def __init__(self, code: str, delivery_date: str, is_am: str, car_count: int):
        self.code = code
        self.delivery_date = delivery_date
        self.car_count = car_count
        self.customers: list = []
        self.is_am = is_am

    def calculate_distance(self, x1, y1, x2, y2) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def create_data_model(self):
        data = {}
        customers: Customers = list(Order.objects.values_list('customer').filter(
            Q(date=self.delivery_date), Q(company__code=self.code), Q(is_am=self.is_am))
                                    .annotate(group_price=Sum('price')))

        customers_ids: list = []
        customers_prices: list = []

        for customer in customers:
            customers_ids.append(customer[0])
            customers_prices.append(customer[1])

        starting_position: Customer = Customer.objects.filter(customer_id='admin').first()  # TODO 하드코딩
        customers_ids.insert(0, starting_position.id)
        customers_prices.insert(0, 0)
        total_price = sum(customers_prices) * 1.1
        each_price = round(total_price / self.car_count)
        from_to_arrs: list = []

        for start in customers_ids:
            from_to_arr: list = []
            for end in customers_ids:
                if start == end:
                    from_to_arr.append(0)
                    continue

                start_customer: Customer = Customer.objects.get(id=start)
                end_customer: Customer = Customer.objects.get(id=end)
                distance: int = round(geodesic((start_customer.latitude, start_customer.longitude),
                                           (end_customer.latitude, end_customer.longitude)).meters)
                # distance: float = self.calculate_distance(
                #     start_customer.latitude, start_customer.longitude, end_customer.latitude, end_customer.longitude)
                # distance: int = MutualDistance.objects.filter(Q(start__id=start), Q(end__id=end)).first().distance
                from_to_arr.append(distance)
            from_to_arrs.append(from_to_arr)

        data['distance_matrix'] = from_to_arrs
        data['demands'] = customers_prices
        data['vehicle_capacities'] = [each_price] * self.car_count
        data['num_vehicles'] = self.car_count
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
                plan_output += ' {} -> '.format(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                distance = routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
                route_distance += distance
                route.append({'index': manager.IndexToNode(index), 'distance': distance})

            # route.append({'index': 0, 'distance': 0})  # 마지막 목적지 insert
            result.append(route)

            plan_output += '{}\n'.format(manager.IndexToNode(index))
            plan_output += 'Distance of the route: {}m\n'.format(route_distance)
            print(plan_output)
            max_route_distance = max(route_distance, max_route_distance)
        print('Maximum of the route distances: {}m'.format(max_route_distance))
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

    def save_route(self, routes: List[List]) -> int:
        starting_position: Customer = Customer.objects.filter(customer_id='admin').first()  # TODO 하드코딩

        route_m = RouteM.objects.create(
            company=Company.objects.get(code=self.code),
            date=self.delivery_date,
            is_am=self.is_am,
            count_car=self.car_count,
            price=100000,  # TODO 하드코딩
            count_location=len(self.customers)
        )
        route_m.save()

        for route_number, route in enumerate(routes):

            for route_index, _route in enumerate(route):
                customer = Customer.objects.get(id=self.customers[_route['index']])

                if customer == starting_position:
                    continue

                orders = Order.objects.filter(Q(date=self.delivery_date), Q(company__code=self.code),
                                              Q(is_am=self.is_am), Q(customer=customer))
                route_d = RouteD.objects.create(
                    distance=_route['distance'],
                    route_m=route_m,
                    customer=customer,
                    route_number=route_number + 1,
                    route_index=route_index + 1,
                )
                for order in orders:
                    order.route = route_d
                    order.save()

                route_d.save()

        return route_m.id
