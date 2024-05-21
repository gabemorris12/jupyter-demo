# Whitworth Quick Return Mechanism
# Crank rotates at 1 revolution every 5 seconds
from mechanism import *
import matplotlib.pyplot as plt
import numpy as np

O, A, C, Q = get_joints('O A C Q')
D = Joint(name='D', exclude=True)
B = Joint(name='B', exclude=True)

a = Vector((A, B), r=2.5)
b = Vector((O, B))
c = Vector((B, C))
d = Vector((Q, C), theta=0, style='ground')
e = Vector((A, Q), r=6.5, theta=np.pi/2, style='dotted')
f = Vector((A, O), r=3.25, theta=-np.pi/2, style='dotted')
g = Vector((C, D), show=False)
h = Vector((O, D), r=16)

t = np.linspace(0, 5, 200)
theta = 2*np.pi/5*t
omega = np.full(theta.shape, 2*np.pi/5)
alpha = np.zeros(theta.shape)


def loops(x, i):
    temp = np.zeros((3, 2))
    temp[0] = d(x[3]) - c(x[2], x[0]) - a(i) + e()
    temp[1] = a(i) - b(x[1], x[0]) - f()
    temp[2] = h(x[0]) - g(x[4], x[5]) - c(x[2], x[0]) - b(x[1], x[0])
    return temp.flatten()


pos_guess = np.array([np.pi/4, 3, 6, 6, 6, .12])
vel_guess = np.array([5, 5, 5, 5, 5, 5])
acc_guess = np.array([5, 5, 5, 5, 5, 5])

mechanism = Mechanism(vectors=(a, b, c, d, e, f, g, h), origin=O, loops=loops, pos=theta, vel=omega, acc=alpha,
                      guess=(pos_guess, vel_guess, acc_guess))
mechanism.iterate()

ani, fig, ax = mechanism.get_animation(velocity=True, acceleration=True, stamp=t, scale=0.5)

ax.set_title('Whitworth Quick Return')
# ani.save('whitworth.mp4', dpi=240)

fig2, ax2 = plt.subplots()
ax2.plot(t, C.x_velocities, color='maroon')
ax2.set_title(r'Velocity ($\frac{in}{s}$)')

fig3, ax3 = plt.subplots()
ax3.plot(t, C.x_accelerations, color='darkgrey')
ax3.set_title(r'Acceleration ($\frac{in}{s^2}$)')

for ax_ in (ax2, ax3):
    ax_.set_xlabel('Time ($s$)')
    ax_.grid()

plt.show()
