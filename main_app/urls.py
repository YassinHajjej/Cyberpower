from django.urls import path
from. import views



urlpatterns = [
    

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('lessons/', views.lessons_index, name='index'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/create/', views.LessonCreate.as_view(), name='lessons_create'),
    path('lessons/<int:pk>/update/', views.LessonUpdate.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', views.LessonDelete.as_view(), name='lesson_delete'),
    path('search/', views.search, name='search'), 
    path('lesson/<int:lesson_id>/comment/create/', views.add_comment, name='comment_create'),
    path('comment_delete/<int:comment_id>/', views.delete_comment, name='comment_delete'),
    path('lessons/<int:lesson_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
    
]