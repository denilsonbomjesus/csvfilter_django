from django.db import models

class CSVFile(models.Model):
    csv_file_1 = models.FileField(upload_to='csv_files/', null=True, blank=True)
    csv_file_2 = models.FileField(upload_to='csv_files/', null=True, blank=True)
    result_file = models.FileField(upload_to='csv_files/', null=True, blank=True)
