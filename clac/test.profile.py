from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile  # change to 'clac.models' if needed

class ProfileTierTest(TestCase):
    def test_update_tier(self):
        # Create a user
        user = User.objects.create_user(username='vaish', password='test123')

        # Ensure profile exists (auto-created or manually created)
        profile, _ = Profile.objects.get_or_create(user=user)

        # Set coins and update tier
        profile.coins = 500
        profile.update_tier()

        # Assert correct tier
        self.assertEqual(profile.tier, 'Innovator')
