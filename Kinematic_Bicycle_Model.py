#!/usr/bin/env python
# coding: utf-8

# In this notebook, you will implement the kinematic bicycle model. The model accepts velocity and steering rate inputs and steps through the bicycle kinematic equations. Once the model is implemented, you will provide a set of inputs to drive the bicycle in a figure 8 trajectory.
# 
# The bicycle kinematics are governed by the following set of equations:
# 
# \begin{align*}
# \dot{x}_c &= v \cos{(\theta + \beta)} \\
# \dot{y}_c &= v \sin{(\theta + \beta)} \\
# \dot{\theta} &= \frac{v \cos{\beta} \tan{\delta}}{L} \\
# \dot{\delta} &= \omega \\
# \beta &= \tan^{-1}(\frac{l_r \tan{\delta}}{L})
# \end{align*}
# 
# where the inputs are the bicycle speed $v$ and steering angle rate $\omega$. The input can also directly be the steering angle $\delta$ rather than its rate in the simplified case. The Python model will allow us both implementations.
# 
# In order to create this model, it's a good idea to make use of Python class objects. This allows us to store the state variables as well as make functions for implementing the bicycle kinematics. 
# 
# The bicycle begins with zero initial conditions, has a maximum turning rate of 1.22 rad/s, a wheelbase length of 2m, and a length of 1.2m to its center of mass from the rear axle.
# 
# From these conditions, we initialize the Python class as follows:





import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math as m
class Bicycle():
    def __init__(self):
        self.xc = 0
        self.yc = 0
        self.theta = 0
        self.delta = 0
        self.beta = 0
        
        self.L = 2
        self.lr = 1.2
        self.w_max = 1.22
        
        self.sample_time = 0.01
        
    def reset(self):
        self.xc = 0
        self.yc = 0
        self.theta = 0
        self.delta = 0
        self.beta = 0


# A sample time is required for numerical integration when propagating the kinematics through time. This is set to 10 milliseconds. We also have a reset function which sets all the state variables back to 0. 
# 
# With this sample time, implement the kinematic model using the function $\textit{step}$ defined in the next cell. The function should take speed + angular rate as inputs and update the state variables. Don't forget about the maximum turn rate on the bicycle!




class Bicycle(Bicycle):
    def step(self, v, w):
        # ==================================
        #  Implement kinematic model here
        # ==================================
       
        
        
        self.xc += v * self.sample_time * m.cos(self.theta + self.beta)
        self.yc += v * self.sample_time * m.sin(self.theta + self.beta)
        self.theta += (v * m.cos(self.beta)*m.tan(self.delta) / self.L) * self.sample_time
        self.beta = m.atan(self.lr * m.tan(self.delta) / self.L)
        self.delta += w * self.sample_time
        
        
        pass


# With the model setup, we can now start giving bicycle inputs and producing trajectories. 
# 
# Suppose we want the model to travel a circle of radius 10 m in 20 seconds. Using the relationship between the radius of curvature and the steering angle, the desired steering angle can be computed.
# 
# \begin{align*}
#     \tan{\delta} &= \frac{L}{r} \\
#     \delta &= \tan^{-1}(\frac{L}{r}) \\
#            &= \tan^{-1}(\frac{2}{10}) \\
#            &= 0.1974
# \end{align*}
# 
# If the steering angle is directly set to 0.1974 using a simplied bicycled model, then the bicycle will travel in a circle without requiring any additional steering input. 
# 
# The desired speed can be computed from the circumference of the circle:
# 
# \begin{align*}
#     v &= \frac{d}{t}\\
#      &= \frac{2 \pi 10}{20}\\
#      &= \pi
# \end{align*}
# 
# We can now implement this in a loop to step through the model equations. We will also run our bicycle model solution along with your model to show you the expected trajectory. This will help you verify the correctness of your model.




sample_time = 0.01
time_end = 20
model = Bicycle()


# set delta directly
model.delta = np.arctan(2/10)


t_data = np.arange(0,time_end,sample_time)
x_data = np.zeros_like(t_data)
y_data = np.zeros_like(t_data)
x_solution = np.zeros_like(t_data)
y_solution = np.zeros_like(t_data)

for i in range(t_data.shape[0]):
    x_data[i] = model.xc
    y_data[i] = model.yc
   
    model.step(np.pi, 0)

    #model.beta = 0
    #solution_model.beta=0
    
plt.axis('equal')
plt.plot(x_data, y_data)

plt.show()


# The plot above shows the desired circle of 10m radius. The path is slightly offset which is caused by the sideslip effects due to $\beta$. By forcing $\beta = 0$ through uncommenting the last line in the loop, you can see that the offset disappears and the circle becomes centered at (0,10). 
# 
# However, in practice the steering angle cannot be directly set and must be changed through angular rate inputs $\omega$. The cell below corrects for this and sets angular rate inputs to generate the same circle trajectory. The speed $v$ is still maintained at $\pi$ m/s.




