from django.contrib.staticfiles.testing import LiveServerTestCase
from django.test import override_settings, tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import socket
import time
import os
import unittest

@override_settings(ALLOWED_HOSTS=['*'])
@tag('selenium')
class BaseTestCase(LiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running selenium.
    """

    # os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8000'
    host = '0.0.0.0'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.host = socket.gethostbyname(socket.gethostname())
        cls.browser = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        # cls.live_server_url = 'http://{}:8000'.format(cls.host)
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


class NewVisitorTest(BaseTestCase):


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        Edith has heard about a cool new online to-do app. She goes
        to check it out
        """
        # self.browser.get("{}{}".format(self.live_server_url,'/admin'))
        self.browser.get(self.live_server_url)


        # she notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


        # she is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )


        # she types "Buy peacock feathers" into a text box (Edith's hobby)
        inputbox.send_keys('Buy peacock feathers')


        """
        When she hits enter, she is taken to a new URL, and now the page
        lists '1: Buy peacock feathers' as an item in a to-do list table
        """
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')


        """
        There is still a text box inviting her to add another item. She
        enters "Use peacock feathers to make a fly"
        """
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)


        # the page updates again, and now she has both items on the list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        """
        Now a new user, Francis, comes along to the site.

        dev-note: We use a new browswer session to make sure no information of
        Edith's list is coming through from cookies etc.
        """
        self.browser.quit()
        self.browser = webdriver.Remote(
                    command_executor='http://selenium:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.CHROME,
                )

        # Francis vists the home page, there is no signs of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis makes his own list and adds an item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no trace of Edith's list but has his own list item
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        self.fail('Finish the test!')
