#-*- coding: utf-8 -*-
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
import physics.object as pobj
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    test = pobj.world(15, 15, gravity=-5j)
    # p1 = pobj.double_pendulum(test, 0j, trace = 'True')
    p1 = pobj.single_pendulum(test, 0j, length = 3, state = 'motional')
    test.play()
