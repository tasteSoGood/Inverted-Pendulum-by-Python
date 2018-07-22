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
        thing.force = thing.mass * self.gravity
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
    def __init__(self, world, pos, mass=1., volocity=0j, force=0j, trace = False, state = 'stable'):
        """
        world: world类，小球所处的世界
        pos: complex, 小球的初始位置
        mass: float, 小球的质量
        volocity: complex, 小球的初始速度
        force: complex, 小球受到的外力
        trace: 是否跟踪路径
        state: 小球的状态，如果是stable，那么只做受力分析，不改变位置
        """
        self.pos = pos
        self.mass = mass
        self.volocity = volocity
        self.force = force
        self.world = world
        self.trace = trace
        self.state = state
        if trace and self.state == 'motional':
            # 当需要循迹并且小球处于可运动状态的时候，do
            self.data = {
                'x': [pos.real],
                'y': [pos.imag]
            }
            self.body = [
                self.world.ax.plot([pos.real], [pos.imag], 'o')[0], 
                self.world.ax.plot(self.data['x'], self.data['y'], '-', lw = 0.5, color = 'black')[0]
            ]
        else:
            self.body, = self.world.ax.plot([pos.real], [pos.imag], 'o')

        self.world.register(self) # 在世界中注册

    def motion(self, i):
        a = self.force / self.mass
        if self.state == 'free': # 最自由的状态才能自主计算位移
            self.pos = self.pos + self.volocity * self.world.dt + 0.5 * a * self.world.dt ** 2
        self.volocity = self.volocity + a * self.world.dt
        if self.trace and self.state == 'motional':
            self.body[0].set_data([self.pos.real], [self.pos.imag])
            self.data['x'].append(self.pos.real)
            self.data['y'].append(self.pos.imag)
            self.body[1].set_data(self.data['x'], self.data['y'])
        else:
            self.body.set_data([self.pos.real], [self.pos.imag])
        
class single_pendulum(thing):
    '''
    普通单摆
    '''
    def __init__(self, world, pos, mass0 = 1, mass = 1, length = 1, angle = 1/3 * np.pi, trace = False, state = 'stable'):
        '''
        world: world类，单摆所处的世界
        pos: 摆的固定端所处的位置
        mass0: 固定点的质量
        mass: 摆球的质量
        length: 摆杆的长度
        trace: 是否跟踪路径
        '''
        self.world = world
        self.force = 0j
        self.length = length
        self.mass = mass0 + mass
        self.ball_0 = ball(
            world = self.world,
            pos = pos,
            mass = mass0,
            state = state
        )
        self.ball_1 = ball(
            world = self.world,
            pos = self.ball_0.pos - 1j * self.length * np.exp(angle * 1j),
            mass = mass,
            trace = trace,
            state = 'motional'
        )
        self.line, = self.world.ax.plot([self.ball_0.pos.real, self.ball_1.pos.real], [self.ball_0.pos.imag, self.ball_1.pos.imag], '-', lw = 1)
        self.angular_v = 0.

        self.world.register(self)
    
    def motion(self, i):
        '''
        说明：此处单摆的运动使用角速度来表述，从物理上来说，单摆在某一时刻受到重力以及向心力的共同作用
        一旦摆球具有速度，根据公式$f = m\frac{v^2}{r}$得到一个指向单摆固定端的向心力，而重力分量的方
        向为切线方向，两个力在方向上是正交的。
        曾经实现过一个不约束摆长的方法，完全计算线速度，结果由于计算的偏差导致摆球的运动非常的混乱。所
        以这里忽略线速度的影响，直接计算切向加速度
        '''
        self.ball_1.pos = self.ball_1.pos - self.ball_0.pos # 动点偏移到原点附近
        t = (0j - self.ball_1.pos) / np.abs(0j - self.ball_1.pos) # 径向单位向量，指向单摆的固定点
        theta = np.arctan(t.real / t.imag) # 移动端此时的偏角
        a = np.abs(self.ball_1.force) * np.cos(np.pi / 2 - theta) / self.ball_1.mass # 切向加速度，牛顿第二定理
        self.angular_v = (self.angular_v * self.length + a * self.world.dt) / self.length # 角速度 = 线速度 / 摆长
        self.ball_1.pos = self.ball_1.pos * np.exp(self.angular_v * 1j)
        # self.ball_1.pos = self.length / np.abs(self.ball_1.pos) * self.ball_1.pos * np.exp(self.angular_v * 1j)
        self.ball_1.pos = self.ball_1.pos + self.ball_0.pos # 偏移回原来的位置
        
        # 这里应当传入运动端的线速度，用来给固定端传递一个向心力（的反作用力）
        self.ball_1.volocity = self.angular_v * self.length # 标量
        to_center = (self.ball_1.volocity ** 2) * self.ball_1.mass / self.length # 向心力（标量）
        self.ball_0.force += to_center * np.cos(theta) * -1j # 在重力方向上的分量

        self.line.set_data([self.ball_0.pos.real, self.ball_1.pos.real], [self.ball_0.pos.imag, self.ball_1.pos.imag])
        self.ball_0.motion(i)
        self.ball_1.motion(i)

class double_pendulum(thing):
    '''
    双摆
    '''
    def __init__(self, world, pos, mass0 = 1, mass1 = 1, mass2 = 1, length1 = 1, length2 = 1, angle1 = 1 / 3 * np.pi, angle2 = 1 / 3 * np.pi, trace = False, state = 'stable'):
        '''
        mass1: 从上向下数第一个摆球的质量
        mass2: 从上向下数第二个摆球的质量
        length1: 第一个摆杆的长度
        length2: 第二个摆杆的长度
        '''
        self.world = world
        self.mass = mass0 + mass1 + mass2
        self.force = 0j
        self.pendulum_1 = single_pendulum(
            world = self.world,
            pos = pos,
            mass0 = mass0,
            mass = mass1,
            length = length1,
            angle = angle1,
            trace = False,
            state = state
        )
        self.pendulum_2 = single_pendulum(
            world = self.world,
            pos = self.pendulum_1.ball_1.pos,
            mass0 = mass1,
            mass = mass2,
            length = length2,
            angle = angle2,
            trace = trace,
            state = 'motional'
        )
        self.pendulum_2.ball_0 = self.pendulum_1.ball_1

        self.world.register(self)
    
    def motion(self, i):
        self.pendulum_1.motion(i)
        self.pendulum_2.motion(i)