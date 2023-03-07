from seleniumbase import BaseCase
from time import sleep
from loguru import logger


class MyTestClass(BaseCase):
    def hover_check(self, hover_selector, element_list):
        self.hover(hover_selector)
        for element in element_list:
            try:
                self.assert_element(f'//*[contains(text(),"{element}")]')
            except Exception as e:
                logger.debug(f"{element} not located: {e}")
                try:
                    self.assert_element(f'//*[text()="{element}"]')
                except Exception as e:
                    logger.error(f"{element} not located: {e}")

    def test_basics(self):
        self.open("https://github.com/")

        # after landing on the main page, search "react" in the search bar
        self.type('input[name="q"]', "react")
        self.submit('input[name="q"]')

        # click on the filter dropdown to go through different filters and perform some testing.
        self.click('//*[text()="Sort:"]')
        menu_items = self.find_elements('//a[@class="select-menu-item"]')
        menu_names = [n.text for n in menu_items]
        for item in menu_names:
            logger.info(f'Clicking dropdown item: "{item}"...')
            self.click(f'//a/span[text()="{item}"]')
            sleep(1)
            self.assert_element_visible(f'//summary/span[text()="{item}"]')
            sleep(1)
            self.click('//*[text()="Sort:"]')
            sleep(1)

        # clear the filter and go to facebook/react repo and verify some page elements
        self.click(f'//a/span[text()="{menu_names[0]}"]')
        sleep(1)
        if self.is_element_visible('//*[@href="/facebook/react"]'):
            self.click('//*[@href="/facebook/react"]')
        else:
            self.goto("https://github.com/facebook/react")
        sleep(2)

        # navigate through different tabs of the repo (e.g. Issues, Pull requests, etc.)
        tab_items = self.find_elements('//li[@class="d-inline-flex"]//a')
        tab_names = [n.text for n in tab_items]
        for tab in range(len(self.find_elements('//li[@class="d-inline-flex"]//a'))):
            logger.info(f'Clicking "{tab_names[tab]}" tab...')
            self.click_nth_visible_element('//li[@class="d-inline-flex"]//a', tab)
            sleep(1)

        # hover over on the main navigation and verify the dropdown content (e.g. Product, Solutions, etc)
        expected_product_elements = ['Actions', 'Packages', 'Security', 'Codespaces', 'Copilot', 'Code review',
                                     'Issues', 'Discussions']
        self.hover_check(hover_selector='//*[contains(text(),"Product")]', element_list=expected_product_elements)

        expected_solutions_elements = ['Enterprise', 'Teams', 'Startups', 'Education', 'CI/CD & Automation', 'DevOps',
                                       'DevSecOps', 'Customer Stories', 'Resources']
        self.hover_check(hover_selector='//*[contains(text(),"Solutions")]', element_list=expected_solutions_elements)

        expected_open_source_elements = ['GitHub Sponsors', 'The ReadME Project', 'Topics', 'Trending', 'Collections']
        self.hover_check(hover_selector='//*[contains(text(),"Open Source")]', element_list=expected_open_source_elements)

        ## Extra ##
        ## write any tests you find interesting, don't go too wild :)
        self.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley")
        sleep(10)
