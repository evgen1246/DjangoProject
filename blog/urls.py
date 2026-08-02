from django.urls import path

from . import views
from .apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="blogpost_list"),
    path("post/<int:pk>/", views.BlogPostDetailView.as_view(), name="blogpost_detail"),
    path("create/", views.BlogPostCreateView.as_view(), name="blogpost_create"),
    path("update/<int:pk>/", views.BlogPostUpdateView.as_view(), name="blogpost_update"),
    path("delete/<int:pk>/", views.BlogPostDeleteView.as_view(), name="blogpost_delete"),
]