sample_time = 0.01
time_end = 20
model.reset()


t_data = np.arange(0,time_end,sample_time)
x_data = np.zeros_like(t_data)
y_data = np.zeros_like(t_data)
x_solution = np.zeros_like(t_data)
y_solution = np.zeros_like(t_data)

for i in range(t_data.shape[0]):
    x_data[i] = model.xc
    y_data[i] = model.yc
    
    if model.delta < np.arctan(2/10):
        model.step(np.pi, model.w_max)
    else:
        model.step(np.pi, 0)
        

    


plt.axis('equal')
plt.plot(x_data, y_data)


plt.show()


# Here are some other example trajectories: a square path, a spiral path, and a wave path. Uncomment each section to view.




sample_time = 0.01
time_end = 60
model.reset()


t_data = np.arange(0,time_end,sample_time)
x_data = np.zeros_like(t_data)
y_data = np.zeros_like(t_data)
x_solution = np.zeros_like(t_data)
y_solution = np.zeros_like(t_data)

# maintain velocity at 4 m/s
v_data = np.zeros_like(t_data)
v_data[:] = 4 

w_data = np.zeros_like(t_data)

# ==================================
#  Square Path: set w at corners only
# ==================================
w_data[670:670+100] = 0.753
w_data[670+100:670+100*2] = -0.753
w_data[2210:2210+100] = 0.753
w_data[2210+100:2210+100*2] = -0.753
w_data[3670:3670+100] = 0.753
w_data[3670+100:3670+100*2] = -0.753
w_data[5220:5220+100] = 0.753
w_data[5220+100:5220+100*2] = -0.753

# ==================================
#  Spiral Path: high positive w, then small negative w
# ==================================
# w_data[:] = -1/100
# w_data[0:100] = 1

# ==================================
#  Wave Path: square wave w input
# ==================================
#w_data[:] = 0
#w_data[0:100] = 1
#w_data[100:300] = -1
#w_data[300:500] = 1
#w_data[500:5700] = np.tile(w_data[100:500], 13)
#w_data[5700:] = -1

# ==================================
#  Step through bicycle model
# ==================================
for i in range(t_data.shape[0]):
    x_data[i] = model.xc
    y_data[i] = model.yc
    model.step(v_data[i], w_data[i])


    
plt.axis('equal')
plt.plot(x_data, y_data)

plt.show()


# We would now like the bicycle to travel a figure eight trajectory. Both circles in the figure eight have a radius of 8m and the path should complete in 30 seconds. The path begins at the bottom of the left circle and is shown in the fig8 shape
# 

# 
# Determine the speed and steering rate inputs required to produce such trajectory and implement in the cell below. Make sure to also save your inputs into the arrays v_data and w_data, these will be used to grade your solution. The cell below also plots the trajectory generated by your own model.




sample_time = 0.01
time_end = 30
model.reset()

t_data = np.arange(0,time_end,sample_time)
x_data = np.zeros_like(t_data)
y_data = np.zeros_like(t_data)
v_data = np.zeros_like(t_data)
w_data = np.zeros_like(t_data)

# ==================================
#   solution begins here
# ==================================

v_data[:]=(16.0/15.0)*np.pi
w_data[0:100]=np.arctan(2/8)
w_data[375:375+100]=2*np.arctan(-2/8)
w_data[1875:1875+100]=2*np.arctan(2/8)

for i in range(t_data.shape[0]):
    
    x_data[i] = model.xc
    y_data[i] = model.yc
    
    model.beta=0
    model.step(v_data[i], w_data[i])
   
    
# ==================================
# solution ends here
# ==================================

plt.axis('equal')
plt.plot(x_data, y_data)
plt.show()


# We will now run your speed and angular rate inputs through our bicycle model solution. This is to ensure that your trajectory is correct along with your model. The cell below will display the path generated by our model along with some waypoints on a desired figure 8. Surrounding these waypoints are error tolerance circles with radius 1.5m, your solution will pass the grader if the trajectory generated stays within 80% of these circles.








data = np.vstack([t_data, v_data, w_data]).T
np.savetxt('figure8.txt', data, delimiter=', ')






sample_time = 0.01
time_end = 30
model.reset()

t_data = np.arange(0,time_end,sample_time)
x_data = np.zeros_like(t_data)
y_data = np.zeros_like(t_data)
v_data = np.zeros_like(t_data)
w_data = np.zeros_like(t_data)

# ==================================
#  Test various inputs here
# ==================================
for i in range(t_data.shape[0]):

    model.step(v_data[i], w_data[i])
    
plt.axis('equal')
plt.plot(x_data, y_data)
plt.show()






