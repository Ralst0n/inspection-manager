from django.test import TestCase
from django.contrib.auth.models import User
from apps.profiles.models import Profile
# Create your tests here.

class ProfilesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Mbaggoo93",
            email="Mbaggoo2@hotmail.com",
            password="this_is_a_password"
        )

    def test_profile_created(self):
        # A profile object is created do to a user being created
        self.assertEqual(Profile.objects.count(), 1)

    def test_profile_defaults(self):
        # Profile fields with default are set correctly
        self.assertEqual(self.user.profile.office, "King of Prussia")
        self.assertEqual(self.user.profile.role, "Observer")