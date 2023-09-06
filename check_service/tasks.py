import pdfkit

from celery import shared_task
from django.template.loader import render_to_string

from check_service.models import Check


@shared_task
def generate_pdf(check_id):
    check = Check.objects.get(pk=check_id)
    order_id = check.order.get(
        "order_id"
    )
    file_name = f"{order_id}_{check.type}.pdf"
    file_path = f"media/pdf/{file_name}"

    rendered_html = render_to_string(
        "check_template.html", {"order": check.order}
    )

    pdfkit.from_string(rendered_html, file_path)

    check.pdf_file = file_path
    check.status = "rendered"
    check.save()
