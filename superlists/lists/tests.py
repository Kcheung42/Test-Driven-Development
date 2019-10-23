from __future__ import unicode_literals
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import render


from lists.models import Item, List

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    # TODO: Failing because of csrf token
    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()
    #     response = home_page(request)
    #     expected_response = render(request, 'home.djhtml')
        # self.assertEqual(response.content.decode(), expected_response.content.decode())


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_home_page_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')



class ListandItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'First item ever!'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Second item ever!'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved = saved_items[0]
        second_saved = saved_items[1]
        self.assertEqual(first_saved.text,'First item ever!' )
        self.assertEqual(first_saved.list, list_)
        self.assertEqual(second_saved.text,'Second item ever!' )
        self.assertEqual(second_saved.list , list_)


class LiveViewTestCase(TestCase):

    def test_uses_list_template(self):
        list = List.objects.create()
        response = self.client.get(f'/lists/{list.id}/')
        self.assertTemplateUsed(response, 'list.djhtml')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemy 1', list=correct_list)
        Item.objects.create(text='itemy 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other_itemy 1', list=other_list)
        Item.objects.create(text='other_itemy 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(response, 'itemy 1')
        self.assertContains(response, 'itemy 2')
        self.assertNotContains(response, 'other_itemy 1')
        self.assertNotContains(response, 'other_itemy 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        test_text = 'A new item for an existing list'
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': test_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, test_text)
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        test_text = 'A new item for an existing list'
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': test_text})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

