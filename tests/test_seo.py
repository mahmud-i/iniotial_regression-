from pages.base_page import PageInstance
from pages.seo_page import SEOInstance
import utils.json_utility as j


class SEOTest:
    def __init__(self, brand_name, testing_data):
        self.brand = brand_name
        self.global_seo_result_data = {}
        self.seo_testing_data = j.load_json(testing_data)
        self.global_seo_check = {}
        self.global_seo_assertion = {}



    def run_seo_test(self, page_instance: PageInstance):
        try:
            instance = SEOInstance(page_instance)

            url = page_instance.url
            slug = page_instance.slug

            seo_data = {
                "page_response" : page_instance.response,
                "meta_title" : instance.get_title(),
                "meta_description" : instance.get_meta_description(),
                "canonical_link" : instance.get_canonical_link(),
                "og_title" : instance.get_og_title(),
                "og_description" : instance.get_og_description(),
                "og_type" : instance.get_og_type(),
                "og_site" : instance.get_og_site(),
                "og_url" : instance.get_og_url(),
                "og_image" : instance.get_og_image(),
                "twitter_title" : instance.get_twitter_title(),
                "twitter_description" : instance.get_twitter_description(),
                "twitter_card" : instance.get_twitter_card(),
                "twitter_image" : instance.get_twitter_image(),
                "h1" : instance.get_h1()
                }
            self.global_seo_result_data[f'{slug}'] = {"url": url, "seo_data": seo_data}
            print(f"{url}\n{seo_data}\n")

            self.compare_seo_data(slug, url, seo_data)


        except Exception as e:
            print(f"Error run_SEO_test on'{page_instance.url}': {e}")
            return None



    def compare_seo_data(self, slug, url, seo_data):

        if slug in self.seo_testing_data:
            check_url = self.seo_testing_data[slug].get("url")
            seo_test_data = self.seo_testing_data[slug].get("seo_data",{})

            if check_url != url:
                print("urls not matched")

            for key, val_1 in seo_data.items():
                val_2 = seo_test_data.get(key)
                if val_1 != val_2:
                    print(f"Mismatch in {slug} for '{key}': '{val_1}' != '{val_2}'")
                else:
                    print(f"Match in {slug} for '{key}': '{val_1}' = '{val_2}'")