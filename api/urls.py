from django.urls import path

from .views import hello, products, product_detail


urlpatterns = [
    path("hello/", hello, name="hello"),

    path("products/", products, name="products"),
    path(
        "products/<int:pk>/",
        product_detail,
        name="product-detail"
    ),
]