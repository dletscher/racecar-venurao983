import random
from math import pi, sqrt

class Agent:
    def chooseAction(self, observations, possibleActions):
        print("Observations:", observations)
        
        lidar = observations['lidar']
        velocity = observations['velocity']
        
        try:
            car_pos = observations['position']
        except KeyError:
            print("Position not found, using fallback")
            car_pos = observations.get('state', (0, 0))
       
        dist_to_center = sqrt(car_pos[0] ** 2 + car_pos[1] ** 2)

        left = lidar[0]
        front_left = lidar[1]
        front = lidar[2]
        front_right = lidar[3]
        right = lidar[4]

        front_limit = 0.8
        side_limit = 1.4

        if all(val == float('inf') for val in lidar):
            return ('straight', 'accelerate')
        
        vel_boost = 0.05

        if velocity < vel_boost:
            return ('straight', 'accelerate')

        proximity_limit= 0.2

        if left < proximity_limit:
            return ('right', 'brake')
        
        if right < proximity_limit:
            return ('left', 'brake')
        
        if front < proximity_limit:
            if left > right:
                return ('left', 'brake')
            else:
                return ('right', 'brake')

        if dist_to_center > 0.8:
            if dist_to_center > 1.0:
                if left > right:
                    return ('right', 'accelerate')
                else:
                    return ('left', 'accelerate')
            else:
                if left > right:
                    return ('right', 'coast')
                else:
                    return ('left', 'coast')

        if front < front_limit:
            if left > right:
                return ('left', 'brake')
            else:
                return ('right', 'brake')

        if left < side_limit:
            return ('right', 'coast')
        if right < side_limit:
            return ('left', 'coast')
        
        vel_straight = 0.9
        vel_turn = 0.2

        if front_left < front_right - 0.1:
            if velocity > vel_turn:
                return ('right', 'coast')
            else:
                return ('right', 'accelerate')

        elif front_right < front_left - 0.1:
            if velocity > vel_turn:
                return ('left', 'coast')
            else:
                return ('left', 'accelerate')

        dist_wall = 1.2

        if front_left > dist_wall and front_right > dist_wall and \
           left > dist_wall and right > dist_wall:
            if velocity < vel_straight:
                return ('straight', 'accelerate')
            else:
                return ('straight', 'coast')

        if velocity < vel_straight:
            return ('straight', 'accelerate')
        else:
            return ('straight', 'coast')

