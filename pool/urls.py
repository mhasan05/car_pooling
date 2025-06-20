from django.urls import path
from .views import *

urlpatterns = [
    path('add_new_pool/', PoolView.as_view(), name='add_new_pool'),
    path('all_pool/', PoolView.as_view(), name='all_pool'),
    path('update_pool/<int:pk>/', PoolView.as_view(), name='update_pool'),
    path('delete_pool/<int:pk>/', PoolView.as_view(), name='delete_pool'),
    path('pool/<int:pk>/', PoolView.as_view(), name='pool_detail'),



    path('join_pool/<int:pk>/', PoolJoinView.as_view(), name='join_pool'),
    path('all_pool_member/<int:pk>/', PoolJoinView.as_view(), name='all_pool_member'),
    path('single_pool_member/<int:pk>/', PoolMemberDetailView.as_view(), name='single_pool_member'),
    path('leave_pool/<int:pk>/', PoolMemberDetailView.as_view(), name='leave_pool'),
    path('become_driver/<int:pk>/', BecomeDriverView.as_view(), name='become_driver'),

]