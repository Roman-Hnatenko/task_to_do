# # pylint: skip-file
# from typing import Any, Dict
# from django.utils import timezone
# from datetime import timedelta
# from django.test import TestCase, RequestFactory, Client
# from django.contrib.auth.models import AnonymousUser
# from django.conf import settings
# from django.urls import reverse
# from list.models import Task, InviteKey, User
# from list import views


# class SimpleTestCaseMixin:

#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='jacob', email='jacob@gmail.com', password='secrets',
#         )
#         self.client.post(
#             settings.LOGIN_URL,
#             {'username': 'jacob', 'password': 'secrets'},
#         )

#     def test_login_required(self):
#         request = self.factory.get(self.url)
#         request.user = AnonymousUser()
#         response = self.class_view.as_view()(request)
#         response.client = Client()
#         self.assertRedirects(response, f'{settings.LOGIN_URL}?next={self.url}')

#     def test_url_exist(self):
#         resp = self.client.get(self.url)
#         self.assertEqual(resp.status_code, 200)


# class PaginationTestCaseMixin:
#     filter_params: Dict[str, Any] = {}
#     done_task = False

#     def setUp(self):
#         super().setUp()
#         task_number = Task.objects.filter(author=self.user, **self.filter_params).count()

#         tasks = (Task(
#             title=f'My Title{number}',
#             author=self.user,
#             done_date=timezone.now() if self.done_task else None,
#         ) for number in list(range(max(6 - task_number, 0))))
#         if tasks:
#             Task.objects.bulk_create(tasks)

#     def test_pagination_page_exist(self):
#         resp = self.client.get(f'{self.url}?page=1')
#         self.assertEqual(len(resp.context['task_list']), 5)
#         resp = self.client.get(f'{self.url}?page=2')
#         self.assertEqual(resp.status_code, 200)

#     def test_paginational_page_not_exist(self):
#         resp = self.client.get(f'{self.url}?page=3')
#         self.assertEqual(resp.status_code, 404)

#     def test_filters_with_pagination(self):
#         date_now = timezone.now()
#         number_task = Task.objects.filter(date__date=date_now).count()
#         date_now = date_now.date()
#         resp = self.client.get(f'{self.url}?date__date={date_now}&page=1')
#         self.assertEqual(len(resp.context['task_list']), min(number_task, 5))
#         self.assertTrue(resp.context['is_paginated'])


# class TaskCreateTestCase(SimpleTestCaseMixin, TestCase):
#     class_view = views.TaskCreateView
#     url = reverse('task_add')

#     def test_valid_task_form(self):
#         resp = self.client.post(self.url, {'title': 'TestTitle', 'description': 'Some Description'})
#         self.assertEqual(resp.status_code, 302)
#         task = Task.objects.get(title='TestTitle')
#         self.assertEqual(task.title, 'TestTitle')

#     def test_empty_title_field(self):
#         resp = self.client.post(self.url, {'title': '', 'description': 'Some Description'})
#         self.assertFalse(resp.context['form'].is_valid())

#     def test_not_allowed_get_method(self):
#         resp = self.client.get(self.url, {'title': '', 'description': 'Some Description'})
#         self.assertFalse(resp.context['form'].is_valid())


# class TaskDeleteTestCase(SimpleTestCaseMixin, TestCase):
#     class_view = views.TaskDeleteView

#     def setUp(self):
#         super().setUp()
#         self.obj_pk = Task.objects.create(title='Some Task to delete', author=self.user).pk
#         self.url = reverse('task_delete', kwargs={'pk': self.obj_pk})

#     def test_deleted_task_not_exists(self):
#         self.assertTrue(Task.objects.filter(pk=self.obj_pk))
#         self.client.post(self.url)
#         self.assertFalse(Task.objects.filter(pk=self.obj_pk))


# class TaskUpdateTestCase(SimpleTestCaseMixin, TestCase):
#     class_view = views.TaskUpdateView

#     def setUp(self):
#         super().setUp()
#         self.obj_pk = Task.objects.create(title='To update', author=self.user).pk
#         self.url = reverse('task_update', kwargs={'pk': self.obj_pk})

#     def test_changed_title(self):
#         self.client.post(self.url, {'title': 'Another title', 'description': 'Good Task'})
#         self.assertEqual(Task.objects.get(pk=self.obj_pk).title, 'Another title')
#         self.assertEqual(Task.objects.get(pk=self.obj_pk).description, 'Good Task')

#     def test_update_on_empty_title(self):
#         resp = self.client.post(self.url, {'title': '', 'description': 'Good Task'})
#         self.assertFalse(resp.context['form'].is_valid())
#         self.assertEqual(Task.objects.get(pk=self.obj_pk).title, 'To update')


# class TaskListTestCase(PaginationTestCaseMixin, SimpleTestCaseMixin, TestCase):
#     class_view = views.TaskListView
#     url = reverse('task_view')


# class ActiveTaskTestCase(PaginationTestCaseMixin, SimpleTestCaseMixin, TestCase):
#     class_view = views.ActiveTaskView
#     url = reverse('task_active')
#     filter_params = {
#         'done_date__isnull': True,
#     }


# class DoneTaskTestCase(PaginationTestCaseMixin, SimpleTestCaseMixin, TestCase):
#     class_view = views.DoneTaskView
#     url = reverse('task_done')
#     done_task = True
#     filter_params = {
#         'done_date__isnull': False,
#     }

#     def test_filter_for_done_date(self):

