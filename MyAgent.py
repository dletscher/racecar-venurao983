import pickle
import random
import math

class Agent:
    def __init__(self):
        self._Qvalues = {}
        self._values = {}

        self._learningRate = 0.1
        self._discountFactor = 0.95
        self._epsilon = 0.2  # exploration rate

        # Discretization settings
        self._numBins = 5  # number of bins per lidar sensor
        self._velocityBins = 3

    
    import math

    def getBin(self, observation):
        bins = []

        for d in observation:
            try:
                d = float(d)  # convert to float in case it's a string
            except ValueError:
                d = 0.0  # default to 0.0 if conversion fails

            if math.isinf(d):
                d = 1.0  # treat infinite as max distance

            d = min(max(d, 0.0), 1.0)  # clamp to [0.0, 1.0]

            bins.append(min(int(d * self._numBins), self._numBins - 1))

        return tuple(bins)


    def chooseAction(self, observations, possibleActions):
        state = self.getBin(observations)

        # Epsilon-greedy policy
        if random.random() < self._epsilon:
            return random.choice(possibleActions)

        # Pick best action
        bestAction = possibleActions[0]
        bestValue = self._Qvalues.get(state + (bestAction,), 0)
        for action in possibleActions:
            q = self._Qvalues.get(state + (action,), 0)
            if q > bestValue:
                bestValue = q
                bestAction = action
        return bestAction

    def updateValues(self, observation1, action, observation2, reward):
        state1 = self.getBin(observation1)
        state2 = self.getBin(observation2)

        oldQ = self._Qvalues.get(state1 + (action,), 0)
        nextValue = max([self._Qvalues.get(state2 + (a,), 0) for a in [('left','accelerate'), ('left', 'coast'), ('left','brake'),
                                                                      ('straight','accelerate'), ('straight', 'coast'), ('straight','brake'),
                                                                      ('right','accelerate'), ('right', 'coast'), ('right','brake')]])

        newQ = (1 - self._learningRate) * oldQ + self._learningRate * (reward + self._discountFactor * nextValue)
        self._Qvalues[state1 + (action,)] = newQ
        self._values[state1] = max([self._Qvalues.get(state1 + (a,), 0) for a in [('left','accelerate'), ('left', 'coast'), ('left','brake'),
                                                                                 ('straight','accelerate'), ('straight', 'coast'), ('straight','brake'),
                                                                                 ('right','accelerate'), ('right', 'coast'), ('right','brake')]])

    def train(self, repetitions):
        from Track import buildTrack
        from Racecar import Racecar

        for _ in range(repetitions):
            track = buildTrack(random.randint(1, 8))
            car = Racecar(track)
            obs, _, done = car.step(('straight','coast'))

            steps = 0
            while not done and steps < 1000:
                steps += 1
                action = self.chooseAction(obs, car.actions())
                nextObs, reward, done = car.step(action)
                self.updateValues(obs, action, nextObs, reward)
                obs = nextObs

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self._values, f)
            pickle.dump(self._Qvalues, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self._values = pickle.load(f)
            self._Qvalues = pickle.load(f)
