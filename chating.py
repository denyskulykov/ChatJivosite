output_file = "report.csv"
delimiter = ';'  # "," or ";"   - depend on version excel

login = ''  #
password = ''  #

time_for_select_period = 1  # sec

# ----------------------------------------

import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(2)
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

list_messages = driver.find_elements_by_xpath('//*[@id="ArchiveList"]/div/tr')

count_record = 0
count_error_record = 0

headers = ('Name', 'Data', 'Messages', 'Source')
with open(output_file, 'w', ) as csv_file:
    writer = csv.DictWriter(csv_file,
                            fieldnames=headers,
                            delimiter=delimiter,
                            lineterminator='\n')
    writer.writeheader()

    for message in list_messages:
        try:
            try:
                message.click()
            except Exception as er:
                driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
                sleep(1)
                message.click()

            message_id = message.text
            client_name = message.text.split('\n')[0]

            date_message = driver.find_element_by_class_name(
                'text__UHzKN').text
            text_messages = driver.find_element_by_class_name(
                'msgList__3xKsJ').text.replace('\n', ' / ')

            forward_link = '(empty)'
            try:
                forward_link = driver.find_element_by_class_name(
                    'capitalize__aHjHM').text
            except Exception as er:
                pass

            record = (client_name, date_message, text_messages, forward_link)
            writer.writerow(dict(zip(
                headers, [unicode(s).encode("cp1251") for s in record])))

            count_record += 1
        except Exception as er:
            count_error_record += 1
            print er
            continue

print 'Number of Messages: {}'.format(len(list_messages))
print 'Success: {}'.format(count_record)
print 'Error: {}'.format(count_error_record)


# mails = [i.get_attribute('value') for i in driver.find_elements_by_xpath('//input') if i.get_attribute('value').count('@') > 0]
# mail = '(empty)'
# if mails.__len__() == 1:
#     mail = mails[0]
