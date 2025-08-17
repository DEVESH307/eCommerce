from django.urls import path
from products import views

urlpatterns = [
    # ------------------- Test -------------------
    path('hello/', views.hello_world, name='hello_world'),

    # ------------------- Product APIs -------------------
    path('products/', views.get_products, name='get_products'),              # GET all
    path('product/<int:id>/', views.get_product, name='get_product_by_id'),  # GET by ID
    path('product/', views.create_product, name='create_product'),           # POST create
    path('product/<int:id>/replace/', views.replace_product, name='replace_product'),  # PUT
    path('product/<int:id>/update/', views.update_product, name='update_product'),    # PATCH
    path('product/<int:id>/delete/', views.delete_product, name='delete_product'),    # DELETE

    # ------------------- Category APIs -------------------
    path('categories/', views.get_categories, name='get_categories'),              # GET all
    path('category/<int:id>/', views.get_category, name='get_category_by_id'),     # GET by ID
    path('category/', views.create_category, name='create_category'),              # POST
    path('category/<int:id>/replace/', views.replace_category, name='replace_category'),  # PUT
    path('category/<int:id>/update/', views.update_category, name='update_category'),    # PATCH
    path('category/<int:id>/delete/', views.delete_category, name='delete_category'),    # DELETE

    # ------------------- Order APIs -------------------
    path('orders/', views.get_orders, name='get_orders'),              # GET all
    path('order/<int:id>/', views.get_order, name='get_order_by_id'),  # GET by ID
    path('order/', views.create_order, name='create_order'),           # POST
    path('order/<int:id>/replace/', views.replace_order, name='replace_order'),  # PUT
    path('order/<int:id>/update/', views.update_order, name='update_order'),    # PATCH
    path('order/<int:id>/delete/', views.delete_order, name='delete_order'),    # DELETE
]
