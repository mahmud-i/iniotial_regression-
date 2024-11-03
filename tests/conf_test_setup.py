import configparser
from contextlib import contextmanager
from utils.browser_utility import ConfigurePlatform
from pages.base_page import PageInstance
import tests.test_pdp as pdp_test

class TestInstance:
    def __init__(self, brand_name):
        self.config = configparser.ConfigParser()
        self.config.read(f"./config_files/{brand_name}.ini")
        self.prod_domain_url = self.config['urls_data']['prod_domain_url']
        self.brand_name = brand_name



    def page_setup(self, context):
        page = PageInstance(context, self.prod_domain_url)
        page.close_pop_ups()
        page.terminate()
        print("Page setup done successfully.")


    def execute_test(self, urls_to_check):
        with ConfigurePlatform().browser() as (browser, context):
            print(f"Running tests for: {self.brand_name}")
            self.page_setup(context)
            # Now loop through each URL and run tests
            for url in urls_to_check:
                print(f"Running tests for: {url}")
                page = PageInstance(context, url)

                pdp_test.run_pdp_tests(page, url)

                page.terminate()  # Close the page after testing
