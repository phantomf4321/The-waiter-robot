from battlefield import Battlefield
from read import Read
from defaults import Defaults
from monitor import Display
from successor import State
from node import Node
from min_heap import MinHeap
import time


class GameManager:

    battlefield: Battlefield
    init_state: State
    display: Display

    def __init__(self):
        self.battlefield, self.init_state = self.parse_map()
        # After parsing map it's time to start pygame
        self.display = Display(self.battlefield)

    def start_search(self, search_type: str) -> tuple[list[State], int, int]:
        """Chooses a search between all and returns its result list.
        :param search_type Search algorithm type
        :returns The result of search"""

        result = self.__getattribute__(search_type + "_search")()

        result_list = GameManager.extract_path_list(result)
        # result_list.pop()
        result_list.reverse()
        return result_list, result.depth, result.get_cost

    def display_states(self, states_list: list[State]) -> None:
        if len(states_list) <= 0:
            print("There is no way")
            return
        self.display.update(self.init_state)  # display
        self.display.begin_display()
        for state in states_list:
            time.sleep(Defaults.STEP_TIME)
            self.display.update(state)
            
            
            
    def ids_search(self) -> Node:
        def dls_search(limit: int, depth: int, node: Node) -> Node:
            if time.time() - cur_time > 60.0:
                raise Exception('Time limit. Mission failed!')
            res = None
            if depth < limit and node.state not in visited_states:
                actions = State.successor(node.state, self.battlefield)
                visited_states[node.state] = True
                for child in node.expand(actions)[::-1]:
                    if State.is_goal(child.state, self.battlefield.points):
                        return child
                    r = dls_search(limit, depth + 1, child)
                    if r is not None:
                        res = r
                        break
                    if child.state in visited_states:
                        del visited_states[child.state]
            return res
        for i in range(Defaults.FIRST_K, Defaults.LAST_K):
            print('Starting depth: ', i)
            cur_time = time.time()
            root_node = Node(self.init_state)
            visited_states = {}
            result = dls_search(i, 0, root_node)
            if result is not None:
                return result
            

    def a_star_search(self) -> Node:
        def manhattan_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
            d1 = point1[0] - point2[0]
            d2 = point1[1] - point2[1]
            if d1 < 0:
                d1 = d1*(-1)
            if d2 < 0:
                d2 = d2*(-1)
         
            manhattan_distance = d1 + d2
            return manhattan_distance

        def heuristic(state: State) -> int:
            total_distance = 0
            for butter in state.butters:
                min_distance = float("inf")
                for point in self.battlefield.points:
                    curr_distance = manhattan_distance(point, butter)
                    if curr_distance < min_distance:
                        min_distance = curr_distance
                total_distance += min_distance

            return total_distance
        # Setting all nodes heuristic functions
        Node.heuristic = heuristic
        # Beginning of a star search
        heap = MinHeap()  
        visited = set()
        root_node = Node(self.init_state)
        heap.add(root_node)
        while not heap.is_empty():
            node = heap.pop()
            # Checking goal state
            if State.is_goal(node.state, self.battlefield.points):
                return node
            if node.state not in visited:
                visited.add(node.state)
            else:
                continue
            # A* search
            actions = State.successor(node.state, self.battlefield)
            for child in node.expand(actions):
                heap.add(child)

    def ucs_search(self) -> Node:
        heap = MinHeap()
        visited = set()
        source_node = Node(self.init_state)
        heap.add(source_node)
        while not heap.is_empty():
            node = heap.pop()

            if State.is_goal(node.state, self.battlefield.points):
                return node

            if node.state not in visited:
                visited.add(node.state)
            else:
                continue

            actions = State.successor(node.state, self.battlefield)
            for child in node.expand(actions):
                heap.add(child)

    def bfs_search(self) -> Node:

        frontier = [Node(self.init_state)]
        visited = {}

        while len(frontier) > 0:  # Starting BFS loop
            node_1 = frontier.pop(0)
            visited[node_1.state] = node_1

            if State.is_goal(node_1.state, self.battlefield.points):
                return node_1

            actions = State.successor(
                node_1.state, self.battlefield
            )  # Add successors to frontier
            for child in node_1.expand(actions):
                if child.state not in visited:
                    frontier.append(child)

    def dfs_search(self) -> Node:
        frontier = [Node(self.init_state)]
        visited = {}

        while len(frontier) > 0:  # Starting DFS loop
            node_1 = frontier.pop()
            visited[node_1.state] = node_1
            
            # In case of equality, the work of the function is finished and node is returned.
            if State.is_goal(node_1.state, self.battlefield.points):
                return node_1
            
            #Actions are equal to the output of the successor function. As a result, all future statuses are placed in actions.
            actions = State.successor(
                node_1.state, self.battlefield
            )  # Add successors to frontier
            
            # these actions are converted into acceptable nodes for the children of node_1 by the expand function.
            for child in node_1.expand(actions): 
                # Avoid duplicate statuses
                if child.state not in visited:
                    frontier.append(child)

    @staticmethod
    def parse_map() -> tuple[Battlefield, State]:
        """Uses map file to create map object in game.
        :returns The map object and the init state"""

        map_array = Read.read_line_by_line(Defaults.MAP_FILE)
        sizes = map_array.pop(0)
        h, w = int(sizes[0]), int(sizes[1])
        map_object = Battlefield(h, w)

        butters = []  # Variables to read from map
        points = []
        robot = (0, 0)
        for j, row in enumerate(map_array):
            for i, col in enumerate(row):

                if len(col) > 1:  # If there is an object in map
                    if col[1] == "b":
                        butters.append((j, i))
                    elif col[1] == "p":
                        points.append((j, i))
                    elif col[1] == "r":
                        robot = (j, i)
                    row[i] = col[0]

            map_object.append_row(row)  # Append row to map

        map_object.set_points(points)
        return map_object, State(robot, butters)

    @staticmethod
    def extract_path_list(node: Node) -> list[State]:
        result_list = []
        watchdog = 0
        while node is not None:
            watchdog += 1
            if watchdog > 1000:
                raise Exception("LIMITED!")
            result_list.append(node.state)
            node = node.parent

        return result_list

    @staticmethod
    def state_in_list_of_nodes(state: State, nodes_list: list[Node]) -> bool:
        for node in nodes_list:
            if node.state == state:
                return True
        return False
