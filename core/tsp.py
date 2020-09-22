from __future__ import print_function
from typing import List, Tuple
from datetime import date

from django.db.models import Q, Sum
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from customer.models import Order, MutualDistance, Customer

Customers = List[Tuple]


def create_data_model(code: str, delivery_date: date):
    """Stores the data for the problem."""
    data = {}
    customers: Customers = list(Order.objects.values_list('customer').filter(
        Q(date=delivery_date), Q(company__code=code), Q(is_am=True)).annotate(test=Sum('price')))

    customers_ids: list = []
    customers_prices: list = []

    for customer in customers:
        customers_ids.append(customer[0])
        customers_prices.append(customer[1])

    starting_position: Customer = Customer.objects.filter(customer_id='admin').first()  # TODO 하드코딩
    customers_ids.insert(0, starting_position.id)
    customers_prices.insert(0, 0)
    each_price = round(sum(customers_prices) / 4)
    temp: list = []
    for start in customers_ids:
        from_to_arr: list = []
        for end in customers_ids:
            if start == end:
                from_to_arr.append(0)
                continue

            distance: int = MutualDistance.objects.filter(Q(start__id=start), Q(end__id=end)).first().distance
            from_to_arr.append(distance)
        temp.append(from_to_arr)


    data['distance_matrix'] = temp
    data['demands'] = customers_prices
    data['vehicle_capacities'] = [each_price+10000, each_price+10000, each_price+10000, each_price+10000]
    data['num_vehicles'] = 4
    data['depot'] = 0

    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))


def tsp(data: dict):
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


    # Add Capacity constraint.
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

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
