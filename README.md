# imofind
## Finding outliers on house rental website

![imofind](https://user-images.githubusercontent.com/51707272/154373256-6f167cf8-1f2e-40af-bb05-d496513e4e2a.jpg)


Finding a good deal on a house might be difficult. Also, fraudulent posts often appear as "too good to be true", where a good house is cheaper than normal for a given 
location and size. These scripts extracts links for houses that are lower outliers for each municipality and type in Portugal.

It's divided in two files, data_fetch and find_outliers. 

The final output is a csv with all the links for the ouliers.

To get the final csv with the "hot" links, open the directory where the files are located and type in the terminal:

$ python3 data_fetch.py

After, type:

$ python3 find_outliers.py





