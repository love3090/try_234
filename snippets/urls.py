from django.urls import path
from snippets import views

app_name = "snippets"

urlpatterns = [
#    path('snippets/', views.snippet_list, name="list"),
    path('snippets/', views.SnippetList.as_view(), name='snippet_list'),
#    path("snippets/<int:pk>/", views.snippet_detail, name="detail"),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet_detail'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
]
