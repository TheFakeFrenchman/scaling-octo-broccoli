"""

File for comparing information in each CSV

"""

from parseCsv import parseCsv

mainCat, clusters, kinematics, morphology = parseCsv()

# Overview of total catids
print("Catalogue size - Unique catids:")
print("Main catalogue:", len(mainCat), " - ", mainCat["catid"].nunique())
print("Clusters:", len(clusters), " - ", clusters["catid"].nunique())
print("Kinematics:", len(kinematics), " - ", kinematics["catid"].nunique())
print("Morphology:", len(morphology), " - ", morphology["catid"].nunique())


# Set of all catids within each CSV
mainIds = set(mainCat["catid"])
clusterIds = set(clusters["catid"])
kinematicsIds = set(kinematics["catid"])
morphologyIds = set(morphology["catid"])


# How catids are shared amongst CSVs
print()
print("Shared catids:")
print("Main - Clusters:", len(mainIds & clusterIds))
print("Main - Kinematics:", len(mainIds & kinematicsIds))
print("Main - Morphology:", len(mainIds & morphologyIds))
print("Clusters - Kinematics:", len(clusterIds & kinematicsIds))
print("Clusters - Morphology:", len(clusterIds & morphologyIds))
print("Kinematics - Morphology:", len(kinematicsIds & morphologyIds))


# Valuable information within kinematics CSV
print()
print("Kinematics CSV:")

print("Total catids", len(kinematicsIds))
print("Total catids with valid sigma_re:", 
    kinematics.groupby("catid")      # Group each galaxy entry by catid,
    ["sigma_re"]                     # look at velocity dispersion             
    .first()                         # Pick first NaN entry
    .notna()                         # Verify not NaN
    .sum()                           #
    )                                      

mainKin = kinematics[kinematics["catid"].isin(mainIds)]
clusterKin = kinematics[kinematics["catid"].isin(clusterIds)]

print("Main catalogue with valid sigma_re:", 
    mainKin.groupby("catid")
    ["sigma_re"]
    .first()
    .notna()
    .sum()
    )

print("Cluster catalogue with valid sigma_re:", 
    clusterKin.groupby("catid")
    ["sigma_re"]
    .first()
    .notna()
    .sum()
    )
