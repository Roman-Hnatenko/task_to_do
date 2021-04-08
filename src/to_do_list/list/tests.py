from typing import Any, Dict
from datetime import datetime, timedelta
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.urls import reverse
from list.models import Task, InviteKey
from list import views


class SimpleTestCaseMixin:

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        # self.user = User.objects.create_user(
        #     username='jacob', email='jacob@gmail.com', password='secrets',
        # )
        # self.client.post(
        #     settings.LOGIN_URL,
        #     {'username': 'jacob', 'password': 'secrets'},
        # )

    def test_login_required(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = self.class_view.as_view()(request)
        response.client = Client()
        self.assertRedirects(response, f'{settings.LOGIN_URL}?next={self.url}')

    def test_url_exist(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class PaginationTestCaseMixin:
    filter_params: Dict[str, Any] = {}
    done_task = False

    def setUp(self):
        super().setUp()
        task_number = Task.objects.filter(author=self.user, **self.filter_params).count()

        tasks = (Task(
            title=f'My Title{number}',
            author=self.user,
            done_date=datetime.now() if self.done_task else None,
        ) for number in list(range(max(6 - task_number, 0))))
        if tasks:
            Task.objects.bulk_create(tasks)

    def test_pagination_page_exist(self):
        resp = self.client.get(f'{self.url}?page=1')
        self.assertEqual(len(resp.context['task_list']), 5)
        resp = self.client.get(f'{self.url}?page=2')
        self.assertEqual(resp.status_code, 200)

    def test_paginational_page_not_exist(self):
        resp = self.client.get(f'{self.url}?page=3')
        self.assertEqual(resp.status_code, 404)

    def test_filters_with_pagination(self):
        date_now = datetime.now().date()
        number_task = Task.objects.filter(date__date=date_now).count()
        resp = self.client.get(f'{self.url}?date__date={date_now}&page=1')
        self.assertEqual(len(resp.context['task_list']), min(number_task, 5))
        self.assertTrue(resp.context['is_paginated'])


class TaskCreateTestCase(SimpleTestCaseMixin, TestCase):
    class_view = views.TaskCreateView
    url = reverse('task_add')

    def test_valid_task_form(self):
        resp = self.client.post(self.url, {'title': 'TestTitle', 'description': 'Some Description'})
        self.assertEqual(resp.status_code, 302)
        task = Task.objects.get(title='TestTitle')
        self.assertEqual(task.title, 'TestTitle')

    def test_empty_title_field(self):
        resp = self.client.post(self.url, {'title': '', 'description': 'Some Description'})
        self.assertFalse(resp.context['form'].is_valid())

    def test_not_allowed_get_method(self):
        resp = self.client.get(self.url, {'title': '', 'description': 'Some Description'})
        self.assertFalse(resp.context['form'].is_valid())


class TaskDeleteTestCase(SimpleTestCaseMixin, TestCase):
    class_view = views.TaskDeleteView

    def setUp(self):
        super().setUp()
        self.obj_pk = Task.objects.create(title='Some Task to delete', author=self.user).pk
        self.url = reverse('task_delete', kwargs={'pk': self.obj_pk})

    def test_deleted_task_not_exists(self):
        self.assertTrue(Task.objects.filter(pk=self.obj_pk))
        self.client.post(self.url)
        self.assertFalse(Task.objects.filter(pk=self.obj_pk))


class TaskUpdateTestCase(SimpleTestCaseMixin, TestCase):
    class_view = views.TaskUpdateView

    def setUp(self):
        super().setUp()
        self.obj_pk = Task.objects.create(title='To update', author=self.user).pk
        self.url = reverse('task_update', kwargs={'pk': self.obj_pk})

    def test_changed_title(self):
        self.client.post(self.url, {'title': 'Another title', 'description': 'Good Task'})
        self.assertEqual(Task.objects.get(pk=self.obj_pk).title, 'Another title')
        self.assertEqual(Task.objects.get(pk=self.obj_pk).description, 'Good Task')

    def test_update_on_empty_title(self):
        resp = self.client.post(self.url, {'title': '', 'description': 'Good Task'})
        self.assertFalse(resp.context['form'].is_valid())
        self.assertEqual(Task.objects.get(pk=self.obj_pk).title, 'To update')


class TaskListTestCase(PaginationTestCaseMixin, SimpleTestCaseMixin, TestCase):
    class_view = views.TaskListView
    url = reverse('task_view')


class ActiveTaskTestCase(PaginationTestCaseMixin, SimpleTestCaseMixin, TestCase):
    class_view = views.ActiveTaskView
    url = reverse('task_active')
    filter_params = {
        'done_date__isnull': True,
    }


class DoneTaskTestCase(PaginationTestCaseMixin, SimpleTestCaseMixin, TestCase):
    class_view = views.DoneTaskView
    url = reverse('task_done')
    done_task = True
    filter_params = {
        'done_date__isnull': False,
    }

    def test_filter_for_done_date(self):
        date_yesterday = datetime.today().date() - timedelta(days=1)
        Task.objects.create(title='DoneTask', author=self.user, done_date=date_yesterday)
        resp = self.client.get(f'{self.url}?done_date__date={date_yesterday}&page=1')
        self.assertEqual(resp.context['task_list'].first().title, 'DoneTask')


class FriendsListTestCase(SimpleTestCaseMixin, TestCase):
    class_view = views.FriendsListView
    url = reverse('friends_list')


class KeyCreationTestCase(TestCase):
    url = reverse('creation_key')

    def setUp(self):
        self.client = Client()
        # self.user = User.objects.create_user(
        #     username='jacob', email='jacob@gmail.com', password='secrets',
        # )
        # self.client.post(
        #     settings.LOGIN_URL,
        #     {'username': 'jacob', 'password': 'secrets'},
        # )

    def test_exists_key_in_bd(self):
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(InviteKey.objects.filter(invitor=self.user).count(), 1)
