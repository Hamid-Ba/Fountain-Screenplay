from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from PIL import Image
import tempfile

from .. import models
from .. import serializers


def create_frame(title, orginal_image):
    """Helper Function To Create a Frame"""
    return models.Frame.objects.create(
        title=title,
        orginal_image=SimpleUploadedFile(name=orginal_image, content=b"content"),
    )


def create_user(phone, password):
    """Helper Function To Create a User"""
    return get_user_model().objects.create(phone=phone, password=password)


class PublicTest(TestCase):
    """Tests Which Does Not Need User To Be Authenticated"""

    def setUp(self):
        self.client = APIClient()

    def test_return_unauthorized(self):
        """Test if user is unauthorized"""
        url = reverse_lazy("fountain:frame-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class FrameTest(TestCase):
    """Frame API Tests"""

    def setUp(self):
        user = create_user("09151498722", "admin")
        self.frame_1 = None
        self.client = APIClient()
        self.client.force_authenticate(user)

    def tearDown(self):
        if self.frame_1:
            try:
                self.frame_1.orginal_image.delete()
            except FileNotFoundError:
                pass

        return super().tearDown()

    def test_list_frame_should_work_properly(self):
        """Test List Frame API"""
        self.frame_1 = models.Frame.objects.create(title="Frame 1")
        frame_2 = models.Frame.objects.create(title="Frame 2")

        res = self.client.get(reverse_lazy("fountain:frame-list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        frame_2.orginal_image.delete()

    def test_get_single_frame_should_work_properly(self):
        """Test Get Single Frame API"""
        self.frame_1 = create_frame("Frame 1", "frame1.png")

        url = reverse_lazy("fountain:frame-detail", args=(self.frame_1.id,))
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_frame_should_work_properly(self):
        """Test Create Frame API"""
        payload = {"title": "Frame 1"}
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload["orginal_image"] = image_file

            res = self.client.post(
                reverse_lazy("fountain:frame-list"),
                payload,
                format="multipart",
            )
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)

            self.frame_1 = models.Frame.objects.get(title="Frame 1")
            serialaizer = serializers.FrameSerializer(self.frame_1, many=False)
            self.assertEqual(serialaizer.data["id"], res.data["id"])

    def test_update_frame_should_work_properly(self):
        """Test Update Frame API"""
        self.frame_1 = create_frame("Frame 1", "frame1.png")
        payload = {
            "type": self.frame_1.type,
            "title": "Update Frame 1",
            "x_axis": self.frame_1.x_axis,
            "y_axis": self.frame_1.y_axis,
        }

        with tempfile.NamedTemporaryFile(suffix=".png") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="PNG")
            image_file.seek(0)
            payload["orginal_image"] = image_file

            self.frame_1.orginal_image.delete()
            res = self.client.put(
                reverse_lazy("fountain:frame-detail", args=(self.frame_1.id,)),
                payload,
                format="multipart",
            )

            self.assertEqual(res.status_code, status.HTTP_200_OK)

            self.frame_1.refresh_from_db()
            for key, value in payload.items():
                if key != "orginal_image":
                    self.assertEqual(getattr(self.frame_1, key), value)

    def test_patch_frame_should_work_properly(self):
        """Test Patch Frame API"""
        self.frame_1 = create_frame("Frame 1", "frame1.png")
        payload = {"title": "Update Frame 1"}

        url = reverse_lazy("fountain:frame-detail", args=(self.frame_1.id,))
        res = self.client.patch(url, payload, format="multipart")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.frame_1.refresh_from_db()

        for key, value in payload.items():
            self.assertEqual(getattr(self.frame_1, key), value)
