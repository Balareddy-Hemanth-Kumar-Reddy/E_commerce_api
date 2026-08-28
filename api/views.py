from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductSerializer, RegisterSerializer
from .models import Product, Cart, CartItem
from .serializers import (
    ProductSerializer,
    RegisterSerializer,
    CartSerializer,
)

@api_view(["POST"])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "username": user.username,
                "email": user.email
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
def hello(request):

    return Response({
        "message": "E-Commerce API is working!"
    })


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Product, Cart, CartItem
from .serializers import (
    ProductSerializer,
    RegisterSerializer,
    CartSerializer,
)


@api_view(["POST"])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
def hello(request):

    return Response({
        "message": "E-Commerce API is working!"
    })


@api_view(["GET", "POST"])
def products(request):

    # GET → Public
    if request.method == "GET":

        products = Product.objects.all()

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

    # POST → Authentication required
    if request.method == "POST":

        if not request.user.is_authenticated:

            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):

    try:
        product = Product.objects.get(pk=pk)

    except Product.DoesNotExist:

        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # GET → Public
    if request.method == "GET":

        serializer = ProductSerializer(product)

        return Response(serializer.data)

    # PUT / DELETE → Authentication required
    if not request.user.is_authenticated:

        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # PUT → Update
    if request.method == "PUT":

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DELETE → Delete
    if request.method == "DELETE":

        product.delete()

        return Response(
            {"message": "Product deleted successfully"}
        )


@api_view(["GET", "POST"])
def cart(request):

    # JWT required
    if not request.user.is_authenticated:

        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Get or create user's cart
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    # GET → View cart
    if request.method == "GET":

        serializer = CartSerializer(cart)

        return Response(serializer.data)

    # POST → Add product to cart
    if request.method == "POST":

        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        try:
            quantity = int(quantity)

        except (TypeError, ValueError):

            return Response(
                {"error": "Quantity must be a number"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:

            return Response(
                {"error": "Quantity must be at least 1"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if quantity > product.stock:

            return Response(
                {"error": "Not enough stock"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "quantity": quantity
            }
        )

        # Product already exists in cart
        if not created:

            new_quantity = (
                cart_item.quantity + quantity
            )

            if new_quantity > product.stock:

                return Response(
                    {"error": "Not enough stock"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            cart_item.quantity = new_quantity
            cart_item.save()

        serializer = CartSerializer(cart)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
    if request.method == "GET":

        serializer = CartSerializer(cart)

        return Response(serializer.data)

    if request.method == "POST":

        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > product.stock:
            return Response(
                {"error": "Not enough stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "quantity": quantity
            }
        )

        if not created:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                return Response(
                    {"error": "Not enough stock"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = new_quantity
            cart_item.save()

        serializer = CartSerializer(cart)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):

    try:
        product = Product.objects.get(pk=pk)

    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET → Public
    if request.method == "GET":

        serializer = ProductSerializer(product)

        return Response(serializer.data)

    # PUT / DELETE → Authentication required
    if not request.user.is_authenticated:

        return Response(
            {"error": "Authentication required"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # PUT → Update product
    if request.method == "PUT":

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE → Delete product
    if request.method == "DELETE":

        product.delete()

        return Response(
            {"message": "Product deleted successfully"}
        )