from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('signup/', views.signup_view),
    path('user/<str:username>/', views.user_view),
    path('ticket/<int:id>/', views.ticket_detail, name='ticket'),
    path('ticket_edit/<int:id>/', views.ticket_edit),
    path('add_ticket/', views.add_ticket),
    path('claim_ticket/<int:id>/', views.claim_ticket),
    path('ticket_done/<int:id>/', views.ticket_done),
    path('ticket_invalid/<int:id>/', views.ticket_invalid)
]
