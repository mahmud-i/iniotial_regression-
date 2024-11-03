


def run_pdp_tests(page, url):

    page_type = page.get_page_type()
    print(f"Tests completed for: {url}, Page type: {page_type}")
    page.terminate()  # Close the page after testing
