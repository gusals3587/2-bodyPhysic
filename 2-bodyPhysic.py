import unittest
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from typing import List

def main():
    fig, ax = plt.subplots()
    weight = Body(pos=[0.5, 0.0], v=[0.0, 1.63], dt=0.1, ax=ax)
    anim = FuncAnimation(fig, weight, init_func=weight.init)
    plt.show()


class Body():

    # the syntax is position, velocity, and the Axes object from matplotlib
    def __init__(self, pos: List[float], v: List[float], ax, dt: float):
        self.pos = [pos]
        self.v = v
        self.ax = ax
        self.line, = ax.plot([], [])
        self.ax.set_xlim(-1.2, 1)
        self.ax.set_ylim(-1, 0.8)
        self.r = np.linalg.norm(pos)
        self.a = [-self.pos[-1][i] / (self.r ** 3) for i in range(2)]
        self.dt = dt
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def init(self):
        self.line.set_data([tmp[0] for tmp in self.pos], [tmp[1] for tmp in self.pos])
        return self.line,

    def __call__(self, i):
        if i == 0:
            self.v = [self.v[i] + ((self.dt / 2) * self.a[i]) for i in range(2)]
        else:
            self.v = [self.v[i] + (self.dt * self.a[i]) for i in range(2)]
        self.pos += [[self.pos[-1][i] + (self.dt * self.v[i]) for i in range(2)]]
        self.r = np.linalg.norm(self.pos[-1])
        # the acceleration vector's x-component's direction will always be the opposite of x axis
        self.a = [-self.pos[-1][i] / (self.r ** 3) for i in range(2)]
        #TODO make it prettier
        self.line.set_data([tmp[0] for tmp in self.pos], [tmp[1] for tmp in self.pos])
        return self.line,


class TestSimulationMethod(unittest.TestCase):

    def setUp(self):
        self.fig, self.ax = plt.subplots()
        self.body = Body(pos=[0.5, 0.0], v=[0.0, 1.63], dt=0.1, ax=self.ax)


    def test_bodyInit(self):
        testLine = self.body.init()[0]
        targetLine = self.ax.plot(0.5, 0.0)[0]
        self.assertEqual(targetLine.get_data(), testLine.get_data(), msg="bodyInit is not working")

    def test_bodyCall(self):
        self.body(0)
        self.body(1)
        self.body(2)
        testLine = self.body(3)[0]
        targetLine = self.ax.plot([0.5, 0.48, 0.423, 0.337], [0.0, 0.163, 0.313, 0.443])[0]
        for i in range(2):
            test = testLine.get_data()[i]
            target = targetLine.get_data()[i]
            for testPos, targetPos in zip(test, target):
                self.assertEqual(targetPos, round(testPos, 3))


if __name__ == "__main__":
    main()