from flatland.playgrounds.playground import *
from test_pg import *

pg_params = {
    'playground_type': 'chest-test',

}

pg = PlaygroundGenerator.create(pg_params)

from flatland.agents import agent
from flatland.default_parameters.agents import *

agent_params = {
    'name': 'Agent 1',
    'frame': {
        'type': 'forward',
        'params': {
            'base_radius': 10,
                }
    },
    'controller': {
        'type': 'keyboard'
    },
    'sensors': {
        #'rgb_1': {**rgb_default, **{'bodyAnchor': 'head', 'fovResolution': 128, 'fovRange': 1000} },
        'rgb_2': {**rgb_default, **{'bodyAnchor': 'base', 'fovResolution': 64, 'fovRange': 300, }},
        #'touch_1' : touch_default,
    },
}

my_agent = agent.Agent(agent_params)

from flatland.game_engine import Engine

engine_parameters = {
    'inner_simulation_steps': 5,
    'scale_factor': 1,

    'display': {
        'playground' : True,
        'frames' : True,
    }
}

rules = {
    'replay_until_time_limit': True,
    'time_limit': 10000
}

game = Engine(playground=pg, agents=[my_agent], rules=rules, engine_parameters=engine_parameters )


import cv2
import time

t1 = time.time()


while game.game_on:

    actions = {}
    for agent in game.agents:
        actions[agent.name] = agent.get_controller_actions()

    game.step(actions)
    game.update_observations()

    #     for ent in game.playground.entities: print(ent, ent.is_initial_entity)
        

    game.render_simulation(sensors=True, actions=False)

print(1000 / (time.time() - t1))
game.terminate()