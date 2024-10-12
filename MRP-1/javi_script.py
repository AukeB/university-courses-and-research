"""This program helps to fit the flare model of Davenport et al (2014) to dataobtained with MASCARA. The main parameters to fit the data are the t0, time at which the flux reaches half of the maximum of the flare; and dt_half, how long takes for the flare to decay to half of the maximum flux. Use it under your own risk."""

# Imports
import numpy as np
import matplotlib.pyplot as plt

# Flux and time files
flux_file='/home/bruinsma/Desktop/lsreduce-2017.6/flux_arr_20180308.npy'
time_file='/home/bruinsma/Desktop/lsreduce-2017.6/time_arr_20180308.npy'
flux= np.load(flux_file)
time= np.load(time_file)

# Functions for the model
F0 = lambda x: 0*x
F1 = lambda x: (1 + 1.941*x - 0.175*x**2 - 2.246*x**3 - 1.125*x**4)
F2 = lambda x: (0.6890 * np.exp(-1.600 * x) + 0.3030 * np.exp(-0.2783 * x))

#time at which the functions will be evaluated in resolution of 0.001 
#as said in the paper
X0 = np.linspace(-47, -1, num=46001)
X1 = np.linspace(-1, 0, num=1001)
X2 = np.linspace(0,20, num=20001)

#X0 = np.linspace(-170, -151, num=19001)
#X1 = np.linspace(-151, -145.5, num=6501)
#X2 = np.linspace(-145.5,-125.5, num=20001)

# The model: the factor is how much increments the relative flux with 
# respect to the quiscent phase during the flare
factor=3.0
Ftot=np.concatenate([F0(X0),F1(X1),F2(X2)])*factor
Xtot=np.concatenate([X0,X1,X2])

#Fitting a cuadratic polinomia to the continous (rejecting the areas with no 
#or flare)
time3=time[time > 8]
flux3=flux[time > 8]
#time3=time2[flux2 < 900]
#flux3=flux2[flux2 < 900]
p=np.polyfit(time3,flux3,2)
fit=np.polyval(p,time)

#Coverting the time as in t1/2, i.e., the time at which the flare reach half of
# its maximum flux. Thus for fitting you have to adjust t0 and dt_thalf.
t0=8.34
dt_half=0.041
binn=flux*0.
timedt=(time-t0)/dt_half
for i in range(0,101):
    binn[i]=np.mean(Ftot[(Xtot > timedt[i]) & (Xtot < timedt[i+1])])

plt.axis([-20,20,-0.2,1.5]) #axis limits
plt.plot(timedt,flux/fit - 1., timedt, binn) # data in t1/2 and binned model
#plt.plot(time,flux)
plt.show(); plt.close();