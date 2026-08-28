from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Product, Cart, CartItem
from .serializers import (
    ProductSerializer,
    RegisterSerializer,
    CartSerializer,
)


# =========================
# USER REGISTRATION
# =========================

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


# =========================
# HELLO API
# =========================

@api_view(["GET"])
def hello(request):

    return Response(
        {
            "message": "E-Commerce API is working!"
        }
    )


# =========================
# PRODUCTS
# =========================

@api_view(["GET", "POST"])
def products(request):

    # -------------------------
    # GET ALL PRODUCTS
    # -------------------------

    if request.method == "GET":

        products = Product.objects.all()

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

    # -------------------------
    # CREATE PRODUCT
    # -------------------------

    if request.method == "POST":

        if not request.user.is_authenticated:

            return Response(
                {
                    "error": "Authentication required"
                },
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


# =========================
# SINGLE PRODUCT
# =========================

@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):

    try:

        product = Product.objects.get(pk=pk)

    except Product.DoesNotExist:

        return Response(
            {
                "error": "Product not found"
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -------------------------
    # GET PRODUCT
    # -------------------------

    if request.method == "GET":

        serializer = ProductSerializer(
            product
        )

        return Response(serializer.data)

    # -------------------------
    # AUTHENTICATION
    # -------------------------

    if not request.user.is_authenticated:

        return Response(
            {
                "error": "Authentication required"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # -------------------------
    # UPDATE PRODUCT
    # -------------------------

    if request.method == "PUT":

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -------------------------
    # DELETE PRODUCT
    # -------------------------

    if request.method == "DELETE":

        product.delete()

        return Response(
            {
                "message": "Product deleted successfully"
            }
        )


# =========================
# CART
# =========================

@api_view(["GET", "POST"])
def cart(request):

    # -------------------------
    # AUTHENTICATION
    # -------------------------

    if not request.user.is_authenticated:

        return Response(
            {
                "error": "Authentication required"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # -------------------------
    # GET OR CREATE CART
    # -------------------------

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    # -------------------------
    # GET CART
    # -------------------------

    if request.method == "GET":

        serializer = CartSerializer(
            cart
        )

        return Response(
            serializer.data
        )

    # -------------------------
    # ADD PRODUCT TO CART
    # -------------------------

    if request.method == "POST":

        product_id = request.data.get(
            "product"
        )

        quantity = request.data.get(
            "quantity",
            1
        )

        # Validate quantity
        try:

            quantity = int(quantity)

        except (TypeError, ValueError):

            return Response(
                {
                    "error": "Quantity must be a number"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:

            return Response(
                {
                    "error": "Quantity must be at least 1"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find product
        try:

            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            return Response(
                {
                    "error": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check stock
        if quantity > product.stock:

            return Response(
                {
                    "error": "Not enough stock"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "quantity": quantity
            }
        )

        # If product already exists
        if not created:

            new_quantity = (
                cart_item.quantity + quantity
            )

            if new_quantity > product.stock:

                return Response(
                    {
                        "error": "Not enough stock"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            cart_item.quantity = new_quantity

            cart_item.save()

        serializer = CartSerializer(
            cart
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


# =========================
# CART ITEM UPDATE / DELETE
# =========================

@api_view(["PUT", "DELETE"])
def cart_item_detail(request, pk):

    # -------------------------
    # AUTHENTICATION
    # -------------------------

    if not request.user.is_authenticated:

        return Response(
            {
                "error": "Authentication required"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # -------------------------
    # FIND CART ITEM
    # -------------------------

    try:

        cart_item = CartItem.objects.get(
            pk=pk,
            cart__user=request.user
        )

    except CartItem.DoesNotExist:

        return Response(
            {
                "error": "Cart item not found"
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # -------------------------
    # UPDATE QUANTITY
    # -------------------------

    if request.method == "PUT":

        quantity = request.data.get(
            "quantity"
        )

        try:

            quantity = int(quantity)

        except (TypeError, ValueError):

            return Response(
                {
                    "error": "Quantity must be a number"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:

            return Response(
                {
                    "error": "Quantity must be at least 1"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check stock
        if quantity > cart_item.product.stock:

            return Response(
                {
                    "error": "Not enough stock"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item.quantity = quantity

        cart_item.save()

        serializer = CartSerializer(
            cart_item.cart
        )

        return Response(
            serializer.data
        )

    # -------------------------
    # DELETE CART ITEM
    # -------------------------

    if request.method == "DELETE":

        cart = cart_item.cart

        cart_item.delete()

        serializer = CartSerializer(
            cart
        )

        return Response(
            serializer.data
        )