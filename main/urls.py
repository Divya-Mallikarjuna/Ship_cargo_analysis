from django.urls import path 
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
    path('page4/', views.page4, name='page4'),
    path('page5/', views.page5, name='page5'),
    path('page6/', views.page6, name='page6'),
    path('page7/', views.page7, name='page7'),
    path('page8/', views.page8, name='page8'),
    path('page9/', views.page9, name='page9'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('update_user/',views.update_user,name='update_user'),
    path('register/',views.register_user,name='register'),
    path('admin_dash/',views.admin_dash,name='admin_dash'),
    path('add_tables/',views.add_tables,name='add_tables'),
    path('card/',views.card,name='card'),
    path('shipment_details/',views.shipment_details,name='shipment_details'),
    path('user/', views.user_list, name='user_list'),
    path('user/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('user/<int:user_id>/toggle_status/', views.toggle_user_status, name='toggle_user_status'),
    path('delete_customer/', views.delete_customer, name='delete_customer'),
    path('view_shipments/',views.view_shipments, name='view_shipments'),
    path('confirmation/',views.confirmation,name='confirmation'),
    path('shipment_view/',views.shipment_view,name='shipment_view'),
    path('shipment_view/barchart/', views.barchart, name='barchart'),
    path('current_shipments/',views.current_shipments,name='current_shipments'),
    path('view_location/',views.view_location,name='view_location'),
    path('view_ship/',views.view_ship,name='view_ship'),
    path('calculate_shipping_rate/',views.calculate_shipping_rate,name='calculate_shipping_rate'),
    path('calculate_rate/',views.calculate_rate,name='calculate_rate'),
    path('ship_routes_news/',views.ship_routes_news,name='ship_routes_news'),
    path('route_analysis/',views.route_analysis,name='route_analysis'),
    path('update_tables/',views.update_tables,name='update_tables'),
    path('update_customer/',views.update_customer,name='update_customer'),
    path('update_ship/',views.update_ship,name='update_ship'),
    path('update_ware/',views.update_ware,name='update_ware'),
    path('update_sup/',views.update_sup,name='update_sup'),
    path('update_shipment/',views.update_shipment,name='update_shipment'),
    path('route_map/', views.route_map, name='route_map'),
    path('map/', views.map, name='map'),
    path('view_sup/',views.view_sup,name='view_sup'),
    path('view_route/',views.view_route,name='view_route'),
    path('view_ware/',views.view_ware,name='view_ware'),
    path('view_payments/',views.view_payments,name='view_payments'),
    path('view_package/',views.view_package,name='view_package'),

   








]