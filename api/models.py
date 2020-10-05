from django.db import models


class File(models.Model):
    file = models.FileField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'file'


class PanInfo(models.Model):
    full_name = models.TextField(null=True, blank=True)
    fathers_name = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    pan_number = models.TextField(null=True, blank=True)
    scanned_signature = models.FileField(null=True, blank=True)
    photo = models.FileField(null=True, blank=True)
    pan_file = models.ForeignKey(File, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pan_info'
