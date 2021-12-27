import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}
medicinelist=[]
def getMedicine(category_name, page):
    url = 'https://www.netmeds.com/non-prescriptions/ayush/page/{page}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    medicines = soup.find_all('div', {'class':'col-md-3 padding-none'})
    for item in medicines:
        medicine= {
        'title' : item.find('span', {'class':'clsgetname'}).text,
        'link' : 'https://www.netmeds.com' + item.find('a', {'class':'category_name'})['href'],
        'manuf' : item.find('span', {'class':'drug-varients ellipsis'}).text,
        'price' : item.find('span', {'id':'final_price'}).text,
        }
        medicinelist.append(medicine)
    return
for x in range(1,666):
    getMedicine('category_name', x)
df = pd.DataFrame(medicinelist)  
print(df) 
df.to_excel('netmed_ayush_category_data.xlsx')
print('Done. The End')
