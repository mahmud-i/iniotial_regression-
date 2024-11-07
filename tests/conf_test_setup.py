import os
import configparser as cp
import utils.json_utility as j
from utils.browser_utility import ConfigurePlatform
from pages.base_page import PageInstance
from tests.test_seo import SEOTest
from datetime import datetime
import tests.test_pdp as pdp_test

class TestInstance:
    def __init__(self, brand_name):
        self.config = cp.ConfigParser()
        self.config.read(f"./config_files/{brand_name}.ini")
        self.prod_domain_url = self.config['urls_data']['prod_domain_url']
        self.brand_name = brand_name
        current_time = datetime.now()
        self.time = current_time.strftime("%H-%M")
        self.date = current_time.strftime("%d-%m-%Y")
        self.testing_error = {}





    def page_setup(self, context):
        page = PageInstance(context, self.prod_domain_url)
        page.close_pop_ups()
        page.terminate()
        print("Page setup done successfully.")


    def execute_test(self, urls_to_check):
        with ConfigurePlatform().browser() as (browser, context):
            c = 0
            total = len(urls_to_check)
            print(f"Running tests for: {self.brand_name}\nTotal urls to check: {total}")
            self.page_setup(context)

            seo_test_instance = SEOTest(self.brand_name, self.config)


            # Now loop through each URL and run tests
            for url in urls_to_check:
                c += 1
                print(f"\npage: {c}/{total}")
                page = PageInstance(context, url)

                if page.open_status == "success":
                    seo_test_instance.run_seo_test(page)
                    pdp_test.run_pdp_tests(page, url)


                    page.terminate() # Close the page after testing

                else:
                    self.testing_error[f'{url}'] = {"error" : f"page opening error: {page.open_status}"} #Exeption handling in case of Page error due to network or any other reason.



            report_directory = f"Tests_data_result/{self.brand_name}/{self.date}/{self.time}"
            os.makedirs(report_directory, exist_ok=True)

            seo_test_instance.generate_seo_report(report_directory) #SEO Test Report Generation

            if self.testing_error:
                j.save_json(self.testing_error, f"{report_directory}/error_page_testing.json") #Page with error report generation
