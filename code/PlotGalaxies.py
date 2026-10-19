"""
    
    Plots Faber-Jackson relation (with uncertainties)
    Plots Fundamental Plane relation
    
    
"""



import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import numpy as np


df = pd.read_csv("code/data/viable_galaxies.csv")


# FABER JACKSON (OLD)

x = df["M_r"]
y = np.log10(df["sigma_re"])
yerr = np.log10(np.exp(1)) * ((df["sigma_re_err"]) / df["sigma_re"])


plt.scatter(x, y, s= 10)
plt.errorbar(x, y, yerr=yerr, fmt='none')
plt.title('Faber–Jackson relation')
plt.xlabel('Absolute Magnitude M_r')
plt.ylabel('Log velocity dispersion σ (km/s)')
plt.gca().invert_xaxis()

#line of best fit
m, c, *_ = stats.linregress(x, y)
plt.plot(x, m*x + c, color='r')
print('gradient of', m, "giving a FJ power relation of", -0.4 / m)

plt.show()



# FABER JACKSON (FOR 4 DIFFERENT STELLAR MASSES)

datasets = [
    ("code/data/viable_galaxies910.csv",   "9 < log(M*) < 10",    "red"),
    ("code/data/viable_galaxies10105.csv", "10 < log(M*) < 10.5", "orange"),
    ("code/data/viable_galaxies10511.csv", "10.5 < log(M*) < 11", "green"),
    ("code/data/viable_galaxies1115.csv",  "11 < log(M*) < 11.5", "blue")
]

plt.figure(figsize=(12, 8))

for file, label, colour in datasets:

    df = pd.read_csv(file)

    x = df["M_r"]
    y = np.log10(df["sigma_re"])
    yerr = np.log10(np.exp(1)) * ((df["sigma_re_err"]) / df["sigma_re"])

    # Plot galaxy points
    plt.scatter(x, y, s=12, color=colour, label=label)
    plt.errorbar(x, y, yerr=yerr, fmt='none', ecolor=colour)

    m, c, *_ = stats.linregress(x, y)

    x_fit = np.linspace(x.min(), x.max(), 100)
    plt.plot(x, m*x + c, color=colour, linewidth=2)
    print('gradient of', m, "giving a FJ power relation of", -0.4 / m)



plt.title("Faber–Jackson Relation Across Stellar Mass Ranges")
plt.xlabel("Absolute Magnitude M_r")
plt.ylabel("Log Velocity Dispersion σ (km/s)")
plt.gca().invert_xaxis()
plt.legend()


plt.show()




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
ax.set_zlabel('Log effective angular radius log(R_e)')


### Finds coefficents of fundamental plane equation + plane of best fit

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