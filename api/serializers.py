from rest_framework import serializers
from .models import PanInfo, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class PanInfoSerializer(serializers.ModelSerializer):
    pan_file = FileSerializer(read_only=True)

    class Meta:
        model = PanInfo
        fields = "__all__"
