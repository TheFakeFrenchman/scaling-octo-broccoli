"""

    Filters through main catalogue and clusters catalogue to find
        - Massive eliptical galaxies
        - Keeps their velocity dispersion and absolute r-band magnitude for FJ relation
        - TODO Keeps uncertainties for FJ relation
        - TODO Keep effective radius and Surface Brightness for FJ relation
        - TODO Keeps uncertainties for FP relation
        
    Puts this information within a new CSV "viable_galaxies.csv"


"""

import pandas as pd
from parseCsv import parseCsv

STELLAR_MASS_THRESHOLD_UPPER = 10.5
STELLAR_MASS_THRESHOLD_LOWER = 10
ELLIPTICAL_GALAXIES = [0, 0.5]      # Both 0 and 0.5 are elliptical galaxies

# Select only elliptical galaxies
mainCat, clusters, kinematics, morphology = parseCsv()
ellipt = morphology[morphology["type"].isin(ELLIPTICAL_GALAXIES)]
elliptIds = set(ellipt["catid"])


# Select ellpitcal galxies with certain mass
massiveGama = mainCat[
    (mainCat["mstar"] > STELLAR_MASS_THRESHOLD_LOWER)
    & (mainCat["mstar"] < STELLAR_MASS_THRESHOLD_UPPER)
    & (mainCat["catid"].isin(elliptIds))
] 

massiveCluster = clusters[
    (clusters["mstar"] > STELLAR_MASS_THRESHOLD_LOWER)
    & (clusters["mstar"] < STELLAR_MASS_THRESHOLD_UPPER)
    & (clusters["catid"].isin(elliptIds))
]

# Combine both catalogues
massiveIds = set(massiveGama["catid"]) | set(massiveCluster["catid"])



# Obtain velocity dispersion
velDispIds = kinematics[kinematics["catid"].isin(massiveIds)]

# Combines with velocity dispersion uncertainty
velDisp = pd.DataFrame({
    'catid': velDispIds["catid"], 
    'sigma_re': velDispIds["sigma_re"], 
    'sigma_re_err': velDispIds["sigma_re_err"]
    })

velDisp = velDisp.dropna()



# Obtain Absolute r-band magnitude 

# Gather list of M_r insamiDR3InputCatClusters.csv
M_rIdsCluster = clusters[clusters["catid"].isin(massiveIds)]

M_rClusterList = pd.DataFrame({
    'catid': M_rIdsCluster["catid"], 
    'M_r': M_rIdsCluster["m_r"],
    'r_e': M_rIdsCluster["r_e"],
    'mu_e': M_rIdsCluster["mu_within_1re"]
    })

M_rClusterList = M_rClusterList.dropna()


# Gather list of M_r InputCatGAMADR3.csv
M_rIdsMainCat = mainCat[mainCat["catid"].isin(massiveIds)]

M_rMainCatList = pd.DataFrame({
    'catid': M_rIdsMainCat["catid"],
    'M_r': M_rIdsMainCat["m_r"],
    'r_e': M_rIdsMainCat["r_e"],
    'mu_e': M_rIdsMainCat["mu_within_1re"]
    })

M_rMainCatList = M_rMainCatList.dropna()


# Combine both lists
M_r = pd.concat([M_rMainCatList, M_rClusterList])

# Combine velocity dispersion and Absolute r-band magnitude lists
viableGalaxies10105 = pd.merge(velDisp, M_r, how="left", on="catid")

# Delete any rows where either velocity dispersion or Absolute r-band magnitude are empty and print as a csv file
viableGalaxies10105.dropna().to_csv("code/data/viable_galaxies10105.csv", index=False)
