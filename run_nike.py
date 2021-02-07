import time
import os
import zipfile
import pyautogui

from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

scrolling_time = 20 #(in minutes)

def set_proxy_values_and_get_chromedriver(val,use_proxy=False, user_agent=None):

    proxy_file = open("new_proxies.txt","r")
    proxy_list = proxy_file.read().splitlines()
    proxy_file.close()

    selected_num = val%len(proxy_list)

    PROXY_HOST = proxy_list[selected_num].split(":")[0]
    PROXY_PORT = int(proxy_list[selected_num].split(":")[1])
    PROXY_USER = proxy_list[selected_num].split(":")[2]
    PROXY_PASS = proxy_list[selected_num].split(":")[3]


    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    def get_chromedriver(use_proxy=False, user_agent=None):
        path = os.path.dirname(os.path.abspath(__file__))
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            # chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-blink-features")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("start-maximized")
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % user_agent)
        driver = webdriver.Chrome(
            os.path.join(path, 'chromedriver'),
            options=chrome_options)
        return driver

    return get_chromedriver(use_proxy,user_agent)



def do_scroll(t):
    total_sec=0
    while True:
        if total_sec<t:
            scrol_amount=randint(100, 500)
            if(scrol_amount%3==0):
                scrol_amount=scrol_amount*-1
            driver.execute_script("window.scrollBy(0,"+str(scrol_amount)+")", "")
            sleep_time=randint(5, 10)
            time.sleep(sleep_time)
            total_sec+=sleep_time
        else:
            break





file_testing = open("AccountsForTesting.txt","r")
account_list = file_testing.read().splitlines()
file_testing.close()

main_proxy_file = open("new_proxies.txt","r")
main_proxy_list = main_proxy_file.read().splitlines()
main_proxy_file.close()


proxy_number=0
# for i in range (0, len(account_list)):
for i in range (0, len(account_list)):

    # driver = get_chromedriver(use_proxy=True)

    while True:
        try:
            driver = set_proxy_values_and_get_chromedriver(proxy_number,use_proxy=True)
            driver.get("https://www.nike.com/de/login")
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located(
                (By.NAME, "emailAddress")))
            print(account_list[i].split(":")[0]+" connected with proxy " + main_proxy_list[proxy_number % len(main_proxy_list)])
            break
        except:
            print("connecting failed to proxy -> "+main_proxy_list[proxy_number%len(main_proxy_list)])
            proxy_number+=1


    # driver.get("https://api.myip.com")
    # time.sleep(30)




    try:
        proxy_ok_btn = WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//*[@id="PrivacyPolicyBannerAccept"]')))
        proxy_ok_btn.click()
    except:
        pass



    pyautogui.moveTo(100,200)
    time.sleep(2)
    #email location
    pyautogui.click(938, 615)
    time.sleep(1)
    pyautogui.typewrite(account_list[i].split(":")[0])
    time.sleep(1)
    #password location
    pyautogui.click(938, 670)
    time.sleep(1)
    pyautogui.typewrite(account_list[i].split(":")[1])
    time.sleep(1)
    #login button location
    pyautogui.moveTo(938, 916)
    time.sleep(1)
    pyautogui.click()


    #checking logging succesfully
    try:
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '/html/body/div[2]/div[3]/div[7]/form/div[1]/ul/li')))
        print(account_list[i].split(":")[0]+" Login failed")
        driver.close()
        continue
    except:
        print(account_list[i].split(":")[0]+" Successful Login")
        pass



    # ------   not useful when using proxies.

    # time.sleep(10)
    # driver.get("https://www.nike.com")

    #selecting Belgium for the  country

    # WebDriverWait(driver, 60).until(expected_conditions.element_to_be_clickable(
    #     (By.XPATH, '//*[@id="gen-nav-footer"]/nav/div/div/div[4]/div/a[4]/div[2]/p')))
    # country= driver.find_element_by_xpath('//*[@id="gen-nav-footer"]/nav/div/div/div[4]/div/a[4]/div[2]/p')
    # actions = ActionChains(driver)
    # actions.move_to_element(country).perform()
    # country.click()
    #
    # driver.get("https://www.nike.com/de/launch")
    # driver.get("https://www.nike.com/de")

    # ------   not useful when using proxies.

    try:
        #said 20 minutes
        do_scroll(scrolling_time*60)

        driver.get("https://www.nike.com/de/launch?s=upcoming")
        time.sleep(2)
        #clicking on first shoe
        WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[2]/div[2]/div/section[1]/figure[1]/div/div/a/img')))
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/div[2]/div[2]/div/section[1]/figure[1]/div/div/a/img').click()

        time.sleep(2)
        #said 22 sec
        do_scroll(22)

        driver.get("https://www.nike.com/de/launch")
        time.sleep(1)

        #Mehr laden button
        WebDriverWait(driver, 60).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[2]/div[2]/div/section[2]/div/button')))
        driver.find_element_by_xpath(
            '//*[@id="root"]/div/div/div[1]/div/div[2]/div[2]/div/section[2]/div/button').click()

        time.sleep(5)
        # anchor_tags = driver.find_elements_by_tag_name('a')
        figcaptions = driver.find_elements_by_tag_name('figcaption')
        for k in range(0,len(figcaptions)):
            try:
                if(figcaptions[k].text=="Weitere Infos"):
                    figcaptions[k].click()
                    # said 33 sec
                    time.sleep(3)
                    do_scroll(30)
                    print("reading text with "+account_list[i].split(":")[0])
                    break
            except:
                continue

        print("Done with "+account_list[i].split(":")[0])
        output_file = open("emails_done.txt","a")
        output_file.write(account_list[i].split(":")[0]+"\n")
        output_file.close()

        driver.execute_script("window.scrollBy(0,-2000)", "")
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/div/ul/li[1]/div/div/button/div/span/span').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div/header/div[1]/section/div/ul/li[1]/div/div/ul/li[2]/button').click()
        time.sleep(2)
        driver.close()
        proxy_number += 1
    except:
        proxy_number += 1
        continue


print("Done with All")












