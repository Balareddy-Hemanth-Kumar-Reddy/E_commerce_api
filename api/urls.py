from django.urls import path

from .views import hello, products, product_detail

from .views import hello, products, product_detail, register


urlpatterns = [
    path("hello/", hello, name="hello"),

    path("products/", products, name="products"),
    path(
        "products/<int:pk>/",
        product_detail,
        name="product-detail"
    ),

    path("auth/register/", register, name="register"),
    
]