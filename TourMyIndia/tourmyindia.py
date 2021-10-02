import requests, time, csv
from bs4 import BeautifulSoup
base_url = 'https://www.tourmyindia.com'

csv_keys = ['Speciality', 'Name of Procedure', 'Min Days', 'Max Days', 'Min Cost', 'Max Cost', 'Currency', 'Link', 'Time Duration', 'Procedure/Treatment Details', 'Factors Affecting Cost']
csv_file = open('tourMyIndia.csv', 'a', newline="")
writer = csv.DictWriter(csv_file, fieldnames=csv_keys)
writer.writeheader()

def makeReq(url):
  # send soup object
  req = requests.get(base_url + url)
  soup = BeautifulSoup(req.content, 'lxml')
  return soup

def getAllLinks(url):
  # send link for all specialities
  soup = makeReq(url)
  headers = soup.find('div', class_='header-left navbar').find_all('div', class_='dropdown')
  links = [{head.button.text : [[a.text.strip(), a.get('href')] for a in head.find('div',class_='row').find_all('a')]} for head in headers]
  return links

def getMaxPrice(soup):
  # returns max price
  spans = soup.find('div', class_='procedures-banner-inner-st')
  price = [int(span.text[1:].strip()) for span in spans.find_all('span', class_='price')]
  return max(price)

def otherData(data, index):
  for spec, procedures in data.items():
    for value in procedures[index:]:
      print(f'def_index:- {index}')
      index += 1
      csv_data, soup = {}, makeReq(value[1])
      procedureDiv = soup.find('div', {"class":"total-days-procedures-main"}).find_all('div', {"class":"days-procedures-list"})
      if len(procedureDiv) < 2:
        # if maximum and minimum days are not available then skip this round
        continue
      minDay = procedureDiv[0].find('span').text
      maxDay = procedureDiv[1].find('span').text
      timeDuration = procedureDiv[2].find('span').text if len(procedureDiv)==3 else ''
      minCost = soup.find('div', class_='cost-banner').h2.span.next_sibling.split()
      currency = minCost[0]
      minCost = minCost[1]
      maxCost = getMaxPrice(soup)
      csv_data.update({'Speciality':spec, 'Name of Procedure':value[0], 'Min Days':minDay, 'Max Days':maxDay, 'Min Cost':minCost, 'Max Cost':maxCost, 'Currency':currency, 'Time Duration':timeDuration, 'Link': base_url+value[1]})
      writer.writerow(csv_data)
      time.sleep(2)

allLinks = getAllLinks('/medical-tourism/treatment/ankle-fusion-surgery')

# this indexes are used to resume executing of script from the point script stopped executing
def_index, for_index = 0, 7

for link in allLinks[for_index:]:
    # printing these indexes to resume executing of script from the point script stopped executing
    print(f'\nfor_index:- {for_index}\tdef_index:- {def_index}')
    otherData(link, def_index)
    def_index = 0
    for_index += 1
