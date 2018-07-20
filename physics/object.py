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
    def __init__(self, w, h, gravity = -5j, dt = 0.01, resistence = 0):
        '''
        w: 世界的宽
        h: 世界的高
        gravity: 重力
        dt: 世界的最小时间单位
        resistance: 阻力系数
        '''
        self.fig, self.ax = plt.subplots(figsize = (5 * w / h, 5))
        self.gravity = gravity
        self.res = resistence
        self.dt = dt
        self.ax.axis([-w / 2, w / 2, -h / 2, h / 2])
        self.object = set({}) # 在该世界中存在的物体

    def register(self, thing):
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
    def __init__(self, world, pos, mass=1., volocity=0j, force=0j):
        """
        world: world类，小球所处的世界
        pos: complex, 小球的初始位置
        mass: float, 小球的质量
        volocity: complex, 小球的初始速度
        force: complex, 小球受到的外力
        """
        self.pos = pos
        self.mass = mass
        self.volocity = volocity
        self.force = force
        self.world = world
        self.body, = self.world.ax.plot([pos.real], [pos.imag], 'o')

    def motion(self, i):
        a = self.force / self.mass
        self.pos = self.pos + self.volocity * self.world.dt + 0.5 * a * self.world.dt ** 2
        self.volocity = self.volocity + a * self.world.dt
        self.body.set_data([self.pos.real], [self.pos.imag])
        
class single_pendulum(thing):
    '''
    普通单摆
    '''
    def __init__(self, world, pos, mass = 1, length = 1, angle = 1/3 * np.pi):
        '''
        world: world类，单摆所处的世界
        pos: 摆的固定端所处的位置
        mass: 摆球的质量
        length: 摆杆的长度
        '''
        # self.world = world
        # self.mass = mass
        # self.force = self.world.gravity
        # self.length = length
        # self.sp = pos
        # self.mp = self.sp - 1j * self.length * np.exp(angle * 1j)
        # self.body = [
        #     self.world.ax.plot([self.sp.real, self.mp.real], [self.sp.imag, self.mp.imag], '-', lw = 1)[0],
        #     self.world.ax.plot([self.sp.real], [self.sp.imag], 'bo')[0],
        #     self.world.ax.plot([self.mp.real], [self.mp.imag], 'ro')[0]
        # ]
        # self.angular_v = 0.

        self.world = world
        self.length = length
        self.angle = angle
        self.sp = pos
        self.mp = ball(self.world, self.sp - 1j * self.length * np.exp(self.angle * 1j), mass = mass)
        self.body = [
            self.world.ax.plot([self.mp.pos.real, self.sp.real], [self.mp.pos.imag, self.sp.imag], '-', lw = 1)[0],
            self.mp.body,
            self.world.ax.plot([self.sp.real], [self.sp.imag], 'ro')[0]
        ]
    
    def motion(self, i):
        # self.mp = self.mp - self.sp
        # theta = 1j * (np.log(self.mp) - np.log(0 - self.length * 1j)) # 偏移角度
        # a = np.abs(self.force) * np.cos(np.pi / 2 - theta) / self.mass # 切向加速度，牛顿第二定理
        # self.angular_v = (self.angular_v * self.length + a * self.world.dt) / self.length
        # self.mp = self.mp * np.exp(self.angular_v * 1j)
        # self.mp = self.mp + self.sp

        # self.body[0].set_data([self.sp.real, self.mp.real], [self.sp.imag, self.mp.imag])
        # self.body[1].set_data([self.sp.real], [self.sp.imag])
        # self.body[2].set_data([self.mp.real], [self.mp.imag])
        
        t = self.sp - self.mp.pos
        self.angle = np.arctan(t.real / t.imag)
        self.mp.force = self.world.gravity * np.sin(self.angle) * np.exp(1j * (np.pi / 2 - self.angle)) # 受力分解

        self.world.ax.scatter([self.mp.force.real], [self.mp.force.imag])

        self.mp.motion(i)

        self.body[0].set_data([self.mp.pos.real, self.sp.real], [self.mp.pos.imag, self.sp.imag])
        self.body[1] = self.mp.body
        self.body[2].set_data([self.sp.real], [self.sp.imag])