import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
from urllib.request import urlopen
import pandas as pd
import numpy as np
import requests
import csv
import datetime


class LinkedinScrap:
    def __init__(self, username, password, language, position, location, max_jobs):

        self.dirpath = os.getcwd()
        self.language = language
        self.options = self.browser_options()
        self.browser = webdriver.Chrome(
            options=self.options, executable_path=self.dirpath + "/chromedriver.exe"
        )
        self.start_linkedin(username, password)
        self.outputcsv = position + "_" + location + ".csv"
        self.max_jobs = max_jobs
        self.position = position
        self.location = location

    def browser_options(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(
            "user-agent=Chrome/53.0.2704.79 Safari/537.36 Edge/14.14393"
        )
        # options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        # options.add_argument('--disable-gpu')
        # options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        return options

    def start_linkedin(self, username, password):
        print("\nLogging in.....\n \nPlease wait :) \n ")
        self.browser.get("https://www.linkedin.com/uas/login")
        try:
            elem = self.browser.find_element_by_id("username")
            elem.send_keys(username)
            elem = self.browser.find_element_by_id("password")
            elem.send_keys(password)
            # Enter credentials with Keys.RETURN
            elem.send_keys(Keys.RETURN)
            # Wait a few seconds for the page to load
            time.sleep(5)
        except TimeoutException:
            print(
                "TimeoutException! Username/password field or login button not found on glassdoor.com"
            )

    def wait_for_login(self):
        if language == "en":
            title = "Sign In to LinkedIn"
        elif language == "es":
            title = "Inicia sesión"
        elif language == "pt":
            title = "Entrar no LinkedIn"

        time.sleep(1)

        while True:
            if self.browser.title != title:
                print("\nStarting LinkedIn bot\n")
                break
            else:
                time.sleep(1)
                print("\nPlease Login to your LinkedIn account\n")

    def fill_data(self):
        self.position = self.position
        self.location = "&location=" + self.location

    def start_scrape(self):
        self.fill_data()
        self.extract_jd()

    def extract_jd(self):
        jobs_per_page = 0
        writer = csv.writer(open(self.outputcsv, "w", encoding="utf-8"))

        writer.writerow(
            [
                "job_description",
                "company_name",
                "location",
                "industry_1",
                "employement_type",
                "industry_2",
                "experience_Level",
                "current_url",
            ]
        )

        print("\nLooking for jobs.. Please wait..\n")
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(1920, 1080)
        # self.browser.maximize_window()
        self.browser, _ = self.next_jobs_page(jobs_per_page)
        while jobs_per_page < self.max_jobs:
            print(f"\nAt {jobs_per_page}:\n")
            jobs = self.browser.find_elements_by_class_name("job-card-container")
            for job in jobs:
                current_url = self.browser.current_url

                job.click()

                try:
                    company_name = self.browser.find_element_by_class_name(
                        "jobs-details-top-card__company-url"
                    )
                    company_name = company_name.text
                    if company_name:
                        company_name = company_name.strip()
                except:
                    company_name = None

                try:
                    job_name = self.browser.find_element_by_class_name(
                        "jobs-details-top-card__job-title"
                    )
                    job_name = job_name.text

                    if job_name:
                        job_name = job_name.strip()
                except:
                    job_name = None

                try:
                    job_description = self.browser.find_element_by_xpath(
                        '//*[@id="job-details"]'
                    )
                    job_description = job_description.text

                    if job_description:
                        job_description = job_description.strip()
                except:
                    job_description = None

                try:
                    employement_type = self.browser.find_element_by_class_name(
                        "js-formatted-employment-status-body"
                    )
                    employement_type = employement_type.text

                    if employement_type:
                        employement_type = employement_type.strip()
                except:
                    employement_type = None

                try:
                    industry = self.browser.find_element_by_class_name(
                        "js-formatted-industries-list"
                    )
                    industry = industry.find_elements_by_class_name(
                        "jobs-box__list-item"
                    )
                    industry = [ind.text for ind in industry]
                    industry = ",".join(industry)

                    if industry:
                        industry = industry.strip()
                except:
                    industry = None

                try:
                    location = self.browser.find_element_by_class_name(
                        "jobs-details-top-card__bullet"
                    )
                    location = location.text

                    if location:
                        location = location.strip()
                except:
                    location = None

                try:
                    job_function = self.browser.find_element_by_class_name(
                        "js-formatted-job-functions-list"
                    )
                    job_function = job_function.text

                    if job_function:
                        job_function = job_function.strip()
                except:
                    job_function = None

                try:
                    experience_Level = self.browser.find_element_by_class_name(
                        "js-formatted-exp-body"
                    )
                    experience_Level = experience_Level.text

                    if experience_Level:
                        experience_Level = experience_Level.strip()
                except:
                    experience_Level = None

                writer.writerow(
                    [
                        job_description,
                        company_name,
                        location,
                        industry,
                        employement_type,
                        job_function,
                        experience_Level,
                        current_url,
                    ]
                )
                print(
                    company_name
                    + " - "
                    + job_name
                    + f"({job.get_attribute('data-job-id')})"
                )
                time.sleep(random.uniform(3.5, 10))
            jobs_per_page += 25
            self.browser, _ = self.next_jobs_page(jobs_per_page)

    def load_page(self, sleep=1):
        # scroll = self.browser.find_element_by_class_name('jobs-search-results')
        # for i in range(0,6):
        #     scroll.send_keys(Keys.PAGE_DOWN)
        #     time.sleep(i/10)
        page = BeautifulSoup(self.browser.page_source, "lxml")
        return page

    def next_jobs_page(self, jobs_per_page):
        self.browser.get(
            "https://www.linkedin.com/jobs/search/?keywords="
            + self.position
            + self.location
            + "&start="
            + str(jobs_per_page)
        )

        self.load_page()
        return (self.browser, jobs_per_page)

    def end_scrape(self):
        self.browser.close()
