from __future__ import unicode_literals
from django.test import TestCase

class smokeTest(TestCase):
	def test_bad_maths(self):
		self.assertEqual(1+1, 3)

