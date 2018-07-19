#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import physics.constant as pcon
import physics.object as pobj

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize = (5, 5))
    ax.axis([-2, 2, -2, 2])
    ax.grid(True)
    ball1 = pobj.ball(ax, -2 + 0j, volocity = 2 + 1j, force = pcon.gravity)
    def update(i):
        ball1.motion()
        return ball1
    ani = animation.FuncAnimation(
        fig, update, np.arange(0, 2, .01), interval=1)
    plt.show()