#         date_yesterday = timezone.now() - timedelta(days=1)
#         Task.objects.create(title='DoneTask', author=self.user, done_date=date_yesterday)
#         resp = self.client.get(f'{self.url}?done_date__date={date_yesterday}&page=1')
#         self.assertEqual(resp.context['task_list'].first().title, 'DoneTask')


# class FriendsListTestCase(SimpleTestCaseMixin, TestCase):
#     class_view = views.FriendsListView
#     url = reverse('friends_list')

#     def test_friends_exist(self):
#         first_user = User.objects.create_user(
#             username='first', email='first@gmail.com', password='secrets',
#         )
#         second_user = User.objects.create_user(
#             username='second', email='second@gmail.com', password='secrets',
#         )
#         self.user.friends.add(first_user, second_user)
#         resp = self.client.get(self.url)
#         self.assertEqual(len(resp.context['user_list']), 2)


# class KeyCreationTestCase(TestCase):
#     class_view = views.KeyCreationView
#     url = reverse('creation_key')

#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='jacob', email='jacob@gmail.com', password='secrets',
#         )
#         self.client.post(
#             settings.LOGIN_URL,
#             {'username': 'jacob', 'password': 'secrets'},
#         )

#     def test_exists_key_in_bd(self):
#         resp = self.client.post(self.url)
#         self.assertEqual(resp.status_code, 302)
#         self.assertEqual(InviteKey.objects.filter(invitor=self.user).count(), 1)


# class LinkTestCase(SimpleTestCaseMixin, TestCase):
#     class_view = views.LinkView
#     class_name = 'link_info'

#     def setUp(self):
#         super().setUp()
#         key = InviteKey.objects.create(invitor=self.user).key
#         self.url = reverse(self.class_name, kwargs={'key': key})
#         self.another_user = User.objects.create_user(
#             username='another', email='anot@gmail.com', password='secrets',
#         )
#         self.test_user = User.objects.create_user(
#             username='test_user', email='anot@gmail.com', password='secrets',
#         )

#     def test_wrong_key(self):
#         key = InviteKey.objects.create(invitor=self.another_user).key
#         url = reverse(self.class_name, kwargs={'key': key})
#         resp = self.client.get(url)
#         self.assertEqual(resp.status_code, 404)

#     def test_wrong_used_key(self):
#         key = InviteKey.objects.create(invitor=self.user, friend=self.test_user).key
#         url = reverse(self.class_name, kwargs={'key': key})
#         resp = self.client.get(url)
#         self.assertEqual(resp.status_code, 404)


# class AllOutputCsvFileTestCase(SimpleTestCaseMixin, TestCase):
#     class_view = views.AllOutputCsvFileView
#     url = reverse('output_file')


# class DoneOutputCsvFileTestCase(SimpleTestCaseMixin, TestCase):
#     class_view = views.DoneOutputCsvFileView
#     url = reverse('output_file_done')


# class ActiveOutputCsvFileTestCase(SimpleTestCaseMixin, TestCase):
#     class_view = views.ActiveOutputCsvFileView
#     url = reverse('output_file_active')


# class UploadCsvFileTestCase(SimpleTestCaseMixin, TestCase):
#     class_view = views.UploadCsvFileView
#     url = reverse('upload_file')

#     def test_wrong_file_type(self):
#         with open('test_files/test.txt') as file:
#             resp = self.client.post(self.url, {'file': file})
#             self.assertEqual(resp.status_code, 200)
#             self.assertFalse(resp.context['form'].is_valid())

#     def test_empty_file(self):
#         with open('test_files/empty.csv') as file:
#             resp = self.client.post(self.url, {'file': file})
#             self.assertEqual(resp.status_code, 200)
#             self.assertFalse(resp.context['form'].is_valid())

#     def test_wrong_data_in_file(self):
#         with open('test_files/wrong_data.csv') as file:
#             resp = self.client.post(self.url, {'file': file})
#             self.assertEqual(resp.status_code, 200)
#             self.assertFalse(resp.context['form'].is_valid())


# class InvitorInfoTestCase(LinkTestCase):
#     class_view = views.InvitorInfoView
#     class_name = 'invitor_info'

#     def test_wrong_key(self):
#         key = InviteKey.objects.create(invitor=self.another_user).key
#         wrong_key = str(key)[:-2]
#         url = reverse(self.class_name, kwargs={'key': wrong_key})
#         resp = self.client.get(url)
#         self.assertEqual(resp.status_code, 404)

#     def test_invitor_username(self):
#         key = InviteKey.objects.create(invitor=self.another_user).key
#         url = reverse(self.class_name, kwargs={'key': key})
#         resp = self.client.get(url)
#         self.assertEqual(resp.context['key'].invitor.username, 'another')


# class InviteAcceptingTestCase(TestCase):
#     url = reverse('accept_invite')

#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='jacob', email='jacob@gmail.com', password='secrets',
#         )
#         self.client.post(
#             settings.LOGIN_URL,
#             {'username': 'jacob', 'password': 'secrets'},
#         )
#         self.another_user = User.objects.create_user(
#             username='another', email='another@gmail.com', password='secrets',
#         )
#         self.key_obj = InviteKey.objects.create(invitor=self.another_user)

#     def test_add_to_friends(self):
#         self.client.post(self.url, {'key': self.key_obj.key})

#         self.assertTrue(self.user.friends.filter(username='another'))

#     # def test_already_frieds(self):
#     #     resp = self.client.post(self.url, kwargs={'key': self.key_obj.key})
#     #     self.assertEqual(resp.status_code, 200)

#     # def test_friend_with_self(self):
#     #     self.client.post(
#     #         settings.LOGIN_URL,
#     #         {'username': 'another', 'password': 'secrets'},
#     #     )
