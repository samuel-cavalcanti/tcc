from typing import Optional
from .graph import Graph
from .node import Node
from .min_heap import MinHeap
from .a_star_parameters import AStarParameters


class AStarSearch:

    __open_set: MinHeap
    __graph: Graph
    __came_from: dict[Node, Node]
    __visited_set: dict[Node, bool]
    __distances: dict[Node, float]
    __parameters: AStarParameters

    def __init__(self, graph: Graph, params: AStarParameters) -> None:
        self.__visited_set = dict()
        self.__distances = dict()
        self.__came_from = dict()
        self.__open_set = MinHeap()
        self.__graph = graph
        self.__parameters = params

    def run(self, initial_node: Node, desired_node: Node) -> list[Node]:

        self.__distances[initial_node] = 0.0

        self.__open_set.push(initial_node, distance=self.__distances[initial_node])

        while self.__open_set.is_not_empty():
            path = self.__one_it(desired_node)
            if path is not None:
                return path
        
        return []

    def __one_it(self, desired_node: Node) -> Optional[list[Node]]:
        current_node = self._visit_next_node()

        if current_node is None:
            return None

        if current_node == desired_node:
            return self.__reconstruct_path(current_node)

        for neighbor in self.__graph.get_neighbors(current_node):
            self.__relaxing_node(origin_node=current_node, target_node=neighbor)

    def __relaxing_node(self, origin_node: Node, target_node: Node):
        if self.__visited(target_node):
            return

        self.__update_distance(origin_node, target_node)

        self.__open_set.push(target_node, distance=self.__get_distance(target_node))

    def _visit_next_node(self) -> Optional[Node]:
        next_node = self.__open_set.pop()
        if next_node is None:
            return None

        while self.__visited(next_node):
            next_node = self.__open_set.pop()
            if next_node is None:
                return None

        self.__visited_set[next_node] = True

        return next_node

    def __visited(self, node: Node) -> bool:
        return self.__visited_set.get(node, False) == True

    def __reconstruct_path(self, current_node: Node) -> list[Node]:

        path = [current_node]
        while current_node in self.__came_from.keys():
            current_node = self.__came_from[current_node]
            path.insert(0, current_node)

        return path

    def __update_distance(self, origin_node: Node, target_node: Node):

        cost = self.__parameters.get_real_cost(origin=origin_node, target=target_node)

        heuristic_cost = self.__parameters.get_heuristic_cost(origin=origin_node, target=target_node)

        origin_distance = self.__distances[origin_node]

        current_distance = self.__get_distance(target_node)

        new_distance = origin_distance + cost + heuristic_cost

        if new_distance < current_distance:
            self.__distances[target_node] = new_distance
            self.__came_from[target_node] = origin_node

    def __get_distance(self, node: Node) -> float:
        return self.__distances.get(node, float('inf'))
