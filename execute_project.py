# execute_project.py
import sys
import argparse
import configparser
from utils.get_urls import GetUrls
from tests.conf_test_setup import TestInstance

def initializing_test():
    # Load configuration from specified .ini file
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Retrieve values from the .ini file
    brands = config['settings']['brands']
    full_site_testing = config['settings'].get('full_site_testing', 'Y').strip().upper()
    parsing_method = config['settings'].get('parsing_method', '3')

    parser = argparse.ArgumentParser(description="Process multiple data points.")

    # Optional arguments with default values set to None
    parser.add_argument("--brands", type=str, default=brands, help="Brands for test (separate with comma for multiple)")
    parser.add_argument("--full_site", type=str, default=full_site_testing, help="If test run for full site")
    parser.add_argument("--parsing_method", type=str, default=parsing_method, help="Choose any methods for get urls for test: "
                                                                                "1. Get urls from csv file"
                                                                                "2. Input a list of urls for test"
                                                                                "3. Use some random urls collected from the sitemap.xml")
    parser.add_argument("--headless", type=str, default=None, help="Headless mode")
    parser.add_argument("--browser", type=str, default=None, help="Browser type")
    parser.add_argument("--mobile", type=str, default=None, help="Test on Mobile device")
    parser.add_argument("--device_model", type=str, default=None, help="Mobile device model")

    args = parser.parse_args()

    if args.headless is not None :
        config.set('settings', 'headless_chk', args.headless.strip().upper())

    if args.browser is not None :
        config.set('platform', 'browser_type', args.browser.strip().lower())

    if args.mobile is not None :
        responsive = args.mobile.strip().upper()
        if responsive == 'Y' and args.device_model is not None :
            config.set('platform', 'mobile_emulation', "Y")
            config.set('platform', 'mobile_model', args.device_model )

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    brand_list = args.brands.split(',')
    brand_list = [brand.strip() for brand in brand_list]

    for brand_name in brand_list :
        urls_parser = GetUrls(brand_name, args.parsing_method)
        #prod_domain_url = urls_parser.prod_domain_url

        if args.full_site == 'Y':
            urls_to_check = urls_parser.get_urls_from_sitemap()
        else:
            urls_to_check = urls_parser.get_urls_from_others()

        # Running the test suite
        test_service = TestInstance(brand_name)
        test_service.execute_test(urls_to_check)



# Main entry point
if __name__ == "__main__":
    initializing_test()