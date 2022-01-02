from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import time

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.maximize_window()
start = time.time()

symptoms = list(pd.read_csv('symptoms.csv')['Symptom'])

flow = []


# A function to Click the Next button wherever applicable
def click_next():
    next_button = driver.find_element_by_class_name('btn-next')
    driver.execute_script("arguments[0].click();", next_button)


def checkbox():
    question = driver.find_element_by_class_name('question-text').text
    print(question)
    flow.append(question)

    Os = option_block.find_elements_by_class_name('checkbox-label')
    options = ", ".join([O.text for O in Os])
    print(options)
    flow.append(options)

    option_block.find_elements_by_class_name('checkbox-label')[0].click()
    answer = option_block.find_elements_by_class_name('checkbox-label')[0].text
    print(answer, "\n")
    flow.append(answer)

    time.sleep(1)
    click_next()
    time.sleep(2)

def radio():
    question = driver.find_element_by_class_name('question-text').text
    print(question)

    Os = option_block.find_elements_by_class_name('radio-label')
    options = ", ".join([O.text for O in Os])
    print(options)

    option_block.find_elements_by_class_name('radio-label')[0].click()
    answer = option_block.find_elements_by_class_name('radio-label')[0].text
    print(answer, "\n")

    flow.append(question)
    flow.append(options)
    flow.append(answer)

    time.sleep(1)
    click_next()
    time.sleep(2)

def multiple():
    subs = option_block.find_elements_by_class_name('question-item')
    main_q = driver.find_element_by_class_name('question-text').text

    for sub in subs:
        question = main_q + " " + sub.find_element_by_class_name('name').text
        print(question)

        options = ", ".join(sub.find_element_by_class_name('buttons').text.split("\n"))
        print(options)

        sub.find_element_by_class_name('buttons').find_element_by_class_name('radio-label').click()
        answer = sub.find_element_by_class_name('buttons').find_element_by_class_name('radio-label').text
        print(answer, "\n")

        flow.append(question)
        flow.append(options)
        flow.append(answer)

    time.sleep(1)
    click_next()
    time.sleep(2)

def buttons():
    question = driver.find_element_by_class_name('question-text').text
    print(question)

    Os = option_block.find_elements_by_class_name('btn-answer')
    options = ", ".join([O.text for O in Os])
    print(options)

    option_block.find_elements_by_class_name('btn-answer')[0].click()
    answer = option_block.find_elements_by_class_name('btn-answer')[0].text
    print(answer, "\n")

    flow.append(question)
    flow.append(options)
    flow.append(answer)
    time.sleep(2)

def scale():
    question = driver.find_element_by_class_name('question-text').text
    print(question)

    options = "Range 1 - 10 (Mild to Unbearable)"
    print(options)

    answer = "5"
    print(answer, "\n")

    flow.append(question)
    flow.append(options)
    flow.append(answer)

    try:
        option_block.find_element_by_class_name('scale-square-5').click()
    except:
        pass

    time.sleep(1)
    click_next()
    time.sleep(2)

for _ in range(2):
    driver.get('https://symptomate.com/diagnosis')
    time.sleep(5)

    try:
        cookie = driver.find_element_by_class_name('cky-btn-accept')
        driver.execute_script("arguments[0].click();", cookie)
    except: pass

    # Page 1
    click_next()
    time.sleep(1)

    # Page 2
    check_box = driver.find_elements_by_class_name('checkbox-label')

    driver.execute_script("arguments[0].click();", check_box[0])
    driver.execute_script("arguments[0].click();", check_box[1])

    click_next()
    time.sleep(1)

    # Page 3
    skip_button = driver.find_element_by_class_name('skip-question')

    driver.execute_script("arguments[0].click();", skip_button)
    time.sleep(1)

    # Page 4
    driver.execute_script("arguments[0].click();", driver.find_element_by_class_name('direct'))
    time.sleep(1)

    # Page 5
    driver.execute_script("arguments[0].click();", driver.find_element_by_class_name('male'))
    time.sleep(1)

    click_next()
    time.sleep(1)

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

    # Page 7
    search_box = driver.find_element_by_class_name('evidence-search-input')

    for i in symptoms_list:
        search_box.clear()
        search_box.send_keys(i)
        time.sleep(2)
        search_box.send_keys(Keys.DOWN)
        time.sleep(0.5)
        search_box.send_keys(Keys.RETURN)
        time.sleep(0.5)

    symps = driver.find_element_by_class_name('evidence-list').text.split("\n")
    symps.extend((3 - len(symps))*" ")

    for symp in symps:
        flow.append(symp)

    click_next()
    time.sleep(1)

    # Page 8
    map = driver.find_element_by_css_selector('path.IN')
    map.click()
    time.sleep(1)
    click_next()
    time.sleep(5)

    # QnA starts Here
    print("---------------------------------------------------\n")

    while True:
        option_block = driver.find_element_by_class_name('answers-box')

        try:
            option_block.find_element_by_class_name('question-multiple-group')
            checkbox()
        except:
            try:
                option_block.find_element_by_class_name('question-single-group')
                radio()
            except:
                try:
                    option_block.find_element_by_class_name('btn-answer')
                    buttons()
                except:
                    try:
                        option_block.find_element_by_class_name('question-multiple-group-3-state')
                        multiple()
                    except:
                        try:
                            option_block.find_element_by_class_name('question-scale')
                            scale()
                        except:
                            try:
                                time.sleep(10)

                                conditions = driver.find_elements_by_class_name('condition-item')

                                for condition in conditions:
                                    flow.append(condition.text.split("\n")[0])
                                    flow.append(condition.text.split("\n")[1])
                                    print(condition.text.split("\n")[0])
                                    print(condition.text.split("\n")[1])
                                break
                            except Exception as e:
                                print(e)
                                break

    flow.append("*---*")
driver.quit()
end = time.time()
print("\nTime Taken = ", end - start)

# Convert to CSV
dic = {"Flow" : flow }
df = pd.DataFrame(dic)
df.to_csv("test.csv")
