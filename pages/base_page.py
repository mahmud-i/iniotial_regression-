import re
import os
import json
from http.client import responses
from playwright.sync_api import BrowserContext


def log_response(response, url):
    status = {}
    if response.url == url:
        status_code = response.status
        status_message = responses.get(status_code, "Unknown Status")
        status['status'] = status_code
        status['message'] = status_message
        print(f"URL: {url}\nResponse: {status_code} {status_message}")
        return status


class PageInstance:
    def __init__(self, context : BrowserContext, url):
        self.context = context
        self.page = context.new_page()
        self.url = url
        self.open_url()

    def open_url(self):
        self.page.on("response", lambda response: log_response(response, self.url))
        self.page.goto(self.url)
        self.wait_for_page_load()
        print(f"Opened URL: {self.url}")

    def terminate(self):
        self.page.close()

    @staticmethod
    def safe_get_attribute(element, attribute_name):
        try:
            value = element.get_attribute(attribute_name)

            # Encode the value to handle any special characters
            return value.encode('utf-8').decode('utf-8') if value else None

        except Exception as e:
            print(f"Error getting attribute '{attribute_name}': {e}")
            return None

    def wait_for_page_load(self):
        try:
            self.page.wait_for_load_state('networkidle')
        except Exception as e:
            return f"Network_idle error: {e}"

    def wait_for_time(self, timeout):
        try:
            self.page.wait_for_timeout(timeout)
        except Exception as e:
            return f"Time_out error: {e}"

    def accept_cookies(self, accept_cookie_selector):
        try:
            self.page.locator(accept_cookie_selector).click()
            print("Accepted cookies")
        except Exception as e:
            print(f"Could not find or click cookie button: {e}")

    def close_email_signup_popup(self, close_email_popup_selector):
        try:
            self.page.locator(close_email_popup_selector).click()
            print("Closed email signup popup")
        except Exception as e:
            print(f"Could not find or close the email signup popup: {e}")

    def close_pop_ups(self):
        self.accept_cookies('button#onetrust-accept-btn-handler')
        self.close_email_signup_popup('button.vds-self_flex-end')

    def get_page_type(self):
        try:
            locator = self.page.locator("head script")
            count = locator.count()
            cc_element = None

            for i in range(count):
                element = locator.nth(i)

                # Get the text content of the current script element
                sc_content = element.text_content()

                # Check if 'careClubConfig' is in the script content
                if "page_type" in sc_content:
                    cc_element = element
                    break

            if cc_element:
                script_content = cc_element.text_content()

                data_layer_main_str = script_content.split('window[\'dataLayer\'] = window[\'dataLayer\'] || [];')[1]
                data_layer_push = data_layer_main_str.split('window[\'dataLayer\'].push(')
                data_layer = None

                for i in range(len(data_layer_push)):
                    data_layer_str = data_layer_push[i].split(");")[0]
                    if "page_type" in data_layer_str:
                        data_layer = json.loads(data_layer_str)
                        break

                if data_layer:
                    page_data = data_layer.get("page_data", {})
                    page_type = page_data.get("page_type", None)
                    return page_type
                else:
                    print("\n\n Page_type not found\n\n")
                    return None
        except Exception as e:
            print(f"Error processing: {e}")