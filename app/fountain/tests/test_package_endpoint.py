from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.views import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from fountain import models


def create_user(phone, password):
    """Helper Function To Create a User"""
    return get_user_model().objects.create(phone=phone, password=password)


class PublicTest(APITestCase):
    """Tests Which Does Not Need User To Be Authenticated"""

    def setUp(self):
        self.client = APIClient()

    def test_return_unauthorized(self):
        """Test if user is unauthorized"""
        url = reverse("fountain:package-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PackagesTest(APITestCase):
    def setUp(self):
        user = create_user("09151498722", "admin")
        self.client = APIClient()
        self.client.force_authenticate(user)

    def test_list_packages(self):
        # Create some packages
        frame_1 = models.Frame.objects.create(title="Frame 1")
        frame_2 = models.Frame.objects.create(title="Frame 2")
        p1 = models.Package.objects.create(order=1, repeat=2, frame=frame_1)
        p2 = models.Package.objects.create(order=2, repeat=4, frame=frame_2)

        # Call the endpoint to list packages
        url = reverse("fountain:package-list")
        response = self.client.get(url)

        # Expect status code 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Expect the right number of packages in the response
        self.assertEqual(len(response.data), 2)

        self.assertEqual(p1.frame, frame_1)
        self.assertEqual(p2.frame, frame_2)
