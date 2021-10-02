from bs4 import BeautifulSoup
import requests
import csv

liist = ['urologist','orthopaedist','paediatrician','physiotherapist','sexologist','trichologist','ophthalmologist','dentist','psychiatrist','gastroenterologist','endocrinologist','neurologist','rheumatologist','cardiologist','oncologist','nephrologist'];

for i in range(len(liist)):
  link = f'https://www.cult.fit/care/doctor-consultation/{liist[i]}'
  source = requests.get(link).text
  soup = BeautifulSoup(source, 'lxml')
  csv_file = open('cultfit.csv', 'w')  
  csv_writer = csv.writer(csv_file)
  csv_writer.writerow(['name', 'exp_deg', 'next_avail', 'fees', 'profile_link'])  
  for article in soup.find_all('div', class_="care-doctor-listing-item false"):
    name = article.find('div', class_="css-43mi9w-EllipsesTextDiv e1cd6s610").text
    exp_deg = article.find('div', class_="css-1ef1uxb-EllipsesTextDiv e1cd6s610").text
    next_avail = article.find('div', class_="css-pasf6i-EllipsesTextDiv e1cd6s610").text
    fees = article.find('div', class_="css-1550myk-PriceBlockDiv e6rah60").text
    profile_link = article.find('a', class_="css-41m9h2-Anchor e1xz8vz90")['href']
    csv_writer.writerow([name, exp_deg, next_avail, fees, profile_link])    

csv_file.close()
