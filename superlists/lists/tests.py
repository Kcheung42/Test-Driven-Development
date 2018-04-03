from __future__ import unicode_literals
from django.test import TestCase

import socket
from urllib.parse import urlparse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings 

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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
        cls.selenium = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class homeTest(BaseTestCase):
	# fixtures = ['users']

	def test_home(self):
		"""
		Should open django admin page
		"""
		self.selenium.get("{}{}".format(self.live_server_url,'/admin'))
		self.assertIn('Django', self.selenium.title)
