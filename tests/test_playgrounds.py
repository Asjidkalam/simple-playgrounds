from simple_playgrounds.agents.controllers import Random
from simple_playgrounds.agents import BaseAgent
from simple_playgrounds import Engine
from simple_playgrounds.agents.sensors import *
from simple_playgrounds.agents.parts import ForwardPlatform

from simple_playgrounds.playgrounds.collection.test import *


# Add/remove agent from a playground
def test_add_remove_agent():
    playground_1 = SingleRoom(size=(200, 200))
    playground_2 = SingleRoom(size=(200, 200))
    agent = BaseAgent(controller=Random(), interactive=False, platform=ForwardPlatform)
    playground_1.add_agent(agent)
    playground_1.remove_agent(agent)
    assert playground_1.agents == []
    playground_2.add_agent(agent)


# Create an engine then add an agent
def test_engine():
    playground = SingleRoom(size=(200, 200))
    agent = BaseAgent(controller=Random(), interactive=False, platform=ForwardPlatform)
    engine = Engine(playground, time_limit=100)
    playground.add_agent(agent)
    assert len(engine.agents) == 1
    playground.remove_agent(agent)
    assert len(engine.agents) == 0


# Run the playground, check that position changed
def test_engine_run():
    playground = SingleRoom(size=(200, 200))
    agent = BaseAgent(controller=Random(), interactive=False, platform=ForwardPlatform)
    playground.add_agent(agent)
    engine = Engine(playground, time_limit=100)

    pos_start = agent.position
    assert pos_start == (100., 100., 0.)
    engine.run()
    assert pos_start != agent.position

    playground.remove_agent(agent)
    playground.add_agent(agent)

    engine = Engine(playground, time_limit=100)
    assert len(engine.agents) == 1
    engine.run()

    playground.remove_agent(agent)
    engine = Engine(playground,  time_limit=100)
    playground.add_agent(agent)
    assert len(engine.agents) == 1

    engine.run()



# Run all test playgrounds with basic non-interactive agent
def test_all_test_playgrounds():

    agent = BaseAgent(controller=Random(), interactive=False, platform=ForwardPlatform)

    for pg_class in PlaygroundRegister.filter('test'):
        pg = pg_class()

        pg.add_agent(agent)

        print('Starting testing of ', pg_class.__name__)

        engine = Engine(pg, time_limit=10000)
        engine.run()

        assert 0 < agent.position[0] < pg.size[0]
        assert 0 < agent.position[1] < pg.size[1]

        engine.terminate()


# Run all test playgrounds with 100 agents
def test_multiagents():

    for pg_class in PlaygroundRegister.filter('test'):

        pg = pg_class()
        print('Starting Multiagent testing of ', pg_class.__name__)
        center, shape = pg.area_rooms[(0,0)]
        pos_area_sampler = PositionAreaSampler(center = center, area_shape='rectangle', width_length=shape)

        for i in range(100):
            agent = BaseAgent(pos_area_sampler, controller=Random(), interactive=True, platform=ForwardPlatform)
            pg.add_agent(agent)

        assert len(pg.agents) == 100

        engine = Engine(pg, time_limit=100, screen=False)
        engine.run(update_screen= False)


# Run all test playgrounds with 10 agents
def test_multiagents_no_overlapping():

    for pg_class in PlaygroundRegister.filter('test'):

        pg = pg_class()
        print('Starting Multiagent testing of ', pg_class.__name__)
        center, shape = pg.area_rooms[(0,0)]
        pos_area_sampler = PositionAreaSampler(center = center, area_shape='rectangle', width_length=shape)

        for i in range(2):
            agent = BaseAgent(pos_area_sampler, controller=Random(), interactive=True, platform=ForwardPlatform)
            pg.add_agent(agent, 1000)

        assert len(pg.agents) == 2

        engine = Engine(pg, time_limit=100, screen=False)
        engine.run(update_screen= False)


# Run all test playgrounds with 10 agents
def test_multisteps():

    agent = BaseAgent(controller=Random(), interactive=False, platform=ForwardPlatform)

    sensor = Touch(name='touch_1', anchor=agent.base_platform)
    agent.add_sensor(sensor)

    for pg_class in PlaygroundRegister.filter('test'):

        pg = pg_class()
        print('Starting Multistep testing of ', pg_class.__name__)
        pg.add_agent(agent, 1000)

        engine = Engine(pg, time_limit=10000, screen=False)

        terminate = False
        while not terminate:

            actions = {}
            for agent in engine.agents:
                actions[agent] = agent.controller.generate_commands()

            terminate = engine.multiple_steps(actions, n_steps=3)
            engine.update_observations()

        engine.terminate()


def test_agent_in_different_environments():

    print('Testing of agent moving to different environments')

    agent = BaseAgent(controller=Random(), interactive=False, platform=ForwardPlatform)
    pg_1 = SingleRoom((300, 300))
    pg_2 = SingleRoom((100, 100))


    # Play in pg 1
    pg_1.add_agent(agent)
    engine = Engine(pg_1, 100)
    engine.run()
    engine.terminate()

    # Play in pg 2
    pg_2.add_agent(agent)
    engine = Engine(pg_2, 100)
    engine.run()
    engine.terminate()

    # Alternate between playgrounds
    pg_1.reset()
    pg_2.reset()

    engine_1 = Engine(pg_1, 100)
    engine_2 = Engine(pg_2, 100)

    print('going to playground 1')
    pg_1.add_agent(agent)
    engine_1.run(10)
    pg_1.remove_agent(agent)

    print('going to playground 2')
    pg_2.add_agent(agent)
    engine_2.run(10)
    pg_2.remove_agent(agent)

    print('running playground 1 without agent')
    engine_1.run(10)
    assert engine_1._elapsed_time == 20

    print('agent returning to playground 1')
    pg_1.add_agent(agent)
    engine_1.run()
    engine_1.terminate()


    print('agent returning to playground 2')
    pg_2.add_agent(agent)
    engine_2.run()
    engine_2.terminate()

    print(' Fail when adding agent to 2 playgrounds ')
    pg_1.reset()
    pg_2.reset()
    pg_1.add_agent(agent)


