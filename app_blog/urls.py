from django.urls import path
from app_blog import views

app_name='blog'

urlpatterns = [
    # path('', views.BlogListView.as_view(), name='list'),
    path('', views.blog_list, name='list'),
    path('tag/<slug:tag_slug>/', views.blog_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.blog_details, name='details'),
    path('comment/<int:pk>/', views.post_comment, name='comment'),
]