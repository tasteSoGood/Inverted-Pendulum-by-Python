# -*-coding: utf-8-*-
'''
This module was made for some useful physical object.
此脚本用于定义几个有用的物理实体
'''
from abc import ABCMeta, abstractmethod 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class world:
    '''
    创造一个2D世界
    '''
    def __init__(self, w, h, gravity = -5j, dt = 0.01):
        '''
        w: 世界的宽
        h: 世界的高
        gravity: 重力
        dt: 世界的最小时间单位
        resistance: 阻力系数
        '''
        self.fig, self.ax = plt.subplots(figsize = (5 * w / h, 5))
        self.force = gravity
        self.dt = dt
        self.ax.axis([-w / 2, w / 2, -h / 2, h / 2])
        self.object = set({}) # 在该世界中存在的物体

    def register(self, thing):
        thing.force += thing.mass * self.force
        self.object.add(thing)

    def motion(self, i):
        for item in self.object:
            item.motion(i)
    
    def play(self):
        ani = animation.FuncAnimation(self.fig, self.motion, np.arange(0, 2, .01), interval = 1)
        plt.show()

# 物体抽象类
class thing:
    __metaclass__ = ABCMeta
    @abstractmethod
    def motion(self, i):
        pass

# 物体
class ball(thing):
    '''
    刚体小球
    '''
    def __init__(self, world, pos, mass = 1, v = 0j, f = 0j, trace = False, stable = False):
        # 物理参数
        self.world = world
        self.pos = pos
        self.mass = mass
        self.v = 0 if stable else v
        self.force = f

        # 标志位
        self.flag = {
            'trace': trace,
            'stable': stable
        }

        # 数据
        self.data = [pos]

        # 绘图参数
        self.body, = self.world.ax.plot(self.pos.real, self.pos.imag, 'o')
        if trace and not stable:
            self.trace, = self.world.ax.plot(np.real(self.data), np.imag(self.data), '-', lw = 0.5, c = 'black')

        # 注册
        self.world.register(self)

    def next(self):
        # 计算下一步
        if not self.flag['stable']:
            self.pos = self.pos + (self.v + 0.5 * self.force / self.mass * self.world.dt) * self.world.dt
            self.data.append(self.pos)
            self.v = self.v + self.force / self.mass * self.world.dt

    def motion(self, i):
        self.next()
        if self.flag['trace']:
            self.trace.set_data(np.real(self.data), np.imag(self.data))
        self.body.set_data(self.pos.real, self.pos.imag)

class pole(thing):
    '''
    轻质杆
    '''
    def __init__(self, world, start, end, length):
        pass

if __name__ == '__main__':
    w = world(10, 10)
    b = ball(w, 0j, v = 10, f = -50j, trace = True)
    w.play()