from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('', views.album_create, name='album_create'),
    path('exports/', views.files_list, name='files_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('uploaded/', views.show_all_uploaded_contents, name='uploaded_contents'),
]
