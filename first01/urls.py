from django.urls import path
from first01 import views

urlpatterns = [
    path('snippets/', views.snippet_list, name="list"),
    path("snippets/<int:pk>/", views.snippet_detail, name="detail"),
]
