from django.test import TestCase
from .models import *
import datetime as dt
# Create your tests here.
class ProfileTestClass(TestCase):
    def setUp(self):
        self.profile = Profile(profile_pic = 'fuaad.png', main_user = 'photolee', bio = 'photo fo passports', followers = 0, following = 0)

    def tearDown(self):
        Profile.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save_profile(self):
        self.profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

    def test_delete_profile(self):
        self.profile.save_profile()
        Profile.delete_image(self.profile.id)
        profiles = Profile.objects.all()
        self.assertEqual(len(profiles), 0)

    def test_search_users(self):
        self.profile.save_profile()
        profile = Profile.search_users('photolee')
        self.assertEqual(profile, self.profile)

class ImageTestClass(TestCase):

    def setUp(self):
        self.profile = Profile(profile_pic = 'fuaad.png', main_user = 'photolee', bio = 'photo fo passports', followers = 0, following = 0)
        self.img = Image(image_path = 'fuaad.png', main_user = 'photolee', caption = 'photo fo passports', likes = 0, comments = 0, upload_date=dt.datetime.today())

    def tearDown(self):
        Profile.objects.all().delete()
        Image.objects.all().delete()

    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.img, Image))

    def test_save_image(self):
        self.img.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images) > 0)

    def test_delete_image(self):
        self.img.save_image()
        Image.delete_image(self.img.id)
        images = Image.objects.all()
        self.assertEqual(len(images), 0)

    def test_get_image_by_id(self):
        self.img.save_image()
        image = Image.get_image_by_id(self.img.id)
        self.assertEqual(self.img, image)

    def test_update_image(self):
        Image.update_image(self.img.id, 'fatma.png')
        self.assertEqual(self.img.image_path, 'fatma.png')
