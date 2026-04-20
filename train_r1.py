
from rl_env import TradingEnv



from rl_agent import QAgent



import numpy as np



prices = np.random.rand(1000) * 100  # replace with real price series



env = TradingEnv(prices)



agent = QAgent()



episodes = 50



for ep in range(episodes):



    state = env.reset()



    total_reward = 0



    while True:



        action = agent.choose_action(state)



        next_state, reward, done = env.step(action)



        agent.learn(state, action, reward, next_state)



        state = next_state



        total_reward += reward



        if done:



            break



    print(f"Episode {ep} Reward: {total_reward}")