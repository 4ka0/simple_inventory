from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class TestHomePageNotLoggedIn(TestCase):
    def test_homepage_when_not_logged_in(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "<p>Welcome to your very own fairly simple inventory management system.</p>",
            1,
        )
        # The below string only displayed when user not logged in
        self.assertContains(
            response,
            "But be careful, you must be logged in to do any of this (security is tight here",
            1,
        )


class TestHomePageLoggedIn(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)

    def test_homepage_by_url_when_logged_in(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_homepage_by_name_when_logged_in(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_homepage_content_when_logged_in(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response,
            "<p>Welcome to your very own fairly simple inventory management system.</p>",
            1,
        )
        # The below string only displayed when user is logged in
        self.assertContains(
            response,
            "Feel free to add some &#127819;&#127823;&#127818;, generate some sales, and check out your stats.",
            1,
        )
