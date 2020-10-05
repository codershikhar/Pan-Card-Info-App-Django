from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PanInfoSerializer, FileSerializer
import traceback
from . import util
from .models import PanInfo


class FileUploadView(APIView):
    authentication_classes = []

    def get(self, request):
        try:
            page_count = int(request.GET.get('pageCount', 10))
            page_number = int(request.GET.get('pageNumber', 1))
            pan_info_list = PanInfo.objects.all()[page_number*page_count: (page_number+1)*page_count]
            count = PanInfo.objects.count()
            serializer = PanInfoSerializer(pan_info_list, many=True)
            return Response({'data': serializer.data, 'count': count}, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()

            try:
                pan_info = util.extract_data(file_serializer.data['file'])
                pan_info.pan_file_id = file_serializer.data['id']
                pan_info.save()
                pan_info_serializer = PanInfoSerializer(pan_info)
                print(pan_info_serializer.data)
                return Response(pan_info_serializer.data, status=status.HTTP_201_CREATED)
            except:
                traceback.print_exc()

            return Response({"message": "Error Extracting Data: Image Improper"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
