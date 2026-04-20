import numpy as np



class QAgent:



    def __init__(self):



        self.q_table = {}



        self.alpha = 0.1



        self.gamma = 0.9



        self.epsilon = 0.1



    def get_q(self, state):



        return self.q_table.get(str(state), [0, 0, 0])



    def choose_action(self, state):



        if np.random.random() < self.epsilon:



            return np.random.randint(0, 3)



        return np.argmax(self.get_q(state))



    def learn(self, state, action, reward, next_state):



        q = self.get_q(state)



        q_next = self.get_q(next_state)



        q[action] = q[action] + self.alpha * (



            reward + self.gamma * max(q_next) - q[action]



        )



        self.q_table[str(state)] = q
