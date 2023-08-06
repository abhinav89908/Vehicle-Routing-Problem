# from ortools.constraint_solver import routing_enums_pb2
# from ortools.constraint_solver import pywrapcp
# import math
# from flask import Flask, jsonify, request
# app = Flask(__name__)

# @app.route('/')
# def hello_word():
#     return "Hello world!"

# # data = {}


# def print_solution(data, manager, routing, solution):
#     """Prints solution on console."""
#     print(f'Objective: {solution.ObjectiveValue()}')

#     plan_output_set = []

#     max_route_distance = 0
#     for vehicle_id in range(data['num_vehicles']):
#         index = routing.Start(vehicle_id)
#         plan_output = ""
#         route_distance = 0
#         while not routing.IsEnd(index):
#             plan_output += ' {} -> '.format(manager.IndexToNode(index))
#             previous_index = index
#             index = solution.Value(routing.NextVar(index))
#             route_distance += routing.GetArcCostForVehicle(
#                 previous_index, index, vehicle_id)
#         plan_output += '{}'.format(manager.IndexToNode(index))
#         plan_output_set.append(plan_output)
#         # plan_output += 'Distance of the route: {}m\n'.format(route_distance)
#         print(plan_output)
#         max_route_distance = max(route_distance, max_route_distance)

#     return jsonify({
#         "plan output": plan_output_set,
#         "total distance": max_route_distance
#     })
#     # print('Maximum of the route distances: {}m'.format(max_route_distance))


#     # return 'Maximum of the route distances: ' + str(max_route_distance)



# def solve(data):
#     """Entry point of the program."""
#     print(type(data))
#     print(data)
#     # Create the routing index manager.
#     manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
#                                            data['num_vehicles'], data['depot'])
#     # # Create Routing Model.
#     routing = pywrapcp.RoutingModel(manager)

#     # Create and register a transit callback.
#     def distance_callback(from_index, to_index):
#         """Returns the distance between the two nodes."""
#         # Convert from routing variable Index to distance matrix NodeIndex.
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         return data['distance_matrix'][from_node][to_node]

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)

#     # Define cost of each arc.
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     # Add Distance constraint.
#     dimension_name = 'Distance'
#     routing.AddDimension(
#         transit_callback_index,
#         0,  # no slack
#         3000,  # vehicle maximum travel distance
#         True,  # start cumul to zero
#         dimension_name)
#     distance_dimension = routing.GetDimensionOrDie(dimension_name)
#     distance_dimension.SetGlobalSpanCostCoefficient(100)

#     # Setting first solution heuristic.
#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.first_solution_strategy = (
#         routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

#     # Solve the problem.
#     solution = routing.SolveWithParameters(search_parameters)

#     # Print solution on console.
#     if solution:
#         return print_solution(data, manager, routing, solution)
#     else:
#         print('No solution found !')

#     return data



# @app.route('/process', methods=['GET'])
# def process_data():
#     # Accessing the query parameters from the URL
#     query_params = request.args

#     # Convert the ImmutableMultiDict to a regular Python dictionary
#     data_dict = dict(query_params)


#     # Your processing logic using the received dictionary
#     # ...


#     dist_string = data_dict['distance_matrix'].split(' ')
#     n = int(math.sqrt(len(dist_string)))

#     dist_mat = [[] for _ in range(n)]
#     k=0
#     p=0
#     for i in dist_string:
#         dist_mat[k].append(int(i))
#         if(p==n-1):
#             p=0
#             k=k+1
#         else:
#             p=p+1

#     data = {}
#     data['distance_matrix'] = dist_mat
#     data['num_vehicles'] = int(data_dict['num_vehicles'])
#     data['depot'] = int(data_dict['depot'])

#     res = solve(data)
#     return res


#     return jsonify("Vehicle routing problem is done.")
#     return jsonify({"status": "success", "message": "Data processed successfully"})




# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")



from numpy import double
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
from flask import Flask, jsonify, request
# from flask_cors import CORS  # Import the CORS module
app = Flask(__name__)
# CORS(app)

@app.route('/')
def hello_word():
    return "Hello world!"


# data = {}


def get_vrp_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')

    plan_output_set = []

    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = ""
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}'.format(manager.IndexToNode(index))
        plan_output_set.append(plan_output)
        # plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)

    return jsonify({
        "plan output": plan_output_set,
        "total distance": max_route_distance
    })
    # print('Maximum of the route distances: {}m'.format(max_route_distance))

    # return 'Maximum of the route distances: ' + str(max_route_distance)


def solve(data):
    """Entry point of the program."""
    print(type(data))
    print(data)
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    # # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        return get_vrp_solution(data, manager, routing, solution)
    else:
        print('No solution found !')

    return data


@app.route('/vrp', methods=['GET'])
def process_data():
    query_params = request.args
    data_dict = dict(query_params)
    dist_string = data_dict['distance'].split(' ')
    n = int(math.sqrt(len(dist_string)))
    dist = []
    temp = []
    for i in dist_string:
        temp.append(double(i))
        if len(temp) == 2:
            dist.append(temp)
            temp = []

    loc = len(dist)
    dist_mat = [[] for _ in range(loc)]
    for i in range(loc):
        for j in range(loc):
            d = abs(dist[i][0] - dist[j][0]) + abs(dist[i][1] - dist[j][1])
            dist_mat[i].append(int(round(d, 0)))

    # return jsonify(dist_mat)

    data = {}
    data['distance_matrix'] = dist_mat
    data['num_vehicles'] = int(data_dict['num_vehicles'])
    data['depot'] = int(data_dict['depot'])
    res = solve(data)
    return res


if __name__ == "__main__":
    app.run(debug=True)
