import pandas as pd
import numpy as np
from iteration_utilities import deepflatten

print(" Loading file... ")
try:
    house_data = pd.read_csv('house_data.csv', index_col=0)
except:
    print("Error, file not found. Please run \"python data_fetch.py")




print(" File loaded successfully! Detecting outliers... ")
# FUNCTION THAT WILL EXTRACT OUTLIERS FROM PRICE LIST
def detect_outliers(data):
    
    # find q1 and q3 values
    q1, q3 = np.percentile(sorted(data), [25, 75])
    # compute IRQ
    iqr = q3 - q1
    # find lower and upper bounds
    lower_bound = q1 - (2 * iqr)

    outliers = [x for x in data if x <= lower_bound]       

    return outliers


# cycle through each municipality and each house type and extract outlier indexes
outlier_indexes = [] #
for mun in house_data.municipality.unique():
    for t in house_data.type.unique():
        
        prices = house_data.price[(house_data.municipality == mun) & (house_data.type == t)].to_list()
        
        # pass if there are no house for rent in a municipality and type
        if prices != []:                
            data_outliers = detect_outliers(prices)
        else:
            pass
        
        # pass if there are no outliers in the price
        if data_outliers == []:
            pass
        
        else:
            for o in data_outliers:
                indexes = house_data.index[(house_data.municipality == mun) 
                                           & (house_data.type == t) 
                                           & (house_data.price == o)].to_list()          
        
                outlier_indexes.append(indexes)

# flatten the list to get a one-dimensional list   
outlier_indexes = list(deepflatten(outlier_indexes, depth=1))

# transform list in a dataframe and reset index
outlier_links = pd.DataFrame(house_data.link[outlier_indexes])
outlier_links = outlier_links.reset_index(drop=True)

print(" All outliers have been extracted! Saving file...")
# create csv with links
outlier_links.to_csv('outlier_links.csv')

print(" File saved successfully! Look for outlier_links.csv in your directory. ")