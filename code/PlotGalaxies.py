"""
    
    Plots Faber-Jackson relation (with uncertainties)
    TODO Plots Fundamental Plane relation (TODO with uncertainties)
    
    
"""



import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


df = pd.read_csv("code/data/viable_galaxies.csv")

# FABER JACKSON

x = df["M_r"]
y = df["sigma_re"]
yerr = df['sigma_re_err']


plt.scatter(x, y, s= 10)
plt.errorbar(x, y, yerr= yerr, fmt= 'none')
plt.title('Faber–Jackson relation')
plt.xlabel('Absolute Magnitude M_r')
plt.ylabel('velocity dispersion σ (km/s)')
plt.gca().invert_xaxis()

#line of best fit
m, c, *_ = stats.linregress(x, y)
plt.plot(x, m*x + c, color='r')


plt.show()


# TODO Fundamental Plane