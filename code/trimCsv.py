import pandas as pd
from parseCsv import parseCsv

# Select only elliptical galaxies
mainCat, clusters, kinematics, morphology = parseCsv()
ellipt = morphology[morphology["type"].isin([0, 0.5])]   #Both 0 and 0.5 are elliptical galaxies
elliptIds = set(ellipt["catid"])


#Select ellpitcal galxies with certain mass

#Select in GAMA catalogue
massiveGama = mainCat[(mainCat["mstar"] > 10)                    #Stellar mass stored as log value log(m_gal/m_sun)
                  & (mainCat["catid"].isin(elliptIds))] 
            
#Select in cluster catalogue
massiveCluster = clusters[(clusters["mstar"] > 10)                   
                  & (clusters["catid"].isin(elliptIds))] 
            
#Combine both catalogues
massiveIds = set(massiveGama["catid"]) | set(massiveCluster["catid"])


#Obtain velocity dispersion
velDispIds = kinematics[kinematics["catid"].isin(massiveIds)]
velDisp = velDispIds["sigma_re"].dropna()
catid = velDispIds["catid"].dropna()

velDisp = pd.DataFrame({'catid': catid, 'sigma_re': velDisp})







#Obtain Absolute r-band magnitude 

#gather list of M_r insamiDR3InputCatClusters.csv
M_rIds_cluster = clusters[clusters["catid"].isin(massiveIds)]
M_r_cluster = M_rIds_cluster["m_r"].dropna()
M_rcatid_cluster = M_rIds_cluster["catid"].dropna()

M_r_catid_cluster_list = pd.DataFrame({'catid': M_rcatid_cluster, 'M_r': M_r_cluster})


#gather list of M_r InputCatGAMADR3.csv
M_rIds_mainCat = mainCat[mainCat["catid"].isin(massiveIds)]
M_r_mainCat = M_rIds_mainCat["m_r"].dropna()
M_rcatid_mainCat = M_rIds_mainCat["catid"].dropna()

M_r_catid_mainCat_list = pd.DataFrame({'catid': M_rcatid_mainCat, 'M_r': M_r_mainCat})

M_r = pd.concat([M_r_catid_mainCat_list, M_r_catid_cluster_list]) #combine both lists

viable_galaxies = pd.merge(velDisp, M_r, how="left", on="catid") #combine velocity dispersion and Absolute r-band magnitude lists
viable_galaxies.dropna(how= 'any').to_csv("code/data/viable_galaxies.csv", index=False)    #delete any rows where either velocity dispersion or Absolute r-band magnitude are empty and print as a csv file
