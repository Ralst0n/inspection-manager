import time
import os
import traceback

from bs4 import BeautifulSoup
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from apps.partners.models import (LetProject, ProjectTeam, BusinessPartner )
from apps.utils.helpers import list_blend, none_project, before_cutoff_date, formatted_date, dateField_format

class LetProjectScrapper:

    def run(self):
        # Options to run selenium via buildpacks on heroku
        chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
        opts = ChromeOptions()
        opts.binary_location = chrome_bin
        self.driver = webdriver.Chrome(executable_path="chromedriver",
        chrome_options=opts)
        self.valid_districts = ["Engineering District 3-0", "Engineering District 4-0", "Engineering District 5-0", "Engineering District 6-0", "Engineering District 8-0"]
        # Districts for the Pittsburgh office aren't always included
        self.valid_districts += ["Engineering District 1-0", "Engineering District 2-0", "Engineering District 9-0", "Engineering District 10-0", "Engineering District 11-0", "Engineering District 12-0"]

        self.base_url = "https://www.dot14.state.pa.us/ECMS"
        projects_by_district = {}
        project_and_rankings_list = []
        self.login_user()
        project_list = self.collect_projects()
        for district in self.valid_districts:
            projects_by_district[district] = {}
        if type(project_list) == list:
            for job in project_list:
                # add project to the correct district
                project_and_rankings = {job['prono']: self.get_project_rankings(job)}
                projects_by_district[job['district']].update(project_and_rankings)
        self.driver.quit()



    def get_project_rankings(self, project):
        # check if the job is construction inspection
        self.driver.get(f"{self.base_url}/{project['href']}")
        rankings_page = self.driver.page_source
        rankings = BeautifulSoup(rankings_page, "html.parser")
        job_type = rankings.find('tr', class_='PDOddRow').find_all('td')[-1].string
        job_type2 = rankings.find_all('tr', class_='PDEvenRow')[1].find_all('td')[-1].string
        # if their is no service type listed, on the first sub or the potential second sub, return None

        # if construction inspection is not in either job type location, check for just inspection
        if ((job_type is None or "construction inspection" not in job_type.lower()) and (job_type2 is None or "construction inspection" not in job_type2.lower())):
            #if its not inspection either, return None
           if ((job_type is None or"inspection" not in job_type.lower()) and (job_type2 is None or "inspection" not in job_type2.lower())):
                return None


        # Some of the projects are coming with a trailing comma
        # We don't want that so we strip it away
        project['prono'] = project['prono'].strip(',')
        teams = []
        rankings_even_rows = rankings.find('table', class_='results').find_all('tr', class_='PDEvenRow')
        rankings_odd_rows = rankings.find('table', class_='results').find_all('tr', class_='PDOddRow')
        rankings_rows = list_blend(rankings_even_rows, rankings_odd_rows)

        for row in rankings_rows:
            # If the first td in the row has content, then that is a listing of a prime and should be set to `p` in the team dict
            if row.find('td').contents[0].strip():
                teams.append({'p': row.find('a').contents[0].strip(), 's':[]})
            # Otherwise the row contains a sub, and the sub should be added to the sub list which is set to `s` in the team dict
            else:
                teams[len(teams)-1]['s'].append(row.find('a').contents[0].strip())

        # Add the business partner to BusinessPartner if they don't exist already
        for team in teams:
            if not BusinessPartner.objects.filter(name = team['p']).exists():
                BusinessPartner.objects.create(
                    name = team['p']
                )
            for sub in team['s']:
                if not BusinessPartner.objects.filter(name = sub).exists():
                    BusinessPartner.objects.create(
                        name = sub
                    )
        # Make the district into an integer for saving into model
        district = int(project['district'].strip("Engineering District -0"))

        if LetProject.objects.filter(agreement_number=project['prono']).count() == 0:
            # Add the current `let_project` to the database by using the prime from each of the first 3 teams
            if len(teams) >= 3:
                LetProject.objects.create(
                    agreement_number = project['prono'],
                    district = district,
                    winner = BusinessPartner.objects.get(name=teams[0].get('p')),
                    second_place = BusinessPartner.objects.get(name=teams[1].get('p')),
                    third_place = BusinessPartner.objects.get(name=teams[2].get('p')),
                    date = project['let_date']
                )
            elif len(teams) == 2:
                LetProject.objects.create(
                    agreement_number = project['prono'],
                    district = district,
                    winner = BusinessPartner.objects.get(name=teams[0].get('p')),
                    second_place = BusinessPartner.objects.get(name=teams[1].get('p')),
                    date = project['let_date']
                )
            elif len(teams) == 1:
                LetProject.objects.create(
                    agreement_number = project['prono'],
                    district = district,
                    winner = BusinessPartner.objects.get(name=teams[0].get('p')),
                    date = project['let_date']
                )

            # Add each team combination to `Project_Team` by iterating through the team rosters
            for team in teams:
                for sub in team['s']:
                    ProjectTeam.objects.create(
                        agreement_number = LetProject.objects.get(agreement_number=project['prono']),
                        prime = BusinessPartner.objects.get(name=team['p']),
                        sub = BusinessPartner.objects.get(name=sub),
                    )
            return teams

    def login_user(self):
        # log user into ECMS website
        my_username = config('ECMS_USERNAME')
        my_password = config('ECMS_PASSWORD')

        self.driver.get(self.base_url)
        time.sleep(1) #

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
        # collect all the projects that match our districts
        self.driver.get("http://www.dot14.state.pa.us/ECMS/SVSERFinalRanking?action=CSCMeetingResultsPast&ORGANIZATION_SCOPE=STATE")
        results_html = self.driver.page_source
        # parse the results page html
        soup = BeautifulSoup(results_html, "html.parser")
        projects = [] #list of projects
        results_table = soup.find('table', class_='results')


        if results_table:
            results_even_rows = results_table.find_all('tr', class_='PDEvenRow')
            results_odd_rows = results_table.find_all('tr', class_='PDOddRow')
            results_rows = list_blend(results_even_rows, results_odd_rows)

            for row in results_rows:
                if LetProject.objects.count() == 0:
                    cutoff_date = '01/01/2018'
                else:
                    cutoff_date = formatted_date(LetProject.objects.latest("let_date").let_date)

                date = row.find('td').find('a').contents[0].strip()

                if before_cutoff_date(date, cutoff_date):
                    print(f"{date} is before {cutoff_date}")
                    continue

                # convert date to yyy-mm-dd to match django formating
                date = dateField_format(date)
                tiny_results_table = row.find('tbody').find_all('tr')
                for organization in tiny_results_table:
                    district = organization.find('td').contents[0].strip()

                    if district in self.valid_districts:
                        # project data gets the next td
                        # for some reason the string inside of the district td counts as a sibling so we use next sibling twice.
                        project_data = organization.find('td').next_sibling.next_sibling.find_all('a')
                        for proj_info in project_data:
                            # for each project number in a valid district:
                            # put the project number as the dict 'prono' and the link as the 'proj_info'
                            project_dict = {'district': district, 'prono': proj_info.contents[0].strip(), 'href': proj_info.get('href'), 'let_date':date}
                            projects.append(project_dict)



            return projects