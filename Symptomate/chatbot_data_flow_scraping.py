from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import time

symptoms = list(pd.read_csv('symptoms.csv')['Symptom'])

flow = []

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.maximize_window()

driver.get('https://symptomate.com/diagnosis/#0-66')
time.sleep(10)

try:
    cookie = driver.find_element_by_class_name('cky-btn-accept')
    driver.execute_script("arguments[0].click();", cookie)
except:
    pass

# A function to Click the Next button wherever applicable
def click_next():
    next_button = driver.find_element_by_class_name('btn-next')
    driver.execute_script("arguments[0].click();", next_button)

# Page 1
click_next()
time.sleep(3)

# Page 2
check_box = driver.find_elements_by_class_name('checkbox-label')

driver.execute_script("arguments[0].click();", check_box[0])
driver.execute_script("arguments[0].click();", check_box[1])

click_next()
time.sleep(3)

# Page 3
skip_button = driver.find_element_by_class_name('skip-question')

driver.execute_script("arguments[0].click();", skip_button)
time.sleep(3)

# Page 4
driver.execute_script("arguments[0].click();", driver.find_element_by_class_name('direct'))
time.sleep(3)

# Page 5
driver.execute_script("arguments[0].click();", driver.find_element_by_class_name('male'))
time.sleep(3)

click_next()
time.sleep(3)

# Page 6
questions = driver.find_elements_by_class_name('buttons')
for question in questions[:-1]:
    question.click()

click_next()
time.sleep(1)

# Take Random 3 Symptoms From the CSV
count = 0
symptoms_list = []
while count < 3:
    symptoms_list.append(random.choice(symptoms))
    count += 1

print(symptoms_list,"\n")

# Page 7
search_box = driver.find_element_by_class_name('evidence-search-input')

for i in symptoms_list:
    flow.append(i)
    search_box.clear()
    search_box.send_keys(i)
    time.sleep(1)
    search_box.send_keys(Keys.DOWN)
    time.sleep(0.5)
    search_box.send_keys(Keys.RETURN)
    time.sleep(0.5)

click_next()
time.sleep(3)

# Page 8
map = driver.find_element_by_css_selector('path.IN')
map.click()
time.sleep(3)

click_next()

time.sleep(10)

# QnA starts Here
print("---------------------------------------------------\n")

while True:
    question = driver.find_element_by_class_name('question-text').text
    choices = driver.find_element_by_class_name('answers-box').text
    choices = choices.split("\n")

    choices = ",".join(choices[:-1])

    print(question)
    print(choices)

    flow.append(question)
    flow.append(choices)

    print("\nWaitng For Input")

    # Manually Select the Option / and Go the next Question and then Press enter when Done
    # Input -1 When The Result Page Appears
    x = input("Press Enter For Next Question, Press -1 to break ")
    time.sleep(2)

    print("Next Question, \n")

    if x == '-1':
        break

print("--------------------------------------------------------\n")

# Get the Conditions From the Result Page
try:
    conditions = driver.find_elements_by_class_name('condition-item')

    for condition in conditions:
        flow.append(condition.text.split("\n")[0])
        flow.append(condition.text.split("\n")[1])
        print(condition.text.split("\n")[0])
        print(condition.text.split("\n")[1])
except Exception as e:
    print(e)

driver.quit()

# Convert to CSV
dic = {"Flow" : flow }
df = pd.DataFrame(dic)

df.to_csv("test.csv")
