# -*-coding: utf-8-*-
'''
This module is mode for some useful physical object.
此脚本用于定义几个有用的物理实体
'''
import physics.constant as con

class ball:
    '''
    刚体小球
    '''
    def __init__(self, ax, pos, mass=1., volocity=0j, force=0j):
        """
        ax: type = matplotlib.axes._subplots.AxesSubplot
        For instance, we could initiate the axes variation like this:
        >>> fig, ax = plt.subplots()
        And we could use it like this:
        >>> ax.plot([self.pos.real], [self.pos.imag])

        pos: complex, 小球的初始位置
        mass: float, 小球的质量
        volocity: complex, 小球的初始速度
        force: complex, 小球受到的外力
        """
        self.pos = pos
        self.mass = mass
        self.volocity = volocity
        self.force = force
        self.body, = ax.plot([self.pos.real], [self.pos.imag], 'bo')

    def motion(self):
        a = self.force / self.mass
        self.pos = self.pos + self.volocity * con.dt + 0.5 * a * con.dt ** 2
        self.volocity = self.volocity + a * con.dt
        self.body.set_data([self.pos.real], [self.pos.imag])

class pole:
    '''
    刚体直杆
    '''
    def __init__(self, ax, head, tail, mass = 1.):
        pass