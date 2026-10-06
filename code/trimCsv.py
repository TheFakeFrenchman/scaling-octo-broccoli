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

velDisp.to_csv("code/data/viable_galaxies.csv", index=False)



