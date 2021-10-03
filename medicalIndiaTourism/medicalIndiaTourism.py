import requests, time, csv
from bs4 import BeautifulSoup

csv_keys = ['Speciality', 'Name of Procedure', 'Min Days', 'Max Days', 'Min Cost', 'Max Cost', 'Currency', 'Link']
csv_file = open('medicalTourism.csv', 'a', newline="")
writer = csv.DictWriter(csv_file, fieldnames=csv_keys)
writer.writeheader()

link_file = open('medicaltourindialinks.csv', 'r')
links = [link for r in csv.reader(link_file) for link in r][1:]

def makeReq(url):
  # send soup object
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'lxml')
  return soup

def formatData(value):
  return value.replace('\r','').replace('\n','').replace('\t','').replace('/', '')

# def getCsvData(soup):
for link in links:
  soup = makeReq(link)
  # table_data = []
  # for tr in soup.find('table').find_all('tr'):
  #   rows = tr.find_all('td')
  #   if rows is not None and len(rows) >=3:
  #     columns = []
  #     for td in rows:
  #       columns.append(formatData(td.text))
  #     table_data.append(columns)

  table_data = [[formatData(td.text) for td in tr.find_all('td')] for tr in soup.find('table').find_all('tr') if tr.find_all('td') is not None and len(tr.find_all('td')) >= 3]
  for td in table_data:
    # initializing every key with empty string
    csv_data = {head:'' for head in csv_keys}
    # giving values to keys whose data is available to us
    csv_data.update({'Name of Procedure':td[0], 'Min Days':td[1], 'Min Cost':td[2], 'Currency':'USD', 'Link':link, 'Speciality':formatData(link[55:]).replace('-', ' ')})
    writer.writerow(csv_data)
  time.sleep(2)
