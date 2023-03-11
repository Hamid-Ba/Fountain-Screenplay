from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .. import models


class FrameTestCase(TestCase):
    def setUp(self):
        self.frame1 = models.Frame.objects.create(
            title="Frame 1",
            orginal_image=SimpleUploadedFile(name="test_image.jpg", content=b"content"),
        )
        self.frame2 = models.Frame.objects.create(
            title="Frame 2",
            orginal_image=SimpleUploadedFile(name="test_image.jpg", content=b"content"),
        )

    def tearDown(self):
        self.frame1.orginal_image.delete()
        self.frame2.orginal_image.delete()

    def test_frame_created(self):
        """Test if frame is created"""
        self.assertEqual(models.Frame.objects.all().count(), 2)

    def test_orginal_image_available(self):
        """Test if orginal image path is available"""
        self.assertTrue(self.frame1.orginal_image.url.endswith(".jpg"))

    def test_analyzed_image_not_required(self):
        """Test if analyzed image field is optional"""
        self.assertEqual(self.frame1.analyzed_image, None)
