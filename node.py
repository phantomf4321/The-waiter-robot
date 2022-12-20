from successor import State


def zero_heuristic(state: State) -> int:
    return 0


class Node:
    parent: "Node"
    children: list["Node"]

    act: tuple
    depth: int
    cost: int

    heuristic = zero_heuristic

    def __init__(
        self, state: State, act=None, depth=0, parent=None, cost=0, children=[]
    ):
        self.state = state
        self.parent = parent
        self.children = children

        self.act = act  # Action performed on parent
        self.depth = depth  # Depth of this node
        self.cost = cost  # Cost from root to here
        self.confirm_expand = False  # Expanded?

    def expand(self, actions: list[tuple[State, tuple, int]]) -> list["Node"]:
        children = []
        for act in actions:
            cost = self.cost + act[2]
            depth = self.depth + 1
            parent = self
            node = Node(act[0], act[1], depth, parent, cost)  # it's new node...
            children.append(node)

        self.confirm_expand = True
        self.children.extend(children)
        return children

    def equality(self, other: "Node") -> bool:
        return other.state == self.state

    # get the identity:
    def correspondence(self):
        return self.state

    def get_cost(self):
        return self.cost + Node.heuristic(self.state)

    # compare our objects based on attribute balance a > b
    def __gt__(self, other: "Node") -> bool:
        if not isinstance(other, Node):
            raise TypeError(
                "Error while comparing object with type",
                type(other),
                "and a Node object",
            )
        return self.get_cost() > other.get_cost()

    # compare our objects based on attribute balance a >= b
    def __ge__(self, other: "Node") -> bool:
        if not isinstance(other, Node):
            raise TypeError(
                "Error while comparing object with type",
                type(other),
                "and a Node object",
            )
        return self.get_cost() >= other.get_cost()

    # compare our objects based on attribute balance a < b
    def __lt__(self, other: "Node") -> bool:
        if not isinstance(other, Node):
            raise TypeError(
                "Error while comparing object with type",
                type(other),
                "and a Node object",
            )
        return self.get_cost() < other.get_cost()

    # compare our objects based on attribute balance a <= b
    def __le__(self, other: "Node") -> bool:
        if not isinstance(other, Node):
            raise TypeError(
                "Error while comparing object with type",
                type(other),
                "and a Node object",
            )
        return self.get_cost() <= other.get_cost()

    # return the object representation in string format:
    def __repr__(self):
        return self.__str__()

    # represent the class objects:
    def __str__(self):
        return "State: " + str(self.state) + " | Cost: " + str(self.get_cost())
