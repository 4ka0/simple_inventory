from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class TestHomePageNotLoggedIn(TestCase):

    def test_homepage_when_not_logged_in(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')


class TestHomePageLoggedIn(TestCase):

    def setUp(self):
        user = CustomUser.objects.create_user('testuser', '123456')
        self.client.force_login(user=user)

    def test_homepage_by_url_when_logged_in(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_by_name_when_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_content_when_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'role="button">ログアウト</a>', 1)
        self.assertContains(response, '管理TOP</h4>', 1)
        self.assertContains(response, '販売情報管理</a>', 1)
        self.assertContains(response, '果物マスタ管理</a>', 1)
        self.assertContains(response, '販売統計情報</a>', 1)
