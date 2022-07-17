from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import io
import pickle
from configparser import ConfigParser
from pathlib import Path
from time import sleep
import sys


class Delfi:
    def __init__(self, page: str, domains: list):
        self.page = page
        self.sub_domains = domains
        self.conf = self.read_conf()


    def get_content(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, executable_path='/var/www/html/Paywall/geckodriver')
        url = sys.argv[1]

        driver.get(url)
        domain = url.split(".")[0]

        if domain.split("//")[1] == "www":
            sub_domain = url.split(".")[1]
        else:
            sub_domain = domain.split("//")[1]

        article = url.split("/")

        if article[4] == "artikkel":
            article = article[4] + "-" + article[5] + ".html"
        else:
            article = article[3] + "-" + article[4] + ".html"
        if Path(article).is_file() is False:

            self.check_cookie(sub_domain, driver)

            driver.refresh()
            sleep(4)

            if driver.find_elements_by_css_selector(".S-modal-overlay"):  # delete logout warning
                bg_element = driver.find_element_by_css_selector(".S-modal-overlay")
                driver.execute_script("""var element = arguments[0]; 
            element.parentNode.removeChild(element);""", bg_element)

                log_element = driver.find_element_by_css_selector(".S-modal__content")
                driver.execute_script("""var element = arguments[0]; 
            element.parentNode.removeChild(element);""", log_element)

            html = driver.page_source
            driver.close()

            with io.open(article, "w", encoding="utf-8") as f:
                f.write(html)
                f.close()

        return article


    def read_conf(self):
        conf = ConfigParser()
        conf.read("config.ini")

        return conf


    def log_in(self,data, sub_domain, driver):
        if sub_domain != "delfi":
            driver.get("https://www."+sub_domain+".delfi.ee")
        else:
            driver.get("https://www.delfi.ee")
        driver.implicitly_wait(3)

        driver.find_element_by_css_selector("div.C-tab:nth-child(1) > div:nth-child(1) > div:nth-child(2) > button:nth-child(1)").click()  # accept cookies
        driver.implicitly_wait(2)

        driver.find_element_by_css_selector(".C-header-actions__button--login").click()  # find login button


        driver.find_element_by_css_selector("input.S-form-input:nth-child(1)").send_keys(data.get('DELFI', 'email'))
        driver.find_element_by_css_selector("input.S-form-input:nth-child(2)").send_keys(data.get('DELFI', 'password'))

        driver.find_element_by_css_selector(".S-button--primary").click()  # log in

        cookies = driver.get_cookies()
        driver.delete_all_cookies()
        return cookies



    def save_cookie(self, sub_domain, driver):
        with io.open("cookies/"+sub_domain+"_cookies", "wb") as f:
            pickle.dump(self.log_in(self.conf, sub_domain, driver), f)

    def set_cookie(self, driver, sub_domain):
        with io.open("cookies/"+sub_domain+"_cookies", "rb") as cookief:
            cookies = pickle.load(cookief)
            for cookie in cookies:
                driver.add_cookie(cookie)

    def check_cookie(self, sub_domain: str, driver):
        if self.sub_domains.__contains__(sub_domain):
            file = Path("cookies/"+sub_domain.split(".")[0]+"_cookies")
            if file.is_file():
                self.set_cookie(driver, sub_domain)
            else:
                self.save_cookie(sub_domain, driver)
                self.set_cookie(driver, sub_domain)

        else:
            print("ERROR wrong domain, try again")




if __name__ == '__main__':
    sub_domains = ["forte", "epl", "maaleht", "kroonika", "ekspress", "naistekas", "delfi", "sport", "arileht", "omamaitse", "eestinaine", "tasku", "reisijuht", "roheportaal", "rus", "lood", "perejakodu", "maakodu", "moodnekodu", "lemmikloom", "ilmateade", "annestiil", "tervispluss", "tv", "kinoveeb", "alkeemia"]
    d = Delfi("Delfi", sub_domains)
    print(d.get_content())
