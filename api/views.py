from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.db import transaction

from .models import (
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)

from .serializers import (
    ProductSerializer,
    RegisterSerializer,
    CartSerializer,
    OrderSerializer,
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

    if request.method == "GET":

        products = Product.objects.all()

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

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

    if request.method == "GET":

        serializer = ProductSerializer(
            product
        )

        return Response(serializer.data)

    if not request.user.is_authenticated:

        return Response(
            {
                "error": "Authentication required"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

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

    if not request.user.is_authenticated:

        return Response(
            {
                "error": "Authentication required"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    if request.method == "GET":

        serializer = CartSerializer(
            cart
        )

        return Response(
            serializer.data
        )

    if request.method == "POST":

        product_id = request.data.get(
            "product"
        )

        quantity = request.data.get(
            "quantity",
            1
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

        if quantity > product.stock:

            return Response(
                {
                    "error": "Not enough stock"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "quantity": quantity
            }
        )

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

    if not request.user.is_authenticated:

        return Response(
            {
                "error": "Authentication required"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

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

    if request.method == "DELETE":

        cart = cart_item.cart

        cart_item.delete()

        serializer = CartSerializer(
            cart
        )

        return Response(
            serializer.data
        )


# =========================
# CHECKOUT
# =========================

@api_view(["POST"])
def checkout(request):

    if not request.user.is_authenticated:

        return Response(
            {
                "error": "Authentication required"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:

        cart = Cart.objects.get(
            user=request.user
        )

    except Cart.DoesNotExist:

        return Response(
            {
                "error": "Cart not found"
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    cart_items = cart.items.select_related(
        "product"
    )

    if not cart_items.exists():

        return Response(
            {
                "error": "Cart is empty"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # =========================
    # CHECKOUT TRANSACTION
    # =========================

    with transaction.atomic():

        total_amount = 0

        # -------------------------
        # CHECK STOCK
        # -------------------------

        for cart_item in cart_items:

            product = cart_item.product

            if cart_item.quantity > product.stock:

                return Response(
                    {
                        "error": (
                            f"Not enough stock for "
                            f"{product.name}"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            total_amount += (
                product.price * cart_item.quantity
            )

        # -------------------------
        # CREATE ORDER
        # -------------------------

        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            status="CONFIRMED",
        )

        # -------------------------
        # CREATE ORDER ITEMS
        # -------------------------

        for cart_item in cart_items:

            product = cart_item.product

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=product.price,
            )

            # -------------------------
            # REDUCE STOCK
            # -------------------------

            product.stock -= cart_item.quantity

            product.save()

        # -------------------------
        # CLEAR CART
        # -------------------------

        cart.items.all().delete()

    # -------------------------
    # RETURN ORDER
    # -------------------------

    serializer = OrderSerializer(
        order
    )

    return Response(
        {
            "message": "Checkout successful",
            "order": serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )