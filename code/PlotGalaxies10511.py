"""
    
    Plots Faber-Jackson relation (with uncertainties)
    Plots Fundamental Plane relation (TODO with uncertainties)
    
    
"""



import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import numpy as np

df = pd.read_csv("code/data/viable_galaxies10511.csv")


# FABER JACKSON

x = df["M_r"]
y = np.log10(df["sigma_re"])
yerr = np.log10(np.exp(1)) * ((df["sigma_re_err"]) / df["sigma_re"])


plt.scatter(x, y, s= 10)
#plt.errorbar(x, y, yerr=yerr, fmt='none')
plt.title('Faber–Jackson relation')
plt.xlabel('Absolute Magnitude M_r')
plt.ylabel('Log velocity dispersion σ (km/s)')
plt.gca().invert_xaxis()

#line of best fit
m, c, *_ = stats.linregress(x, y)
plt.plot(x, m*x + c, color='r')


plt.show()
print("m = ", m)

# FUNDAMENTAL PLANE - log(R_e) = a*log(σ) + b*μ_e + c

x = np.log10(df["sigma_re"])
y = df["mu_e"]
z = np.log10(df["r_e"])     # Note r_e is in arcseconds

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Plots each data point
ax.scatter(x, y, z, s=10)
ax.set_title('Fundamental Plane')
ax.set_xlabel('Log velocity dispersion log(σ)')
ax.set_ylabel('Surface brightness μ_e (Mag/arcsecond^2)')
ax.set_zlabel('Log effective radius log(R_e)')


# Finds coefficents of fundamental plane equation + plane of best fit

# Creates a matrix of x, y and ones for bist-fit for the fundamental plane equation
fundamentalPlane = np.array([x, y, np.ones(len(df))]).T

# Solve matrix via least squares to find best fit for coeffecients for fundamental plane equation
a, b, c = np.linalg.lstsq(fundamentalPlane, z)[0]


# Create 2D grid for calculating effective radius for each x, y
X = np.linspace(x.min(), x.max())
Y = np.linspace(y.min(), y.max())

X, Y = np.meshgrid(X, Y)

# Calculates predicted log effective radius at each grid position
Z = a*X + b*Y + c

ax.plot_surface(X, Y, Z, alpha=0.4)


plt.show()

print("Fundamental Plane coefficients:")
print("a =", a)
print("b =", b)
print("c =", c)