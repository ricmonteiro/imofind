# We're going to fetch data from the website
# using beautifulsoup, requests and pandas

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

imo = requests.get('https://www.imovirtual.com/arrendar/apartamento/') # request http
raw_html = imo.text # convert webpage code into raw text
soup = bs(raw_html, features='lxml') # soupify page text

# find number of pages
for i in soup.find_all('ul', class_='pager'):
    pages = int(i.text.split()[-1])
    
# initialize url list with first page for subsequent appending 
urls = ['https://www.imovirtual.com/arrendar/apartamento/'] 

# append further pages links
for page in range(2,pages+1):
    urls.append('https://www.imovirtual.com/arrendar/apartamento/?page=' + str(page))
    
# initialize lists for house prices, types, locations and sizes. We'll also store links
prices = []
types = []
location = []
sizes = [] 
links = []

print(" Website accessed, extracting data... (this might take a few minutes) ")

for u in urls:
    imo = requests.get(u) # request http
    raw_html = imo.text # convert webpage code into raw text
    soup = bs(raw_html, features='lxml') # soupify page text

    # Find the desired data: price, location (concelho), typology and size (m2)

    # price
    for price in soup.find_all('li', class_="offer-item-price"): 
        prices.append(price.string.split('€')[0].replace(' ','').strip())


    #type 
    for ty in soup.find_all('li', class_="offer-item-rooms hidden-xs"):
        types.append(ty.string)

    #location
    for loc in soup.find_all('p', class_="text-nowrap"):
        location.append(loc.text.split('Apartamento para arrendar: ')[1])

    #size (m2)
    for size in soup.find_all('li', class_="hidden-xs offer-item-area"):
        sizes.append(size.next.split(' ')[0]) 
        
    for link in soup.find_all('header', class_="offer-item-header"):
        links.append(link.a['href'])

print(" Data extracted successfully. Cleaning and creating file... ")

all_houses = [] # list where all houses will be
all_houses.append([prices, types, location, sizes, links])
columns = ['price','type','location','size','link'] # columns names for the dataframe
all_data = pd.DataFrame(all_houses[0]) # create datafame with the list created
all_data = all_data.transpose() # transpose dataframe
all_data.columns = columns # rename dataframe columns
all_data = all_data.drop_duplicates() # drop duplicate columns
all_data = all_data[all_data['price'] != 'Preçosobconsulta'] # drop houses with negotiable prices

# replace house types with numeric values       
type_dict = {'T2':2, 'T3':3, 'T1':1, 'T4':4, 'T0':0, 'T5':5, 'T6':6, 'T8':8, 'T7':7, 'T10 ou superior':10, 'T9':9}
all_data['type'] = all_data['type'].replace(type_dict)

# split location into municipality and district columns
municipality = []
district = []
for i in all_data.location.str.split(', '):
    try:
        municipality.append(i[-2])
    except:
        municipality.append(i[-1])     
    try:
        district.append(i[-1])
    except:
        district.append('')

all_data['municipality'] = municipality
all_data['district'] = district
all_data = all_data.drop(columns='location', axis=1)

# change size column to float and price to int
all_data['size'] = all_data['size'].replace(',','.', regex=True).astype('float')
all_data['price'] = all_data['price'].replace(',','.', regex=True).astype('float').round().astype('int')

# reset index to match number of posts
all_data = all_data.reset_index()

# save data to local csv file
all_data.to_csv('house_data.csv', index=False)
print(" All done! File created sucessfully! Search for house_data.csv in your directory. ")