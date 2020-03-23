from flatland.tests.test_basics.test_pg import *
from flatland.agents import agent

# pg = PlaygroundGenerator.create('contact_01', room_shape = [200, 200])
pg = PlaygroundGenerator.create('contact_01', room_shape = [250, 200])

agents = []
#
# for i in range(10):
#     if i == 0:
#         my_agent = agent.Agent('forward', controller_type = 'keyboard')
#     else:
#         my_agent = agent.Agent('forward', controller_type='random')
#     my_agent.add_sensor('depth', 'depth_1', fov_resolution = 128)
#     #my_agent.add_sensor('touch', 'touch_1')
#     my_agent.starting_position = {
#                 'type': 'rectangle',
#                 'x_range': [80, 120],
#                 'y_range': [80, 120],
#                 'angle_range': [0, 3.14 * 2],
#             }
#
#     agents.append(my_agent)
#

my_agent = agent.Agent('forward', name = 'mercotte', controller_type = 'keyboard')
my_agent.add_sensor('depth', 'depth_1', fov_resolution = 128)
my_agent.starting_position = {
            'type': 'rectangle',
            'x_range': [80, 120],
            'y_range': [80, 120],
            'angle_range': [0, 3.14 * 2],
        }

agents.append(my_agent)


from flatland.game_engine import Engine

engine_parameters = {
    'inner_simulation_steps': 5,
    'scale_factor': 1,

    'display': {
        'playground' : False,
        'frames' : True,
    }
}

rules = {
    'replay_until_time_limit': True,
    'time_limit': 10000
}

game = Engine(playground=pg, agents=agents, rules=rules, engine_parameters=engine_parameters )


import cv2
import time

t1 = time.time()


while game.game_on:

    actions = {}
    for agent in game.agents:
        actions[agent.name] = agent.get_controller_actions()

    game.multiple_steps(actions, 1)
    game.update_observations()


    for agent in game.agents[:1]:

        observations = agent.observations

        for obs in observations:

            if 'laser' in  obs:
                #print(observations[obs])
                pass

            else:

                im = cv2.resize(observations[obs], (512, 50), interpolation=cv2.INTER_NEAREST)
                cv2.imshow(obs, im)
                cv2.waitKey(1)

        if agent.reward != 0: print(agent.reward)

        print(agent.name, agent.health)

    img = game.generate_playground_image()
    cv2.imshow('test', img)
    cv2.waitKey(15)

print(1000 / (time.time() - t1))
game.terminate()