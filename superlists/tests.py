import socket
from urllib.parse import urlparse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings 

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

@override_settings(ALLOWED_HOSTS=['*'])
class BaseTestCase(StaticLiveServerTestCase):
	"""
	Provides base test class which connects to the Docker
	container running selenium.
	"""
	host = '0.0.0.0'

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.host = socket.gethostbyname(socket.gethostname())
		cls.browser = webdriver.Remote(
			command_executor='http://selenium:4444/wd/hub',
			desired_capabilities=DesiredCapabilities.CHROME,
		)
		cls.browser.implicitly_wait(5)

	@classmethod
	def tearDownClass(cls):
		cls.browser.quit()
		super().tearDownClass()


class NewVisitorTest(BaseTestCase):
	# fixtures = ['users']

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

		# when she hits enter, the page updates, and now the page lists
		# "1: Buy peacock feathers" as an item in the to-do list table
		inputbox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr') #notice elements plural
		self.assertTrue(
			any(row.text == '1: Buy peacock feathers' for row in rows)
		)

		# There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly"
		self.fail('Finish the test!')


