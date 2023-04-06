from rest_framework import views, viewsets, generics
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# import re


# Create your views here.

from . import models
from . import serializers


class BaseViewClass:
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)


class FrameViewSet(BaseViewClass, viewsets.ModelViewSet):
    queryset = models.Frame.objects.order_by("-id")
    serializer_class = serializers.FrameSerializer


class PackagesList(BaseViewClass, viewsets.ModelViewSet):
    queryset = models.Package.objects.order_by("-id")
    serializer_class = serializers.PackageSerializer


class FountainViewSet(BaseViewClass, viewsets.ModelViewSet):
    queryset = models.Fountain.objects.all()
    serializer_class = serializers.FountainSerializer


class FountainSetMusic(BaseViewClass, generics.UpdateAPIView):
    queryset = models.Fountain.objects.all()
    serializer_class = serializers.FountainMusicSerializer


class TextOutputViewSet(BaseViewClass, views.APIView):
    def get(self, request, fount_id, *args, **kwargs):
        if fount_id == 0:
            return HttpResponse("", status=status.HTTP_200_OK)

        the_fount = get_object_or_404(models.Fountain, pk=fount_id)
        try:
            packs = the_fount.packages.order_by("order")
            bits = []
            for pack in packs:
                the_frame = pack.frame

                if pack.is_reverse:
                    bit = the_frame.reverse_binary_code
                else:
                    bit = the_frame.binary_code

                bit = (
                    bit.replace("\n", "")
                    .replace(",", "")
                    .replace("[", "")
                    .replace("]", "")
                    .strip()
                )

                final_bits = ""
                for _ in range(pack.repeat):
                    final_bits += bit + " "

                bits.append(final_bits)

            response = HttpResponse(bits, content_type="text/plain; charset=UTF-8")
            response["Content-Disposition"] = "attachment; filename={0}".format(
                "bits.txt"
            )
            return response

        except Exception as e:
            return Response(
                {"detail": "Sth Went Wrong"}, status=status.HTTP_400_BAD_REQUEST
            )


# class TextOutputViewSet(BaseViewClass, views.APIView):
#     def get(self, request, fount_id, *args, **kwargs):
#         if fount_id == 0:
#             return HttpResponse("", status=status.HTTP_200_OK)

#         the_fount = get_object_or_404(models.Fountain, pk=fount_id)
#         packs = the_fount.packages.order_by("order")
#         try:
#             bits = []

#             for pack in packs:
#                 bit = (
#                     pack.frame.reverse_binary_code
#                     if pack.is_reverse
#                     else pack.frame.binary_code
#                 )
#                 bit = "".join(bit.split())  # remove all whitespace characters
#                 bit = "".join(bit.split(","))  # remove all , characters
#                 bit = "".join(bit.split("["))  # remove all [ characters
#                 bit = "".join(bit.split("]"))  # remove all ] characters
#                 bit = bit.strip()

#                 # bit = re.sub(r"[\s,\[\]]+", "", bit)
#                 bits.append(bit * pack.repeat)

#             response = HttpResponse(
#                 "\n".join(bits), content_type="text/plain; charset=UTF-8"
#             )
#             response["Content-Disposition"] = "attachment; filename=bits.txt"
#             return response
#         except Exception as e:
#             return Response(
#                 {"detail": "Sth Went Wrong"}, status=status.HTTP_400_BAD_REQUEST
#             )
