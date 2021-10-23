from selenium import webdriver
from selenium.common.exceptions import JavascriptException

from bs4 import BeautifulSoup
import time, csv, requests

hosp_csv = open('hosps.csv', 'a', newline="")
hosp_fieldnames = ['id', 'name', 'description', 'speciality_type', "capacity", "address", 'link']
hosp_writer = csv.DictWriter(hosp_csv, fieldnames=hosp_fieldnames)
# hosp_writer.writeheader()

doc_csv = open('docs.csv', 'a', newline="")
doc_fieldnames = ['hosp_id', 'link']
doc_writer = csv.DictWriter(doc_csv, fieldnames=doc_fieldnames)
# doc_writer.writeheader()

doctors_csv = open('./doctor_Details2.csv', 'a', newline='')
doctors_fieldnames = ['id', 'hosp_id', 'name', 'description', 'speciality', "education", "procedure",
                  'expreince details', 'experience', 'link']
doctors_writer = csv.DictWriter(doctors_csv, fieldnames=doctors_fieldnames)
# doctors_writer.writeheader()

base_url = 'https://www.credihealth.com'
driver = webdriver.Chrome('chromedriver.exe')
driver.set_window_size(width=1150, height=1000)
# driver.get(base_url + '/hospital/jaslok-hospital-mumbai/doctors')
# driver.get(base_url + '/hospital/medicover-hospitals-kurnool/doctors')


def get_hosp_info(url, id):
    req = requests.get(url).content
    soup = BeautifulSoup(req, 'lxml')
    name = soup.find('h1', class_='fs-20 fw-500 margin-0 margin-b10 color-black')
    addr = name.findNextSibling().text.strip() if name is not None else ''
    # name.findChild
    name = name.text.strip() if name is not None else ''


    speciality, capacity = '', ''
    special_div = soup.find('div', class_='hospital-information-section')
    special_div = special_div.find('div', class_='fw-500 display-flex space-between margin-b10 flex-wrap fs-16') if special_div is not None else special_div

    span = special_div.find_all('span') if special_div is not None else special_div
    description = soup.find('div', id='d_all')
    description = description.text.strip() if description is not None else ''
    if span is not None and len(span) >= 2:
        speciality, capacity = span[0].text, span[1].text
    hosp_writer.writerow({'speciality_type': speciality, 'capacity': capacity, 'name': name, 'address': addr, 'description': description, 'link': url, 'id': id})

def load_docs(def_page = 1):
    driver.execute_script("""document.querySelector("#show_more_doctors").click()""")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    page = int(soup.find('a', id='show_more_doctors').get('page'))
    if page != def_page:
        def_page = page
        load_docs(def_page)
    else:
        divs = soup.find('div', {'id': 'speciality_doctors'})
        docs = divs.findChildren('div', recursive=False)
        # print(docs)
        doc_links = [a.find('a').get('href').replace('/feedback', '') for a in docs if a.find("a") is not None]
        for link in doc_links:
            doc_writer.writerow({'link': link, 'hosp_id': id})
        print(page)
        return page

def format_data(string):
    return string.strip().replace('\u200b', '').replace('\u2011', '').replace('\u2010', '')

def makeReq(url):
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'lxml')
  return soup

def getDoctorsDetails(links, id):
    url = base_url + links[1]
    nav = makeReq(url)
    name = nav.find('h1', class_='fs-18 fw-500 margin-0 margin-b10 color-black')
    if name is not None:
        name = name.text.strip()
        special = nav.find('p', class_='margin-0 margin-b10')
        expr = nav.find('span', class_='experince')
        description = nav.find('div', id='d_all')
        education_detail = nav.find('div', id='headingOne')
        expr_details = nav.find('div', id='collapseTwo')
        expr_details = expr_details.findChild().findChildren('div', recursive=False) if expr_details is not None else ''
        procedure = nav.find('div', class_='doctors-procedure')
        procedure = procedure.find_all('p') if procedure is not None else ''
        procedure = [format_data(p.text) for p in procedure if p != '']

        doctors = {
            'id' :id, 'hosp_id': links[0], 'name': format_data(name), 'description': format_data(description.text), 'speciality': format_data(special.text),
            'experience': format_data(expr.text), 'link': url, "procedure": (procedure),
            "education": [format_data(p.text) for p in education_detail.find_all('p') if p is not None],
            'expreince details': [format_data(p.text) for p in expr_details if p is not None]
        }
        doctors_writer.writerow(doctors)
        # print(f'{name}\n{special.text}\n{expr.text}\n{description.text}\n')
    else:
        print('Sleeping for 60 Secs')
        time.sleep(60)
        getDoctorsDetails(links, id)

# Call it after scrapping all hospitals and when you got links for each doctor
def scrape_doctors():

    with open('docs.csv', 'r') as file:
      id = 1
      for i in [link for link in csv.reader(file)][id:255]:
        print(id, i[1])
        getDoctorsDetails(i, id)
        id+=1
        time.sleep(2)

# call it when you want to get link for all doctors.
def get_doctors_link():
    with open('all_hospitals_formatted.csv', 'r') as file:
        id = 1
        hospitals = [link for link in file]
        for link in hospitals[id-1:]:
            get_hosp_info(base_url + link, id)
            try:
                driver.get(base_url + link.replace('overview', 'doctors'))
                load_docs()
            except JavascriptException:
                time.sleep(60)
                driver.get(base_url + link.replace('overview', 'doctors'))
                load_docs()
            print(f'id:- {id}')
            id+=1
            time.sleep(5)
            # break

# scrapping all doctors into a csv file
scrape_doctors()
driver.close()
