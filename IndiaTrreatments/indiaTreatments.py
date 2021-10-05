from bs4 import BeautifulSoup
import requests
link = 'https://www.indiatreatments.com/cost-of-treatments.php'
source = requests.get(link).text

soup = BeautifulSoup(source, 'lxml')
for article in soup.find_all('li', class_='has-title'):
  
  for i in article.find_all('tr', class_='head'):
    string=i.text
    string1=string.splitlines( )
    print(string1[4])
