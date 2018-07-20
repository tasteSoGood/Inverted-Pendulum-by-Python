# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

pole_length = 1.5 # 杆长
mass = 1 # 摆球质量
angular_v = 0. # 角速度
resistance = 0.01 # 阻尼系数
gravity = 5
dt = .01

fig, ax = plt.subplots(figsize = (10, 10))

sp, mp = 0 + 0j, (0 - pole_length * 1j) * np.exp(np.pi * 1/3 * 1j)
line, = ax.plot([sp.real, mp.real], [sp.imag, mp.imag], '-', lw = 1)
stable_point, = ax.plot([sp.real], [sp.imag], 'bo')
motion_point, = ax.plot([mp.real], [mp.imag], 'ro')

ax.axis([-2, 2, -2, 2])
ax.grid(True)

def update(i):
    global mp, angular_v
    
    theta = 1j * (np.log(mp) - np.log(0 - pole_length * 1j)) # 偏移角度
    a = gravity * np.cos(np.pi / 2 - theta) / mass # 切向加速度，牛顿第二定理
    angular_v = (angular_v * pole_length + a * dt) / pole_length
    # angular_v = angular_v * (1 - resistance)

    mp = mp * np.exp(angular_v * 1j)
    stable_point.set_data([sp.real], [sp.imag])
    motion_point.set_data([mp.real], [mp.imag])
    line.set_data([sp.real, mp.real], [sp.imag, mp.imag])
    return motion_point, stable_point, line

def mouse_motion(event):
    global sp
    sp = event.xdata + 0j

if __name__ == "__main__":
    # 把鼠标事件监听放在动画之前，才能生效
    fig.canvas.mpl_connect('motion_notify_event', mouse_motion) # 监听鼠标移动
    ani = animation.FuncAnimation(fig, update, np.arange(0, 2, .01), interval = 1)
    plt.show()