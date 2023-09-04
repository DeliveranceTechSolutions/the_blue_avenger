# extended from https://github.com/fabricio-aguiar/Easy-Apply-bot
import time
import random
import selenium
from dotenv import load_dotenv
load_dotenv()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui

from tkinter import filedialog, Tk
import os

class BlueAvenger:
    MAX_APPLICATIONS = 10000

    def __init__(self, language):
        resource = os.getenv("CHROMEDRIVER_RESOURCE_WINDOWS")
        self.language = language
        self.options = self.browser_options()
        self.browser = webdriver.Chrome(options=self.options, executable_path=resource)
        self.positions = []
        self.position = ""
        self.counter = 0
        self.start_linkedin()

    def browser_options(self):
        options = Options()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("user-agent=Chrome/93.0.4577.82 Safari/537.36 Edge/14.14393")
        return options

    def start_linkedin(self):
        self.browser.get(os.getenv("LOGIN_RESOURCE"))
        user_uname = os.getenv("USER_UNAME")
        user_pname = os.getenv("USER_PNAME")

        
        time.sleep(random.uniform(1.2, 2.3))
        self.browser.execute_script("document.getElementById('password').value = arguments[0]", user_pname)
        time.sleep(random.uniform(3.5, 4.2))
        self.browser.execute_script("document.getElementById('username').value = arguments[0]", user_uname)
        time.sleep(random.uniform(1.2, 1.8))
        self.browser.execute_script("const a = document.getElementsByClassName('btn__primary--large')[0];a.click()")
        # submit_button = self.browser.find_element_by_xpath("//*[text()='Sign in']")
        # print(submit_button)
        # print(submit_button.click())
        # self.click_sign_in(submit_button)
        return
    
    def click_sign_in(self, btn):
        try:
            btn.click()
        except:
            self.click_sign_in(btn)

    def wait_for_login(self):
        time.sleep(30)

    def fill_data(self):
        self.browser.set_window_size(0, 0)
        self.browser.set_window_position(2000, 2000)
        os.system("reset")

        positions = input("What jobs would you like to apply for? Enter multiple keywords for multiple searches, enter keywords as a string seperated as spaces.")
        keywords = positions.split()
        for keyword in keywords:
            self.positions.append(keyword.replace(" ", "%20"))
        location = input("Where are the jobs located? " +
                         "(i.e. Global, Country (United States), State (California), City (San Francisco): ")
        self.location = "&location=" + location.replace(" ", "%20") + "&sortBy=DD"

        print("\nPlease select your curriculum\n")
        time.sleep(1)
        root = Tk()
        self.resumeloctn = ""

        root.destroy()

    def start_apply(self):
        self.wait_for_login()
        self.fill_data()
        for i in range(len(self.positions)):
            self.position = self.positions[i]
            self.applications_loop()

    def applications_loop(self):
        count_application = 0
        count_job = 0
        jobs_per_page = 0

        os.system("reset")

        self.browser.set_window_position(0, 0)
        self.browser.maximize_window()
        self.browser, _ = self.next_jobs_page(jobs_per_page)

        while count_application < self.MAX_APPLICATIONS:
            # sleep to make sure everything loads, add random to make us look human.
            time.sleep(random.uniform(3.5, 6.9))

            page = BeautifulSoup(self.browser.page_source, 'lxml')

            jobs = self.get_job_links(page)

            if not jobs:
                print("Jobs not found")
                break

            for job in jobs:
                count_job += 1
                job_page = self.get_job_page(job)
                print(self.got_easy_apply(job_page))
                if self.got_easy_apply(job_page):
                    print('here')
                    string_easy = os.getenv("HAS_EASY_APPLY")
                    xpath = self.easy_apply_xpath()
                    self.click_button(xpath)
                    self.send_resume()
                    count_application += 1
                else:
                    string_easy = os.getenv("NO_EASY_APPLY")

                position_number = str(count_job + jobs_per_page)
                print(f"\nPosition {position_number}:\n {self.browser.title} \n {string_easy} \n")

                if count_job == len(jobs):
                    jobs_per_page = jobs_per_page + 25
                    count_job = 0
                    print()
                    self.avoid_lock()
                    self.browser, jobs_per_page = self.next_jobs_page(jobs_per_page)

        self.finish_apply()

    def get_job_links(self, page):
        links = []
        for link in page.find_all('a'):
            url = link.get('href')

            if url:
                if '/jobs/view' in url:
                    links.append(url)
        return set(links)

    def get_job_page(self, job):
        root = 'www.linkedin.com'
        if root not in job:
            job = 'https://www.linkedin.com'+job
        self.browser.get(job)
        self.job_page = self.load_page(sleep=0.5)
        return self.job_page

    def got_easy_apply(self, page):
        button = page.find("button", class_="jobs-apply-button")
        return len(str(button)) > 4

    def get_easy_apply_button(self):
        # jobs-s-apply--fadein inline-flex mr2 jobs-s-apply:::possibly old html classes
        button_class = "jobs-apply-button--top-card"
        button = self.job_page.find("div", class_=button_class)
        return button

    def easy_apply_xpath(self):
        button = self.get_easy_apply_button()
        button_inner_html = str(button)
        list_of_words = button_inner_html.split()
        time.sleep(.5)
        next_word = [word for word in list_of_words if "ember" in word and "id" in word]
        ember = next_word[0].split('>')
        xpath = '//*[@'+ember[0]+']'
        self.counter += 1
        print(self.counter)       
        return xpath

    def click_button(self, xpath):
        triggerDropDown = self.browser.find_element_by_xpath(xpath)
        time.sleep(0.5)
        triggerDropDown.click()
        time.sleep(1.5)

    def send_resume(self):
        time.sleep(1)
        print("while loop starts here")
        try:
            for counter in range(0, 8):
                if not self.press_next_button(): counter += 1
                if not self.press_review_button(): counter += 1
                if not self.press_radio_button(): counter += 1
                if not self.enter_input(): counter += 1
                if not self.check_release_lock(): counter += 1
                else: return
                print(counter)

                time.sleep(random.uniform(1.5, 2.5))
                self.browser.switch_to.window(self.browser.window_handles[0])
        except:
            return
               
    def press_next_button(self):
        try:
            next_button = self.browser.find_element_by_xpath("//*[text()='Next']")
            next_button.click()
            return True
        except:
            return False

    def press_review_button(self):
        try:
            review_button = self.browser.find_element_by_xpath("//*[text()='Review']")
            review_button.click()
            return True
        except:
            return False

    def press_radio_button(self):
        try:
            radio_lock = self.browser.find_elements_by_xpath(os.getenv("RADIO_BUTTN_ID") + job_id[5] + "')]")
            for i in range(len(radio_lock)):    
                self.browser.execute_script("arguments[0].click()", radio_lock[i])
            return True
        except:
            return False

    def enter_input(self):
        try:
            job_id = self.browser.current_url.split('/')
            input_lock = self.browser.find_elements_by_xpath(os.getenv("ENTER_INPUT_ID") + job_id[5] + "')]")
            for i in range(len(input_lock)):
                if self.browser.execute_script("arguments[0].value", input_lock[i]) == "":
                    input_lock[i].send_keys('3')   
            return True
        except:
            return False

    def check_release_lock(self):
        try:
            print("Complete")
            submit_button = self.browser.find_element_by_xpath("//*[text()='Submit application']")
            submit_button.click()
            time.sleep(random.uniform(1.5, 2.5))
            return True
        except:
            return False

    def load_page(self, sleep=1):
        scroll_page = 0
        while scroll_page < 4000:
            self.browser.execute_script("window.scrollTo(0,"+str(scroll_page)+" );")
            scroll_page += 200
            time.sleep(sleep)

        if sleep != 1:
            self.browser.execute_script("window.scrollTo(0,0);")
            time.sleep(sleep * 3)

        page = BeautifulSoup(self.browser.page_source, "lxml")
        return page

    def avoid_lock(self):
        x, _ = pyautogui.position()
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(x+1, x, duration=1.0)
        pyautogui.moveTo(x, x+1, duration=0.5)
        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(0.5)
        pyautogui.press('esc')

    def next_jobs_page(self, jobs_per_page):
        self.browser.get(
            os.getenv("NEXT_JOBS_PAGE_RESOURCE") +
            self.position + self.location + "&start="+str(jobs_per_page))
        self.avoid_lock()
        self.load_page()
        return (self.browser, jobs_per_page)

    def finish_apply(self):
        self.browser.close()


if __name__ == '__main__':

    bot = BlueAvenger('en')
    bot.start_apply()
