from battlefield import Battlefield

class State:
    # Constructor function:
    def __init__(self, robot: tuple, butters=[]):
        self.robot = robot
        self.butters = butters

    # Checking the equality of class elements:
    def __eq__(self, other):
        return self.butters == other.butters and self.robot == other.robot

    # represent the class objects:
    def __str__(self):
        return (
            '"The robot is located on: '
            + str(self.robot)
            + " The Butters is located on at: "
            + str(self.butters)
            + '"'
        )

    # return the object representation in string format:
    def __repr__(self):
        return self.__str__()

    # values are used to compare the dictionary keys while doing a dictionary lookup:
    def __hash__(self):
        h = hash(self.robot)
        for i in self.butters:
            h += hash(i)
        return h

    @staticmethod
    def successor(
        state: "State", battlefield_object: Battlefield
    ) -> list[tuple["State", tuple, int]]:
        matrix = battlefield_object.battlefield
        points = battlefield_object.points
        width = battlefield_object.width
        height = battlefield_object.height
        nexts = []
        robot_y = state.robot[0]
        robot_x = state.robot[1]

        def move_robot(y: int, x: int):
            """
            The duties of this function are:
              1)Move the robot.
              2)Push the butter using the robot.
              3)Save new states in "nexts".
            """

            # Diagonal movement is not allowed
            if x * y != 0:
                raise Exception("Unfortunately, you cannot move diagonally:(")
            """
            Authorized transfers:
            (1, 0) Down
            (-1,0) Up
            (0, 1) Right
            (0,-1) Left
            y*x = 0
            Unauthorized transfers:
            ( 1, 1)
            (-1, 1)
            ( 1,-1)
            (-1,-1)
            y*x != 0
            """

            # The element is not allowed to leave the battlefield.
            if battlefield_object.check_out(robot_y + y, robot_x + x):
                return

            # Do not enter the barrier:
            if battlefield_object.is_barrier(robot_y + y, robot_x + x):
                return

            # Checking the presence or absence of butters around the robot
            if (
                robot_y + y,
                robot_x + x,
            ) not in state.butters:  # No butters were found around the robot
                nexts.append(
                    (  # Save new action in "nexts"
                        State(
                            (robot_y + y, robot_x + x), state.butters.copy()
                        ),  # Save new states. The butters remain in their previous position.
                        (
                            y,
                            x,
                        ),  # The initial state of the state is placed in index number 1
                        max(
                            int(matrix[robot_y + y][robot_x + x]),
                            int(matrix[robot_y][robot_x]),
                        ),  # max cost...
                    )
                )
            else:  # butters were found around the robot
                # The robot cannot throw the butters out of the battlefield
                if (
                    (y == -1 and robot_y != 1)
                    or (y == 1 and robot_y != height - 2)
                    or (x == -1 and robot_x != 1)
                    or (x == 1 and robot_x != width - 2)
                ):

                    # If butter is on a point
                    if (robot_y + y, robot_x + x) in points:
                        return

                    # Do not enter the barrier, In addition, the butter cannot pass over an other butter.
                    y2 = robot_y + 2 * y
                    x2 = robot_x + 2 * x
                    if battlefield_object.is_barrier(y2, x2) or (
                        (y2, x2) in state.butters
                    ):
                        return

                    # Moving butter
                    new_butters = state.butters.copy()
                    new_butters.remove((robot_y + y, robot_x + x))
                    new_butters.append((y2, x2))
                    nexts.append(
                        (
                            State((robot_y + y, robot_x + x), new_butters),
                            (y, x),
                            max(
                                int(matrix[robot_y + y][robot_x + x]),
                                int(matrix[robot_y][robot_x]),
                            ),
                        )
                    )

        move_robot(1, 0)
        move_robot(0, 1)
        move_robot(-1, 0)
        move_robot(0, -1)

        return nexts

    @staticmethod
    def is_goal(state: "State", points: list[tuple]):
        for butter in state.butters:
            if butter not in points:
                return False
        return True
