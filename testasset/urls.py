from django.urls import path, include
from . import views



urlpatterns = [
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
  
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),
    path('home/', views.home, name="home"),
    path('assets/', views.assets, name='assets'),
    path('create_asset/', views.createAsset, name='create_asset'),
    path('update_asset/<str:pk>', views.updateAsset, name='update_asset'),
    path('delete_asset/<str:pk>', views.deleteAsset, name='delete_asset'),
    path('import_asset/', views.importExcelAsset, name='import_asset'), 

    path('add_categories/', views.addCategories, name='add_categories'), 
    path('add_department/', views.addDepartment, name='add_department'), 

    # path('view_details/<str:code>',views.view_details,name='view-details'),
    # path('view_details',views.view_details,name='scanned-code'),
    path('scanner',views.viewScanner,name='view-scanner'),


    path('all_staffs/', views.allStaffs, name='all_staffs'),
    path('create_staff/', views.createStaff, name='create_staff'),
    path('update_staff/<str:pk>', views.updateStaff, name='update_staff'),
    path('staff/<str:pk>', views.staff, name='staff'),
    path('import_staff/', views.importExcelStaff, name='import_staff'),

    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<str:pk>', views.event, name='event_edit'),

    # path('assign_asset/<str:pk>', views.assignAsset, name='assign_asset'),
    # path('update_assign_asset/<str:pk>', views.updateAssignAsset, name='update_assign_asset'),
    # path('delete_assign_asset/<str:pk>', views.deleteAssignAsset, name='delete_assign_asset'),
]


