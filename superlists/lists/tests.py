from __future__ import unicode_literals
from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item

class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)
		expected_html = render_to_string(
			'home.html',
			{'new_item_text' :'A new list item'}
		)
		self.assertEqual(response.content.decode(), expected_html)

class ItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'First item ever!'
		first_item.save()

		second_item = Item()
		second_item.text = 'Second item ever!'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		first_saved = saved_items[0]
		second_saved = saved_items[1]
		self.assertEqual(first_saved.text,'First item ever!' )
		self.assertEqual(second_saved.text,'Second item ever!' )

