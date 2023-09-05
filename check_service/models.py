from django.db import models


class Printer(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)
    CHECK_TYPE_CHOICES = [("kitchen", "Kitchen"), ("client", "Client")]
    check_type = models.CharField(max_length=7, choices=CHECK_TYPE_CHOICES)
    point_id = models.IntegerField()

    def __str__(self):
        return self.name


class Check(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=Printer.CHECK_TYPE_CHOICES)
    order = models.JSONField()
    STATUS_CHOICES = [("new", "New"), ("rendered", "Rendered"), ("printed", "Printed")]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="new")
    pdf_file = models.FileField(upload_to="media/pdf/")

    def __str__(self):
        return f"{self.type} - {self.status}"
