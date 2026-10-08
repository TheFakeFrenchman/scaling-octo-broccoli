"""
    
    Plots Faber-Jackson relation (TODO with uncertainties)
    TODO Plots Fundamental Plane relation (TODO with uncertainties)
    
    
"""



import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


df = pd.read_csv("code/data/viable_galaxies.csv")

# FABER JACKSON

x = df["M_r"]
y = df["sigma_re"]

plt.scatter(x, y)
plt.title('Faber–Jackson relation')
plt.xlabel('Absolute Magnitude M_r')
plt.ylabel('velocity dispersion σ (km/s)')
plt.gca().invert_xaxis()

#line of best fit
m, c, *_ = stats.linregress(x, y)
plt.plot(x, m*x + c, color='r')


plt.show()


# TODO Fundamental Plane