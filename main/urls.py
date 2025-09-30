from django.urls import path
from main.views import show_main
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_redirect, name='home'),

    # Login
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # XML/JSON + by id (Data delivery)
    path("products/json/", views.products_json, name="products_json"),
    path("products/xml/", views.products_xml, name="products_xml"),
    path("products/json/<int:id>/", views.product_json_by_id, name="product_json_by_id"),
    path("products/xml/<int:id>/", views.product_xml_by_id, name="product_xml_by_id"),
    
    # Add, Edit, Delete, Search
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:pk>/edit/", views.edit_product, name="edit_product"),
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),
    path('products/filter/', views.product_filter_by_category, name='product_filter'),
]