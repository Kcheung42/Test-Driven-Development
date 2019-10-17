from django.contrib.staticfiles.testing import LiveServerTestCase
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import socket
import time
import os
import unittest

@override_settings(ALLOWED_HOSTS=['*'])
class BaseTestCase(LiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running selenium.
    """

    # os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8000'
    host = '0.0.0.0'

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.host = socket.gethostbyname(socket.gethostname())
        self.browser = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        # self.live_server_url = 'http://{}:8000'.format(self.host)
        self.browser.implicitly_wait(5)


    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        self.browser.quit()


class NewVisitorTest(BaseTestCase):


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Kenny has heard about a cool new online to-do app. He goes
        # to check it out
        # self.browser.get("{}{}".format(self.live_server_url,'/admin'))
        self.browser.get(self.live_server_url)


        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


        # He is invited to enter a to-do item straight away
        nputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )


        # He types "Buy peacock feathers" into a text box (Kenny's hobby)
        inputbox.send_keys('Buy peacock feathers')


        # When He hits enter, He is taken to a new URL, and now the page
        # lists '1: Buy peacock feathers' as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/(\d+)')
        self.check_for_row_in_list_table('1: Buy peacock feathers')


        # There is still a text box inviting her to add another item. He
        # enters 'Use peacock feathers to make a fly'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)


        # the page updates again, and now He has both items on the list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Now a new user, Bambi, comes along to the site.

        # dev-note: We use a new browswer session to make sure no information of
        # Kenny's list is coming through from cookies etc.
        # self.browser.close()

        self.browser = webdriver.Remote(
                    command_executor='http://selenium:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.CHROME,
                )


        # Bambi vists the home page, there is no signs of Kenny's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Bambi makes his own list and adds an item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Bambi gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no trace of Kenny's list but has 51his own list item
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)


    def test_layout_and_styling(self):
        # Kenny goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] // 2,
            512,
            delta=6
            )

        # He starts a new list and also sees the input is nicely centered too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] // 2,
            512,
            delta=6
            )
