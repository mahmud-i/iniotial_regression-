import os
import configparser
from contextlib import contextmanager
from pages.seo_page import SEOInstance
from utils.browser_utility import ConfigurePlatform
from pages.base_page import PageInstance
from tests.test_seo import SEOTest
from datetime import datetime
import utils.json_utility as j
import tests.test_pdp as pdp_test

class TestInstance:
    def __init__(self, brand_name):
        self.config = configparser.ConfigParser()
        self.config.read(f"./config_files/{brand_name}.ini")
        self.prod_domain_url = self.config['urls_data']['prod_domain_url']
        self.brand_name = brand_name
        current_time = datetime.now()
        self.time = current_time.strftime("%H-%M")
        self.date = current_time.strftime("%d-%m-%Y")
        self.seo_testing_data_path = self.config['testing_data']['seo_data']




    def page_setup(self, context):
        page = PageInstance(context, self.prod_domain_url)
        page.close_pop_ups()
        page.terminate()
        print("Page setup done successfully.")


    def execute_test(self, urls_to_check):
        with ConfigurePlatform().browser() as (browser, context):
            print(f"Running tests for: {self.brand_name}")
            self.page_setup(context)

            seo_test_instance = SEOTest(self.brand_name, self.seo_testing_data_path)


            # Now loop through each URL and run tests
            for url in urls_to_check:
                print(f"Running tests for: {url}")
                page = PageInstance(context, url)


                seo_test_instance.run_seo_test(page)

                pdp_test.run_pdp_tests(page, url)

                page.terminate()  # Close the page after testing


            seo_result_data = seo_test_instance.global_seo_result_data

            report_directory = f"Tests_data_result/{self.brand_name}/{self.date}/{self.time}"
            os.makedirs(report_directory, exist_ok=True)
            j.save_json(seo_result_data, f"{report_directory}/SEO_Data_Result_({self.date})_({self.time}).json")


            print(f'{seo_test_instance.global_seo_result_data}')
