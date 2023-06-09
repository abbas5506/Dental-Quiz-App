from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/register', views.register, name="register"),
    path('all_Category', views.all_Category, name="all_Category"),
    path('category-questions/<int:cat_id>', views.category_questions, name="category_questions"),
    path('submit-answer/<int:cat_id>/<int:quest_id>', views.submit_answer, name="submit_answer"),
    path('result', views.result, name="result"),
    path('resultcard', views.resultcard, name="resultcard"),
    path('portfolio/', views.portfolio, name='portfolio'),

    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
         template_name='/Users/inzamamulhaq/Documents/quizApp/main/templates/registration/password_reset.html'), 
         name='password_reset'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
         template_name='/Users/inzamamulhaq/Documents/quizApp/main/templates/registration/password_reset_done.html'),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>', 
         auth_views.PasswordResetConfirmView.as_view(
         template_name='/Users/inzamamulhaq/Documents/quizApp/main/templates/registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    
    path('password-reset-complete', 
         auth_views.PasswordResetCompleteView.as_view(
         template_name='/Users/inzamamulhaq/Documents/quizApp/main/templates/registration/password_reset_complete.html'),
         name='password_reset_complete')
     
]

# To access the media folder inside the main APP
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)