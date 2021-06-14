# conda activate discord

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import re

options = Options()
options.add_argument("--user-data-dir=chrome-data")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

driver.get("https://web.whatsapp.com")

driver.execute_script("window.open()")
driver.switch_to.window(driver.window_handles[1])

driver.get("https://discord.com/channels/742797926761234463/852303486628790299") # Trades
# driver.get("https://discord.com/channels/742797926761234463/742798380870271169") # General

# driver.get("https://discord.com/channels/838029509277777950/838029509277777953")

time.sleep(15)

def deEmojify(text):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', text)

def get_messages(driver):
    messages = driver.find_elements_by_xpath("//*[starts-with(@id, 'chat-messages-')]")
    return messages

def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

def send_message(msg):
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath("//*[@title='CryptoBot']").click()
    driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]').send_keys(msg)
    driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button/span').click()
    driver.switch_to_window(driver.window_handles[1])
    return msg

li1 = get_messages(driver)

while True:
    
    li2 = get_messages(driver)
    
    if li1 != li2:
        li3 = Diff(li2, li1)

        for msg in li3:
            filtered_text = deEmojify(msg.text)
            send_message(filtered_text)
            print(filtered_text)
        
        li1 = li2
