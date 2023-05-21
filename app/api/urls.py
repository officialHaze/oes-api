from django.urls import path
from . import views

urlpatterns = [path("scrap-emails/", views.scrap_email)]
