from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


# =========================
# PRODUCT SERIALIZER
# =========================

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


# =========================
# REGISTER SERIALIZER
# =========================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user


# =========================
# CART ITEM SERIALIZER
# =========================

class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem

        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
        ]


# =========================
# CART SERIALIZER
# =========================

class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Cart

        fields = [
            "id",
            "user",
            "items",
            "created_at",
        ]

        read_only_fields = [
            "user",
            "created_at",
        ]


# =========================
# ORDER ITEM SERIALIZER
# =========================

class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price",
        ]


# =========================
# ORDER SERIALIZER
# =========================

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "user",
            "items",
            "total_amount",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "user",
            "items",
            "total_amount",
            "status",
            "created_at",
        ]
