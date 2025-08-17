from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from products.customException import ProductOutOfStockException
from products.models import Products, Category, Orders
from products.serializers import ProductSerializer, CategorySerializer, OrderSerializer


# Create your views here.
def hello_world(request):
    # print(request)
    data = Products.objects.all()
    d = data[0]
    print(d.name)
    d.name = "ABC"
    d.save()
    data = Products.objects.all()
    print(data[0].name)
    return HttpResponse("Hello, world!")

# # GET: to retrieve data from the server
# /products/1 -> returns the product with ID 1
# # POST: to send data to the server, often resulting in a change in state
# /products/create -> creates a new product
# # PUT: to update existing data on the server
# /products/1 -> updates the product with ID 1
# # DELETE: to remove data from the server
# /products/1 -> deletes the product with ID 1
# # PATCH: to apply partial modifications to a resource on the server
# /products/1 -> partially updates the product with ID 1

# ------------------- Product APIs -------------------
# GET all products
@api_view(['GET'])
def get_products(request):
    data = Products.objects.all()
    serializedProducts = ProductSerializer(data, many=True)
    return Response(serializedProducts.data)


# GET a single product
@api_view(['GET'])
def get_product(request, id):
    try:
        print("open DB connection...")
        # data = Products.objects.get(id=id)
        data = Products.objects.filter(id=id).first()
        if not data:
            raise ProductOutOfStockException("Product is out of stock")
        print(data)
        # print("close DB connection 1...Wrong way to close DB connection")
        serializedProduct = ProductSerializer(data)
        return Response(serializedProduct.data)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ProductOutOfStockException as e:
        # try:
        #     raise Exception()
        # except Exception as e:
        #     print("Close DB connection 2...Wrong way to close DB connection")

        print(1)
        print(e)
        # print("close DB connection 3...Wrong way to close DB connection")

        # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            raise Products.DoesNotExist()
        except Products.DoesNotExist:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # try:
        #     raise Exception()
        # except Exception as e:
        #     print("Close DB connection 4...Wrong way to close DB connection")
        print(2)
        # print("close DB connection 5...Wrong way to close DB connection")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        print("close DB connection 6...Right way to close DB connection")

    # try:
    #     product = Products.objects.get(id=id)
    # except Exception as e:
    #     print(e)
    # else:
    #     print("else block executed: when no exception occurs")
    # finally:
    #     print("Finally block executed: DB connection closed")


# POST - create product
@api_view(['POST'])
def create_product(request):
    try:
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PUT - full update
@api_view(['PUT'])
def replace_product(request, id):
    try:
        product = Products.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data)  # no partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Products.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PATCH - update product (partial update)
@api_view(['PATCH'])
def update_product(request, id):
    try:
        product = Products.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Products.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# DELETE - delete product
@api_view(['DELETE'])
def delete_product(request, id):
    try:
        product = Products.objects.get(id=id)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Products.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------- Category APIs -------------------
# GET all categories
@api_view(['GET'])
def get_categories(request):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# GET single category by ID
@api_view(['GET'])
def get_category(request, id):
    try:
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# POST create category
@api_view(['POST'])
def create_category(request):
    try:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PUT (replace category)
@api_view(['PUT'])
def replace_category(request, id):
    try:
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category, data=request.data)  # full update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PATCH (partial update)
@api_view(['PATCH'])
def update_category(request, id):
    try:
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category, data=request.data, partial=True)  # partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# DELETE category
@api_view(['DELETE'])
def delete_category(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------- Orders APIs -------------------
# GET all orders
@api_view(['GET'])
def get_orders(request):
    try:
        orders = Orders.objects.prefetch_related('products').all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# GET single order by ID
@api_view(['GET'])
def get_order(request, id):
    try:
        order = Orders.objects.prefetch_related('products').get(id=id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Orders.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# POST create order
@api_view(['POST'])
def create_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PUT replace an order (full update)
@api_view(['PUT'])
def replace_order(request, id):
    try:
        order = Orders.objects.get(id=id)
        serializer = OrderSerializer(order, data=request.data)  # full update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Orders.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PATCH partial update
@api_view(['PATCH'])
def update_order(request, id):
    try:
        order = Orders.objects.get(id=id)
        serializer = OrderSerializer(order, data=request.data, partial=True)  # partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Orders.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# DELETE order
@api_view(['DELETE'])
def delete_order(request, id):
    try:
        order = Orders.objects.get(id=id)
        order.delete()
        return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Orders.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
