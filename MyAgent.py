import random

class Agent:
    def chooseAction(self, observations, possibleActions):
        lidar = observations['lidar']
        velocity = observations['velocity']

        left = lidar[0]
        front_left = lidar[1]
        front = lidar[2]
        front_right = lidar[3]
        right = lidar[4]

        front_limit= 0.9
        side_limit = 0.9
        corner_limit = 0.9
        low_vel = 0.05
        normal_speed = 0.4

        if lidar.count(float('inf')) == len(lidar):
            return ('straight', 'accelerate')

        if velocity < low_vel:
            return ('straight', 'accelerate')

        if left < side_limit:
            return ('right', 'brake')

        if right < side_limit:
            return ('left', 'brake')

        if front < front_limit:
            if left > right:
                return ('left', 'brake')
            else:
                return ('right', 'brake')

        if front_left < corner_limit:
            return ('right', 'brake')

        if front_right < corner_limit:
            return ('left', 'brake')

        if left < side_limit:
            return ('right', 'coast')

        if right < side_limit:
            return ('left', 'coast')

        if front < front_limit:
            if front_left < front_right:
                return ('right', 'accelerate')
            else:
                return ('left', 'accelerate')

        if velocity < normal_speed:
            return ('straight', 'accelerate')

        return ('straight', 'coast')
