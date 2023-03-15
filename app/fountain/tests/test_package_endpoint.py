from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse
from fountain import models

class PackagesTest(APITestCase):
    def test_list_packages(self):
        # Create some packages
        frame_1 = models.Frame.objects.create(title="Frame 1")
        frame_2 = models.Frame.objects.create(title="Frame 2")
        p1 = models.Package.objects.create(order=1, repeat=2,frame=frame_1)
        p2 = models.Package.objects.create(order=2, repeat=4,frame=frame_2)

        # Call the endpoint to list packages
        url = reverse("fountain:package-list")
        response = self.client.get(url)

        # Expect status code 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Expect the right number of packages in the response
        self.assertEqual(len(response.data), 2)
        
        self.assertEqual(p1.frame , frame_1)
        self.assertEqual(p2.frame , frame_2)
