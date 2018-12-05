import time
import traceback
import os

from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from apps.partners.models import PlannedProject
from apps.utils.helpers import before_cutoff_date, dateField_format, formatted_date, list_blend

class PlannedProjectScraper:
    def __init__(self):
        pass

    def run(self):
        # Options to run selenium via buildpacks on heroku
        chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
        opts = ChromeOptions()
        opts.binary_location = chrome_bin
        self.driver = webdriver.Chrome(executable_path="chromedriver",
        chrome_options=opts)
        self.base_url = "https://www.dot14.state.pa.us/ECMS/"
        try:
            self.login_user()
            self.collect_projects()
            project = self.collect_projects()
            self.driver.quit()
            return project
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.driver.quit()

    def login_user(self):
        # log user into ECMS website
        my_username = config('ECMS_USERNAME')
        my_password = config('ECMS_PASSWORD')

        self.driver.get(self.base_url)
        time.sleep(1) #

        print(my_username)
        print(my_password)


        #Entering user/pass into ECMS loggin page
        user_elem = self.driver.find_element_by_name("userid")
        pass_elem = self.driver.find_element_by_name("password")

        user_elem.send_keys(my_username)
        pass_elem.send_keys(my_password)

        #wait 1 second for the above info to be entered then press submit
        time.sleep(1)
        self.driver.find_element_by_name('login').click()
        #Navigate past the ECMS Alert box
        WebDriverWait(self.driver, 1).until(EC.alert_is_present())
        alert = self.driver.switch_to_alert()
        alert.accept()

    def collect_projects(self):
        time.sleep(1.5)
        self.driver.get("http://www.dot14.state.pa.us/ECMS/SVADVSearch?action=showMainPage")

        time.sleep(1.5)

        # Create list of 'construction inspection' Projects
        self.driver.get("http://www.dot14.state.pa.us/ECMS/SVPLPSearch?action=search&LAST_PUBLISHED_DATE_SEARCH_DIRECTION=02&LAST_PUBLISHED_DATE_UNITS=1&LAST_PUBLISHED_DATE_UNIT_CODE=03&SORT_BY_CODE=01&")

        planned_html = self.driver.page_source
        soup = BeautifulSoup(planned_html, "html.parser")

        table = soup.find('table', class_='results')
        if not table:
            print('no table found')
            return 'no table found'

        # Get the rows with data removing the colgroup & headings
        even_rows = table.find('tbody').find_all('tr', class_='PDEvenRow')
        odd_rows = table.find('tbody').find_all('tr', class_='PDOddRow')
        table = list_blend(even_rows, odd_rows)

        project_links = []
        # Only grab projects published since last scrape.
        if PlannedProject.objects.count() > 0:
            last_run_date = formatted_date(PlannedProject.objects.latest('scrapped_date').scrapped_date)
            print(f"[SCRAPER]: 'FINDING PROJECTS ADDED SINCE: {last_run_date}'")
        else:
            last_run_date = '05/01/2018'
            print("[SCRAPER]: 'NO PREVIOUS SCRAPE DATE FOUND, USING 05/01/2018'")
        
        
        # For each job row, if the published date is newer than latest publishing
        # And the job description includes one of our services, add it to `project_links`
        services = ['inspection', 'ci']
        for row in table:
            project_name = row.find_all('td')[3].string.lower()
            for service in services:
                if service in project_name and not before_cutoff_date(row.find_all('td')[4].contents[0].strip(),last_run_date):
                    project_links.append(row.find('td').find('a').get('href'))
                
        # We will keep a list of the necessary attributes for each project inside
        # the planned_projects list.
        planned_projects = []
        print(f" [SCRAPER]: There are {len(project_links)} planned projects being added today")

        # GET INFORMATION FROM EACH PLANNED PROJECT DETAIL PAGE
        for project in project_links:
            self.driver.get(self.base_url + project)
            project_html = self.driver.page_source
            soup = BeautifulSoup(project_html, "html.parser")

            # Go to the row of the `publishing controls` table with the initiating organization
            alternate_org = soup.find_all('table', class_='Page')[0]

            service_requested = soup.find_all('table', class_='Section1')[1].find('tbody').find('tr').find('td').find_all('table')[1].find('tbody').find('tr').find_all('tr', class_='body')[4].find_all('td')[1].string
            if "inspection" not in service_requested.lower():
                continue
            district = soup.find_all('table', class_='Section1')[1].find('table', class_="Section1Body").find('label').string

            details_table = soup.find_all('table', class_='Section1')[2]
            agreement_number = details_table.find_all('td', class_='data')[0].find('a').contents[0].strip()
            project_name = details_table.find_all('table', class_='body')[1].find_all('tr')[1].find_all('td', class_='PDTextarea')[0].string
            url = self.base_url + project
            estimated_cost = details_table.find_all('td', class_='data')[5].contents[0].strip()
            advance_date = details_table.find_all('td', class_='data')[6].contents[0].strip()
            description = ''
            for content in soup.find_all('td', class_='PDTextarea')[1].contents:
                # Try to eventually figure out how to deliniate betweeen
                # bs4 navigablestrings and tags. In the meantime, can't add a tag
                # to a string, so this should work for now.
                try:
                    description += content.string
                except:
                    pass


            # format `advance_date` to YYYY-MM-DD as django datefield requires
            advance_date = dateField_format(advance_date)

            # remove 'engineering district' and ending '-0' from district
            # so that only the int remains
            district = int(district.strip("Engineering District -0"))
            if district in [3,4,5,6,8]:
                office = "King of Prussia"
            else:
                office = "Pittsburgh"

            print(f'''
            district: {district},
            agreement: {agreement_number},
            name: {project_name},
            date: {advance_date},
            cost: {estimated_cost},
            url: {url},
            office: {office},
            description: {description}
            ''')

            planned_projects.append(
            [district,
            agreement_number,
            project_name,
            advance_date,
            estimated_cost,
            url,
            office,
            description]
            )
            time.sleep(3)
        return planned_projects
