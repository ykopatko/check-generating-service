"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from check_service import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("new_order/", views.NewOrderView.as_view(), name="new_order"),
    path("checks/<str:api_key>/", views.ChecksForPrinterView.as_view(), name="checks_for_printer"),
    path("download_pdf/<int:check_id>/", views.DownloadPDFView.as_view(), name="download_pdf"),
]
