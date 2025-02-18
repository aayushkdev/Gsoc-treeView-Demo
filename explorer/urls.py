from django.urls import path
from django.views.generic import TemplateView
from .views import get_directory_structure, get_file_content

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),  # Add this line
    path("api/files/", get_directory_structure, name="get_directory_structure"),
    path("api/files/<path:file_path>/", get_file_content, name="get_file_content"),
]
