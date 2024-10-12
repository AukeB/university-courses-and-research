# Imports
import numpy as np

# Radiation pressure.
def P_rad(T):
    return 1/3 * a * T**4

# Ideal gas.
def P_ig(T,rho,mu):
    return (1 / mu) * (rho / m_u) * k_b * T

# Degenerate, non-relativistic.
def P_NR(rho):
    return K_NR * (rho / m_e)**(5/3)

# Degenerate, relativistic.
def P_ER(rho):
    return K_ER * (rho / m_e)**(4/3)

# Mean molecular weight functions.

# mu_e
def func_mu_e(X):
    return 2 / (1+X)

# mu
def func_mu(X,Y,Z):
    value = 2*X + (3/4)*Y + (1/2)*Z
    return 1/value

# Tempature as function of density functions.
def rad_ig(rho,mu):
    return 3.2e7 * mu**(-1/3) * rho**(1/3)

def ig_NR(rho,mu,mu_e):
    return 1.21e5 * mu * mu_e**(-5/3) * rho**(2/3)

def NR_ER(rho,mu_e):
    return 9.7e5 * mu_e

def ig_ER(rho,mu,mu_e):
    return 1.50e7 * mu * mu_e * rho**(1/3)

# Mean molecular weights
X = 0.7
Y = 0.28
Z = 0.02

mu_e = func_mu_e(X)
mu = func_mu(X,Y,Z)

# Variables
log_rho = np.linspace(-10,10,1000)
rho = 10**log_rho

# Boundary lines
T_rad_ig = rad_ig(rho,mu)
T_ig_NR = ig_NR(rho,mu,mu_e)
T_NR_ER = NR_ER(rho,mu_e)
T_ig_ER = ig_ER(rho,mu,mu_e)

T_NR_ER = np.linspace(T_NR_ER,T_NR_ER,len(rho)) # Because vertical boundary line.

# Boundaries for in the plot (manually set).
b1 = 940
b2 = 840
b3 = 840
