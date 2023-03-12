from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .. import models


class FrameModelTest(TestCase):
    """Frame Model Test"""

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


class PackageModelTest(TestCase):
    """Package Model Test"""

    def setUp(self):
        self.frame = models.Frame.objects.create(title="My Frame")
        self.package = models.Package.objects.create(
            order=1, repeat=None, frame=self.frame
        )

    def test_package_creation(self):
        """Test that a package can be created"""
        initial_count = models.Package.objects.count()

        models.Package.objects.create(
            order=2,
            repeat=3,
            frame=self.frame,
        )

        self.assertEqual(models.Package.objects.count(), initial_count + 1)

    def test_package_order_field(self):
        """Test that the `order` field on a Package works correctly"""
        package = models.Package.objects.create(
            order=2,
            repeat=2,
            frame=self.frame,
        )
        self.assertEqual(package.order, 2)

    def test_package_repeat_field(self):
        """Test that the `repeat` field on a Package works correctly"""
        package = models.Package.objects.create(
            order=2,
            repeat=2,
            frame=self.frame,
        )
        self.assertEqual(package.repeat, 2)

    def test_package_frame_relation(self):
        """Test that the `frame` field on a Package works correctly"""
        package = models.Package.objects.create(
            order=2,
            repeat=2,
            frame=self.frame,
        )
        self.assertEqual(package.frame, self.frame)


class FountainModelTestCase(TestCase):
    def setUp(self):
        self.frame = models.Frame.objects.create(title="Test Frame")
        self.package = models.Package.objects.create(order=1, frame=self.frame)
        self.fountain = models.Fountain.objects.create(title="Test Fountain")

    def test_fountain_title(self):
        """Test Fountain title"""
        self.assertEqual(str(self.fountain), "Test Fountain")

    def test_fountain_packages(self):
        """Test Fountain packages"""
        self.fountain.packages.add(self.package)
        self.assertEqual(self.fountain.packages.count(), 1)
        self.assertIn(self.package, self.fountain.packages.all())

    def test_related_name(self):
        """Test related name of Fountain to Package"""
        self.fountain.packages.add(self.package)
        self.assertEqual(self.package.fountains.count(), 1)
        self.assertIn(self.fountain, self.package.fountains.all())
