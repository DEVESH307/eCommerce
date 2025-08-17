from django.db import models
from django.utils.timezone import datetime


# Create your models here.
class AuditData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Products(AuditData):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='products')


class Category(AuditData):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Orders(AuditData):
    customer_name = models.CharField(max_length=255)
    products = models.ManyToManyField(Products, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


# TODO: SELECT related `select_related` (LEFT OUTER JOIN) : I need x data in few seconds, get it right away.. 1xm , 1:1
# select_related worked with 1:1, 1:m, and m:1 relationships (ForeignKey, OneToOneField).
# N+1 Problem: When you access the related data, it will hit the database for each related object.
# This can lead to performance issues if you have a lot of related objects.
# Using `select_related` or `prefetch_related` can help avoid this problem by fetching related data in a single query or fewer queries.
# `select_related` is used for single-valued relationships (ForeignKey, OneToOneField) and performs a SQL join.
# TODO: CREATE MxM table, for product and orders
# FOR MxM : `prefetch_related`
# Order.objects.prefetch_related('products').all()
# `prefetch_related` is used for multi-valued relationships (ManyToManyField, reverse ForeignKey) and performs a separate query to fetch related objects.
# It then combines the results in Python, which is more efficient for large datasets.
# Example: If you have a `Product` model and an `Order` model with a ManyToMany relationship, you can use `prefetch_related` to fetch all products related to each order in a single query.

# ## **1. `select_related` Example**
#
# This is for **single-valued relationships** (ForeignKey, OneToOneField).
# Here, `Products` → `Category` is a **ForeignKey**.
#
# ```python
# # models.py reference
# # Products.category = models.ForeignKey(Category, ...)
#
# from products.models import Products
#
# # Without select_related: This will cause N+1 queries
# for p in Products.objects.all():
#     print(p.name, p.category.name)  # Every loop hits the DB again
#
# # With select_related: Fetch category in the same query
# products = Products.objects.select_related('category').all()
# for p in products:
#     print(p.name, p.category.name)  # No extra queries
# ```
#
# 📌 `select_related` uses **SQL JOIN** to grab `Products` and `Category` in one query.
#
# ---
#
# ## **2. `prefetch_related` Example**
#
# This is for **multi-valued relationships** (ManyToMany, reverse ForeignKey).
# Here, `Orders` ↔ `Products` is a **ManyToMany**.
#
# ```python
# from products.models import Orders
#
# # Without prefetch_related: N+1 queries when looping products
# for order in Orders.objects.all():
#     for p in order.products.all():
#         print(order.customer_name, p.name)
#
# # With prefetch_related: Products are fetched in a separate query and joined in Python
# orders = Orders.objects.prefetch_related('products').all()
# for order in orders:
#     print(order.customer_name)
#     for p in order.products.all():
#         print("  -", p.name)
# ```
#
# 📌 `prefetch_related` fetches **Orders** and **Products** in **two queries** total,
# then matches them in Python — avoiding one query per order.
#
# ---
#
# ## **3. Combining Both**
#
# If you want to get:
#
# * Orders → Products (ManyToMany) → Category (ForeignKey)
#   You can do this:
#
# ```python
# orders = Orders.objects.prefetch_related(
#     'products__category'  # prefetch products and their category
# ).all()
#
# for order in orders:
#     print(f"Order by {order.customer_name}")
#     for p in order.products.all():
#         print(f"  - {p.name} ({p.category.name})")
# ```
#
# This:
#
# * Prefetches products for each order
# * Prefetches category for each product in **one extra query** instead of per product
#
#
