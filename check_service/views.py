import json

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from .models import Printer, Check
from .tasks import generate_pdf
import os


class NewOrderView(View):
    def post(self, request, *args, **kwargs):
        order_data = json.loads(request.body)

        point_id = order_data.get("point_id")
        printers = Printer.objects.filter(point_id=point_id)

        if not printers.exists():
            return JsonResponse({"error": "No printer for this point"}, status=400)

        order_number = order_data.get("order_number")
        existing_check = Check.objects.filter(order__order_number=order_number)

        if existing_check.exists():
            return JsonResponse(
                {"error": "Checks for this order already exist"}, status=400
            )


        for printer in printers:
            new_check = Check.objects.create(
                printer=printer, type=printer.check_type, order=order_data
            )
            generate_pdf.delay(
                new_check.id
            )

        return JsonResponse({"status": "success"})


class ChecksForPrinterView(View):
    def get(self, request, api_key, *args, **kwargs):
        try:
            printer = Printer.objects.get(api_key=api_key)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Printer not found"}, status=404)

        checks = Check.objects.filter(printer=printer, status="rendered")
        serialized_checks = [
            {"id": check.id, "pdf_url": check.pdf_file.url} for check in checks
        ]

        return JsonResponse({"checks": serialized_checks})


class DownloadPDFView(View):
    def get(self, request, check_id, *args, **kwargs):
        try:
            check = Check.objects.get(pk=check_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Check not found"}, status=404)

        file_path = check.pdf_file.path
        with open(file_path, "rb") as pdf:
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = f"inline;filename={os.path.basename(file_path)}"
            return response
