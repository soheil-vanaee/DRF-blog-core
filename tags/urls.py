from django.urls import path
from . import views

urlpatterns = [
    path('', views.TagListView.as_view(), name='tag-list'),
    path('<int:pk>/', views.TagDetailView.as_view(), name='tag-detail'),
]