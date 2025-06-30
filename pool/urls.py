from django.urls import path
from .views import *

urlpatterns = [
    path('add_new_pool/', PoolView.as_view(), name='add_new_pool'),
    path('all_pool/', PoolView.as_view(), name='all_pool'),
    path('all_pool/', MyPoolView.as_view(), name='all_pool'),
    path('my_pool/', MyPoolView.as_view(), name='my_pool'),
    path('update_pool/<int:pk>/', PoolView.as_view(), name='update_pool'),
    path('delete_pool/<int:pk>/', PoolView.as_view(), name='delete_pool'),
    path('pool/<int:pk>/', PoolView.as_view(), name='pool_detail'),



    path('join_pool/<int:pk>/', PoolJoinView.as_view(), name='join_pool'),
    path('all_pool_member/<int:pk>/', PoolJoinView.as_view(), name='all_pool_member'),
    path('single_pool_member/<int:pk>/', PoolMemberDetailView.as_view(), name='single_pool_member'),
    path('leave_pool/<int:pk>/', PoolMemberDetailView.as_view(), name='leave_pool'),
    path('become_driver/<int:pk>/', BecomeDriverView.as_view(), name='become_driver'),

    path('approved_decline_request/<int:pk>/', PoolMemberDetailView.as_view(), name='approved_decline_request'),
    path('all_pending_members/', PendingMemberView.as_view(), name='all_pending_members'),
    path('perticipate_pool/', JoinedPoolsView.as_view(), name='perticipate_pool'),

    path('children_location/', ChildrenAndLocationView.as_view(), name='children_location'),

]