from django.urls import path
from .views import handle_file_upload

app_name = 'fileupload'
urlpatterns = [
    path('', handle_file_upload, name='file_upload'),
]
