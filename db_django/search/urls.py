from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='search'),
    path('api/user', views.user, name='user'),  # @api_view를 이용한 view
    path('api/user/<int:no>/', views.user_detail, name='who')
]
