# imofind
Finding outliers on house rental website



Finding a good deal on a house might be difficult. Also, fraudulent posts often appear as "too good to be true", where a good house is cheaper than normal for a given 
location and size. This scripts extracts links for houses that are lower outliers for each municipality and type in Portugal.

It's divided in two files, data_fetch and find_outliers. 

The final output is a csv with all the links for the ouliers.

To get the csv, open the directory where the files are located and type in the terminal:

$ python data_fetch.py or $ python3 data_fetch.py

After, type:

$ python find_outliers.py






