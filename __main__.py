import pygame
import numpy as np
import cv2


###########################################
# BUILDING A PLAYGROUND
###########################################
import flatland.playgrounds.playground as playground
from flatland.default_parameters.entities import *

### Basic entities
basic_1 = basic_default.copy()
basic_1['position'] = [80, 80, 0.2]
basic_1['physical_shape'] = 'triangle'
basic_1['radius'] = 20


basic_1['texture'] = {
    'type': 'uniform_grained',
    'min': [150, 0, 50],
    'max': [200, 0, 100],
    'size_grains': 8
}



basic_2 = basic_default.copy()
basic_2['position'] = [80, 120, 0]
basic_2['physical_shape'] = 'pentagon'
basic_2['radius'] = 30
basic_2['movable'] = False

basic_2['texture'] = {
    'type': 'polar_stripes',
    'color_1': [0, 0, 150],
    'color_2': [250, 0, 100],
    'n_stripes' : 10
}



### Edibles

edible_1 = edible_default.copy()
edible_1['position'] = [200, 50, 0.2]
edible_1['physical_shape'] = 'pentagon'
edible_1['mass'] = 100
edible_1['radius'] = 20
edible_1['movable'] = False

### Absorbables

absorbable_1 = absorbable_default.copy()
absorbable_1['position'] = [350, 200, 0.2]

absorbable_2 = absorbable_default.copy()
absorbable_2['position'] = [350, 220,0.5]

### Dispenser

dispenser_1 = dispenser_default.copy()
dispenser_1['position'] = [350, 50,0]
dispenser_1['area'] = [[360, 100],[380, 120]]

### Yielder

yielder_1 = yielder_default.copy()
yielder_1['area'] = [[100, 400],[200, 600]]

### Graspable
grasp_1 = graspable_default.copy()
grasp_1['position'] = [150, 200 ,0]

### Door
door_opener = door_opener_default.copy()
door_opener['door']['position'] = [200, 300, math.pi/2]
door_opener['position'] = [50, 300, 0]

pg_params = {
    'scene': {
        'shape': [600, 400]
    },
    'entities': [basic_1, basic_2, edible_1, absorbable_1, absorbable_2, dispenser_1, yielder_1, grasp_1, door_opener]
}

pg = playground.PlaygroundGenerator.create('rooms_2_edible', pg_params )

#################################################
##### BUILDING AN AGENT
#################################################

import flatland.agents.agent as agent
from flatland.default_parameters.agents import *

agent_params = {
    'body' : {
        'type': 'forward',
        'params' : {
            'base_radius': 50
                }
    },
    'controller' :{
        'type': 'human'
    },
    'sensors':{
        'rgb_1': {**rgb_default, **{'bodyAnchor': 'head'} },
        'touch_1' : touch_default,
    },
    'starting_position':{
        'type': 'fixed',
        'position' : [200, 200, 0]
    }
}

my_agent = agent.Agent(agent_params)

####################################################
####### Create game with playground and parameters
####################################################

from flatland.game_engine import Engine

game_parameters = {
    'rules':{
        'game_mode' : 'time',
        'horizon' : 1000
    },
    'engine' : {
        'speed_ratio': 1,
        'aspect_ratio': 1,
        'frame_rate': 24
    },
    'display': {
        'playground' : True,
        'physical_bodies' : True,
    }
}


game = Engine( playground = pg, agents = [my_agent], game_parameters = game_parameters )


clock = pygame.time.Clock()


while game.game_on:

    game.update_observations()
    game.set_actions()
    game.step()

    for agent in game.agents:

        observations = game.agents[agent]['agent'].observations

        for obs in observations:

            im = np.asarray( observations[obs])
            im = np.expand_dims(im, 0)
            im = cv2.resize( im, (512, 50), interpolation=cv2.INTER_NEAREST )
            cv2.imshow( obs, im )
            cv2.waitKey(1)

    game.display_full_scene()



    clock.tick(20)
