from django.urls import path
from .views import *

urlpatterns = [
    path('add_new_vehicle/', VehicleView.as_view(), name='add_new_vehicle'),
    path('all_vehicle/', VehicleView.as_view(), name='all_vehicle'),
    path('update_vehicle/<int:pk>/', VehicleView.as_view(), name='update_vehicle'),
    path('delete_vehicle/<int:pk>/', VehicleView.as_view(), name='delete_vehicle'),
    path('vehicle/<int:pk>/', VehicleView.as_view(), name='vehicle_detail'),

    # path('color_type/', VehicleColorTypeView.as_view(), name='color_type'),
    # path('color_type/<int:pk>/', VehicleColorTypeView.as_view(), name='color_type'),

]