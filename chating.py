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

# checking file
with open(output_file, 'w'):
    pass

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()

URL_PATH = 'https://app.jivosite.com/chat/archive'
ARCHIVE_PATH = 'https://app.jivosite.com/chat/archive'

driver.get(ARCHIVE_PATH)

# login
driver.find_elements_by_xpath('//input')[2].send_keys(login)
# driver.find_element_by_class_name('email__2P1Oe').send_keys(login)
driver.find_elements_by_xpath('//input')[3].send_keys(password)
driver.find_elements_by_xpath('//input')[3].send_keys(Keys.ENTER)
# driver.find_element_by_class_name('').send_keys(password)
# driver.find_element_by_class_name('').send_keys(Keys.ENTER)
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
    with open(output_file, 'w', encoding='cp1251') as csv_file:
        writer = csv.DictWriter(csv_file,
                                fieldnames=headers,
                                delimiter=delimiter,
                                lineterminator='\n')
        writer.writeheader()

        driver.find_element_by_xpath('//*[@id="ArchiveList"]/div/tr').click()
        for _ in range(count_messages):
            try:

                client_name = driver.find_element_by_class_name('nameText__3qMGq').text

                try:
                    date_message = driver.find_element_by_class_name(
                        'text__3Cahs').text
                except BaseException as er:
                    date_message = '(empty)'

                try:
                    forward_link = driver.find_element_by_class_name(
                        'capitalize__1ruF-').text
                except BaseException as er:
                    forward_link = '(empty)'

                # so long - debug
                try:
                    if add_messages:
                        text_messages = driver.find_element_by_class_name(
                            'msgList__3xKsJ').text.replace('\n', ' / ')
                        text_messages = text_messages if \
                            len(text_messages) < len_message \
                            else text_messages[:len_message]
                    else:
                        text_messages = 'skip'
                except BaseException as er:
                    text_messages = 'empty'

                record = (client_name, date_message, text_messages, forward_link)
                temp = [s.encode("cp1251", "replace") for s in record]
                record = [s.decode("cp1251") for s in temp]
                writer.writerow(dict(zip(headers, record)))

                count_record += 1
            except BaseException as er:
                count_error_record += 1
                print(er)
                continue
            finally:
                driver.find_element_by_xpath('//*[@id="ArchiveList"]')\
                    .send_keys(Keys.CONTROL + Keys.DOWN)
                sleep(1)

except BaseException:
    raise
finally:
    print('Execute time: {} seconds'.format(int(time() - start_time)))
    print('Number of Messages: {}'.format(count_messages))
    print('Success: {}'.format(count_record))
    print('Error: {}'.format(count_error_record))
