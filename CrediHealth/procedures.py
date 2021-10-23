from selenium import webdriver
import time
import csv
import pandas as pd
import requests
import bs4
from csv import writer
from csv import reader

driver = webdriver.Chrome(r'C:\Users\conta\chromedriver.exe')
driver.get('https://www.credihealth.com/procedure/india')
details_list = []
file_to_output = open('Procedure Task.csv' , mode = 'a' , newline = '')
csv_writer = csv.writer(file_to_output)
csv_writer.writerow(['Procedure Type' , 'Function' , 'Names', 'Pain intensity', 'Procedure Duration' , 'Hospital Days' , 'Anesthesia Type','Estimated National Average','For Credihealth Users','Procedure Name'  ])
file_to_output.close()
list_list_1 = []
list_list = []
driver.maximize_window()
list_list_2 = []
list_list_3 = []


def add_column_in_csv(input_file, output_file, transform_row):
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)
        for row in csv_reader:
            transform_row(row, csv_reader.line_num)
            csv_writer.writerow(row)

for i in range(1,31):
    try :
        element = driver.find_element_by_xpath(f'/html/body/div[5]/section[1]/div[2]/div/a[{i}]')
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(2)
        element.click()
        time.sleep(2)
        result = requests.get(driver.current_url)
        code = bs4.BeautifulSoup(result.text , 'lxml')
        list_list_2.append(code.select('p.color-green')[0].getText())
        list_list_3.append(code.select('p.color-green')[1].getText())

        details_list = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/div[1]/div[3]').text
        final_list = list(details_list.split("●"))
        for j in final_list:
            final_list1 = j.split(':')
            try:
                list_list.append(final_list1[1])
            except:
                pass
        list_list = list_list + list_list_2 + list_list_3
        file_to_output = open('Procedure Task.csv', mode='a', newline='')
        csv_writer = csv.writer(file_to_output)
        csv_writer.writerow(list_list)
        file_to_output.close()
        list_list.clear()
        list_list_1.clear()
        list_list_2.clear()
        list_list_3.clear()
        driver.back()
        time.sleep(2)

    except:
        print(f'There was some error with the procedure on number {i}')
        driver.back()


