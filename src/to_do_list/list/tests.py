# from django.test import TestCase, RequestFactory
# from django.contrib.auth.models import AnonymousUser
# from django.urls import reverse
# from .models import User
# from . import views
# class BaseViewTestCaseMixin:
#     class_view = None
#     url = None

#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             username='jacob', email='jacob@gmail.com', password='secrets'
#         )

#     def test_login_required(self):
#         request = self.factory.get(self.url)
#         request.user = AnonymousUser()
#         resp = self.class_view.as_view()(request)
#         self.assertEqual(resp.status_code, 302)

#     def test_url_exist(self):
#         request = self.factory.get(self.url)
#         request.user = self.user
#         resp = self.class_view.as_view()(request)
#         self.assertEqual(resp.status_code, 200)


# class TaskCreateTestCase(BaseViewTestCaseMixin, TestCase):
#     class_view = views.TaskCreateView
#     url = reverse('task_add')

#     def test_create_task(self):
#         request = self.factory.get(self.url)
#         print(request)



# class TaskListTestCase(BaseViewTestCaseMixin, TestCase):
#     class_view = views.TaskListView
#     url = reverse('task_view')


# class ActiveTaskTestCase(BaseViewTestCaseMixin, TestCase):
#     class_view = views.ActiveTaskView
#     url = reverse('task_active')


# class DoneTaskTestCase(BaseViewTestCaseMixin, TestCase):
#     class_view = views.DoneTaskView
#     url = reverse('task_done')


# class FriendsListTestCase(BaseViewTestCaseMixin, TestCase):
#     class_view = views.FriendsListView
#     url = reverse('friends_list')
