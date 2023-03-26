from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name="login"),
    path('login/', user_login, name="login_request"),
    path('register/', register, name="register"),
    path('logout/', user_logout, name='logout_request'),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('profile-update/', profile_update_view, name="profile_update"),
    path('activity-log/', activity_log_view, name="activity_log"),
    path('waste-list/', waste_list_view, name="waste_list"),
    path('venue-list/', venue_list_view, name="venue_list"),
    path('task-list/', task_list_view, name="task_list"),
    path('waste-create/', waste_create_view, name="waste_create"),
    path('waste-update/<int:pk>/', waste_update_view, name="waste_update"),
    path('waste-delete/<int:pk>/', waste_delete_view, name="waste_delete"),


    path('api/get-recommendation/', get_recommendation, name="get_recommendation"),
    path('api/get-all-venues-locations/', get_all_venues_locations, name="get_all_venues_locations"),
]
