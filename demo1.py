#-*- coding: utf-8 -*-
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
import physics.object as pobj
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    test = pobj.world(15, 15)
    p1 = pobj.single_pendulum(test, 0j, length = 2)
    p2 = pobj.single_pendulum(test, 0j, length = 3)
    p3 = pobj.single_pendulum(test, 0j, length = 4)
    p4 = pobj.single_pendulum(test, 0j, length = 5)
    p5 = pobj.single_pendulum(test, 0j, length = 6)
    test.register(p1)
    test.register(p2)
    test.register(p3)
    test.register(p4)
    test.register(p5)
    test.play()

    # def func(g, angle):
    #     return g * np.sin(angle) * np.exp(1j * (np.pi / 2 - angle))
    # z1 = 1 + 2j
    # z2 = -2 + 5j
    # plt.figure(figsize = (6, 6))
    # plt.axis([-10, 10, -10, 10])
    # plt.grid(True)
    # plt.scatter([0, z1.real, z2.real, (z1 + z2).real], [0, z1.imag, z2.imag, (z1 + z2).imag])
    # plt.show()