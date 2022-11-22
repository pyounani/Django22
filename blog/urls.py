from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('category/<str:slug>/', views.category_page),  #IP주소/blog/category/slug/
    path('tag/<str:slug>/', views.tag_page),

    #FBV
    #path('', views.index),
    #path('<int:pk>/', views.single_post_page)
]