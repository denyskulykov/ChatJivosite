output_file = "report.csv"
delimiter = ';'  # "," or ";"   - depend on version excel

login = ''
password = ''

time_for_select_period = 1  # sec

add_messages = 1  # 1 or 0
len_message = 500

# ----------------------------------------

import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()

URL_PATH = 'https://app.jivosite.com/chat/archive'
ARCHIVE_PATH = 'https://app.jivosite.com/chat/archive'

driver.get(ARCHIVE_PATH)

# login
driver.find_element_by_class_name('email__10Pt5 ').send_keys(login)
driver.find_element_by_class_name('password__2wrme ').send_keys(password)
driver.find_element_by_class_name('password__2wrme ').send_keys(Keys.ENTER)
sleep(2)


sleep(time_for_select_period)


count_messages = 0
try:
    count_messages = int(driver.find_element_by_class_name('count__2uHut').text[8:])
except:
    temp = driver.find_element_by_class_name('resultFilter__1DMNT').text[8:]
    tmp = ''
    for k in [i for i in temp if i.isdigit()]:
        tmp += k
    count_messages = int(tmp)

start_time = time()

count_record = 0
count_error_record = 0
headers = ('Name', 'Data', 'Messages', 'Source')

try:
    with open(output_file, 'w', ) as csv_file:
        writer = csv.DictWriter(csv_file,
                                fieldnames=headers,
                                delimiter=delimiter,
                                lineterminator='\n')
        writer.writeheader()

        driver.find_element_by_xpath('//*[@id="ArchiveList"]/div/tr').click()
        for _ in range(count_messages):
            try:

                client_name = driver.find_element_by_class_name('nameText__svL1B').text

                date_message = driver.find_element_by_class_name(
                    'text__UHzKN').text

                forward_link = '(empty)'
                try:
                    forward_link = driver.find_element_by_class_name(
                        'capitalize__aHjHM').text
                except Exception as er:
                    pass

                # so long - debug
                text_messages = 'skip'
                if add_messages:
                    text_messages = driver.find_element_by_class_name(
                        'msgList__3xKsJ').text.replace('\n', ' / ')
                    text_messages = text_messages if len(
                        text_messages) < len_message else text_messages[:len_message]

                record = (client_name, date_message, text_messages, forward_link)
                writer.writerow(dict(zip(
                    headers, record)))
                # headers, [unicode(s).encode("cp1251") for s in record])))

                count_record += 1
            except Exception as er:
                count_error_record += 1
                print(er)
                continue
            finally:
                driver.find_element_by_xpath('//*[@id="ArchiveList"]').send_keys(
                    Keys.CONTROL + Keys.DOWN)
                sleep(1)

except:
    raise
finally:
    print('Execute time {}'.format(time() - start_time))
    print('Number of Messages: {}'.format(count_messages))
    print('Success: {}'.format(count_record))
    print('Error: {}'.format(count_error_record))
