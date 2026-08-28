from django.urls import path

from .views import (
    hello,
    products,
    product_detail,
    register,
    cart,
)


urlpatterns = [
    path(
        "hello/",
        hello,
        name="hello"
    ),

    path(
        "auth/register/",
        register,
        name="register"
    ),

    path(
        "products/",
        products,
        name="products"
    ),

    path(
        "products/<int:pk>/",
        product_detail,
        name="product-detail"
    ),

    path(
        "cart/",
        cart,
        name="cart"
    ),
]