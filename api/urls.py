from django.urls import path, include
from . import views


urlpatterns = [
    path("upload", views.BelegNumberList.as_view(), name="file_path"),
    path("entries", views.EntriesList.as_view()),
    path("entries/<int:bg>", views.EntryDetail.as_view())
]

