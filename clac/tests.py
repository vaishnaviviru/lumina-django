from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from clac.models import Profile, Showcase
from django.utils import timezone
from datetime import timedelta


class ShowcaseApprovalTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True,
            is_superuser=True
        )

        self.dev = User.objects.create_user(
            username='dev',
            password='devpass',
            email='dev@paycorp.local'
        )

        self.profile = Profile.objects.get(user=self.dev)

        self.showcase = Showcase.objects.create(
            owner=self.profile,
            title='Test Showcase',
            body_md='**Hello World**',
            approved=False
        )

    def test_admin_can_approve_showcase(self):
        # ✅ Login as admin
        login_success = self.client.login(username='admin', password='adminpass')
        self.assertTrue(login_success, "Admin login failed")

        # ✅ Build and print reverse URL
        url = reverse('approve_showcase', args=[self.showcase.id])
        print("TEST URL:", url)

        # ✅ Post approval
        response = self.client.post(url, {'coins': 200})
        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE CONTENT:", response.content.decode())

        # ✅ Refresh and assert
        self.showcase.refresh_from_db()
        self.profile = Profile.objects.get(user=self.dev)


        self.assertTrue(self.showcase.approved)
        self.assertEqual(self.showcase.coins_award, 200)
        self.assertEqual(self.profile.coins, 200)
        self.assertEqual(self.profile.tier, 'Contributor')
class ShowcaseRejectionTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True,
            is_superuser=True
        )

        self.dev = User.objects.create_user(
            username='dev',
            password='devpass',
            email='dev@paycorp.local'
        )

        self.profile = Profile.objects.get(user=self.dev)

        self.showcase = Showcase.objects.create(
            owner=self.profile,
            title='Unapproved Showcase',
            body_md='Something here...',
            approved=False
        )

    def test_admin_can_reject_showcase(self):
        login_success = self.client.login(username='admin', password='adminpass')
        self.assertTrue(login_success)

        url = reverse('reject_showcase', args=[self.showcase.id])
        response = self.client.post(url, {'reason': 'Inappropriate content'})

        self.showcase.refresh_from_db()

        self.assertFalse(self.showcase.approved)
        self.assertEqual(self.showcase.admin_note, 'Inappropriate content')
        self.assertEqual(self.profile.coins, 0)
class LeaderboardTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create 3 users with different coins and join dates
        self.u1 = User.objects.create_user(username='early_low', password='pass')
        self.p1 = Profile.objects.get(user=self.u1)
        self.p1.coins = 100
        self.p1.joined = timezone.now() - timedelta(days=10)
        self.p1.save()

        self.u2 = User.objects.create_user(username='late_high', password='pass')
        self.p2 = Profile.objects.get(user=self.u2)
        self.p2.coins = 200
        self.p2.joined = timezone.now()
        self.p2.save()

        self.u3 = User.objects.create_user(username='early_high', password='pass')
        self.p3 = Profile.objects.get(user=self.u3)
        self.p3.coins = 200
        self.p3.joined = timezone.now() - timedelta(days=5)
        self.p3.save()

    def test_leaderboard_sorting(self):
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)

        profiles = list(response.context['profiles'])

        # Sorted by coins DESC, then joined ASC
        expected_order = ['early_high', 'late_high', 'early_low']
        actual_order = [p.user.username for p in profiles]

        self.assertEqual(actual_order, expected_order)
class ShowcaseMarkdownRenderingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='dev', password='pass')
        self.profile = Profile.objects.get(user=self.user)

        self.showcase = Showcase.objects.create(
            owner=self.profile,
            title="Markdown Test",
            body_md="**Bold Text**\n\n# Heading 1",
            approved=True
        )

    def test_markdown_is_rendered_to_html(self):
        url = reverse('showcase_detail', args=[self.showcase.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        html = response.content.decode()

        # Check if markdown was rendered
        self.assertIn("<strong>Bold Text</strong>", html)
        self.assertIn("<h1>Heading 1</h1>", html)
class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='vaish', password='testpass')
        self.profile = Profile.objects.get(user=self.user)
        self.profile.coins = 300
        self.profile.update_tier()
        self.profile.save()

        # Create a few showcases
        Showcase.objects.create(
            owner=self.profile,
            title='Showcase One',
            body_md='**Content One**',
            approved=True
        )
        Showcase.objects.create(
            owner=self.profile,
            title='Showcase Two',
            body_md='# Heading Two',
            approved=True
        )

    def test_profile_page_shows_correct_info(self):
        login_success = self.client.login(username='vaish', password='testpass')
        self.assertTrue(login_success)

        url = reverse('profile')
        response = self.client.get(url)
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('vaish', html)
        self.assertIn('300', html)  # coin count
        self.assertIn('Contributor', html)  # tier from coins
        self.assertIn('Showcase One', html)
        self.assertIn('Showcase Two', html)
class ShowcaseFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dev', password='devpass')
        self.profile = Profile.objects.get(user=self.user)

    def test_valid_showcase_submission(self):
        self.client.login(username='dev', password='devpass')
        url = reverse('add_showcase')
        data = {
            'title': 'Valid Showcase',
            'body_md': '**Valid content**',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Showcase.objects.filter(title='Valid Showcase').exists())

    def test_invalid_submission_missing_title(self):
        self.client.login(username='dev', password='devpass')
        url = reverse('add_showcase')
        data = {
            'title': '',
            'body_md': 'This has no title',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFormError(form, 'title', 'This field is required.')

    def test_invalid_submission_missing_body(self):
        self.client.login(username='dev', password='devpass')
        url = reverse('add_showcase')
        data = {
            'title': 'Missing Body',
            'body_md': '',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFormError(form, 'body_md', 'This field is required.')

    def test_body_too_short_validation(self):  # ✅ now at top-level
        self.client.login(username='dev', password='devpass')
        url = reverse('add_showcase')
        data = {
            'title': 'Too Short',
            'body_md': 'This showcase has valid content.',
        }
        response = self.client.post(url, data)
        form = response.context['form']
        self.assertFormError(form, 'body_md', 'Body must be at least 5 words long.')
