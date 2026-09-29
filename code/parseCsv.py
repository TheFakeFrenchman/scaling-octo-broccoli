import pandas as pd


def parseCsv():
    """
        Compares CSV files to determine viability of each catid
    """
    
    # Reads all csv files into seperate Dataframes
    mainCat = pd.read_csv("./data/InputCatGAMADR3.csv", index_col=0)
    clusters = pd.read_csv("./data/samiDR3InputCatClusters.csv", index_col=0)
    kinematics = pd.read_csv("./data/samiDR3StelKin.csv", index_col=0)
    morphology = pd.read_csv("./data/samiDR3VisualMorphology.csv", index_col=0)

    return mainCat, clusters, kinematics, morphology


if __name__ == "__main__":
    mainCat, clusters, kinematics, morphology = parseCsv()
    