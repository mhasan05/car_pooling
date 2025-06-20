from django.urls import path
from .views import *

urlpatterns = [
    path('add_new_child/', ChildrenView.as_view(), name='add_new_child'),
    path('all_child/', ChildrenView.as_view(), name='all_child'),
    path('update_child/<int:pk>/', ChildrenView.as_view(), name='update_child'),
    path('delete_child/<int:pk>/', ChildrenView.as_view(), name='delete_child'),
    path('child/<int:pk>/', ChildrenView.as_view(), name='child_detail'),

]