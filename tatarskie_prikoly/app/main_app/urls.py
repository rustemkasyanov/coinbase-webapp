from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', index, name='index'),
    
    path('register/', register, name='register'),
    path('login/', login, name='login'), 
    path('logout/', logout, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='auth/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='auth/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/reset_password_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/reset_password_complete.html'), name='password_reset_complete'),

    path('transaction_history/', transaction_history, name='transaction_history'),
    # path('transaction_history/delete/<str:pk>', delete_transaction_history, name='delete_transaction_history'),
    path('transaction_history/delete', delete_transaction_history, name='delete_transaction_history'),

    path('regular_trade/', trade_regular_trade, name='trade_regular_trade'),
    
    path('settings/', settings, name='settings'),
    path('settings/ticker/add', add_ticker, name='add_ticker'),
    path('settings/ticker/delete', delete_ticker, name='delete_ticker'),
]