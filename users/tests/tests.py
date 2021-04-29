from django.test import TestCase

from ..models import CustomUser

from freezegun import freeze_time


class TestCustomUser(TestCase):
    @classmethod
    @freeze_time("2021-04-01")
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@email.com",
            password="testpassword",
        )

    def test_string_representation(self):
        expected = "testuser"
        self.assertEqual(expected, str(self.user))

    def test_username(self):
        expected = "testuser"
        self.assertEqual(expected, self.user.username)

    def test_first_name(self):
        expected = "Test"
        self.assertEqual(expected, self.user.first_name)

    def test_last_name_(self):
        expected = "User"
        self.assertEqual(expected, self.user.last_name)

    def test_password(self):
        expected = "testpassword"
        self.assertEqual(expected, self.user.password)

    def test_groups(self):
        self.assertEqual("auth.Group.None", str(self.user.groups))

    def test_permissions(self):
        self.assertEqual(
            "auth.Permission.None", str(self.user.user_permissions)
        )

    def test_is_staff(self):
        self.assertEqual(False, self.user.is_staff)

    def test_is_active(self):
        self.assertEqual(True, self.user.is_active)

    def test_is_superuser(self):
        self.assertEqual(False, self.user.is_superuser)

    def test_last_login(self):
        self.assertEqual("None", str(self.user.last_login))

    def test_date_joined(self):
        self.assertEqual(
            "2021-04-01 00:00:00+00:00", str(self.user.date_joined)
        )
