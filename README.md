# E-Commerce API

A backend E-Commerce API built using **Django** and **Django REST Framework**. The project provides secure JWT authentication, product management, shopping cart functionality, and checkout/order processing through RESTful APIs.

The API includes authentication and authorization, product CRUD operations, cart management, stock validation, order creation, and checkout processing. All APIs were tested using **Postman**.

---

## 🚀 Features

* User registration
* JWT-based authentication
* Secure login and protected API endpoints
* Product creation
* Product listing
* Product details
* Product update
* Product deletion
* Shopping cart management
* Add products to cart
* Update cart item quantity
* Remove products from cart
* Stock validation
* Checkout processing
* Order creation
* Order item creation
* Automatic stock reduction after checkout
* Automatic cart clearing after successful checkout
* Request validation
* Error handling
* Database transactions
* RESTful API architecture
* Postman API testing

---

## 🛠️ Tech Stack

### Backend

* Python
* Django
* Django REST Framework

### Authentication

* JSON Web Token (JWT)
* `djangorestframework-simplejwt`

### Database

* SQLite
* Django ORM

### API Testing

* Postman

### Development Tools

* VS Code
* Git
* GitHub
* Python Virtual Environment

---

## 📁 Project Structure

```text
ecommerce_api/
│
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── venv/
│
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔐 Authentication

The project uses **JWT authentication** to protect APIs that require a logged-in user.

The authentication flow is:

```text
User Registration
       ↓
User Login
       ↓
JWT Access Token
       ↓
Send Token with Protected API Request
       ↓
API verifies Token
       ↓
Access Granted
```

Protected APIs require the JWT access token in the request header:

```text
Authorization: Bearer <access_token>
```

---

## 🔗 API Endpoints

Base URL:

```text
http://127.0.0.1:8000/api/
```

### Hello

```text
GET /api/hello/
```

Returns a simple message to verify that the API is working.

Example response:

```json
{
    "message": "E-Commerce API is working!"
}
```

---

### User Registration

```text
POST /api/auth/register/
```

Example request:

```json
{
    "username": "john",
    "email": "john@example.com",
    "password": "password123"
}
```

Example response:

```json
{
    "message": "User registered successfully",
    "username": "john",
    "email": "john@example.com"
}
```

---

## 🔑 JWT Login

```text
POST /api/auth/login/
```

Login using username and password.

Example request:

```json
{
    "username": "john",
    "password": "password123"
}
```

The API returns an access token.

Example:

```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

The access token is then used to access protected endpoints.

---

# 📦 Product APIs

## Get All Products

```text
GET /api/products/
```

Returns all available products.

Example response:

```json
[
    {
        "id": 1,
        "name": "Samsung Galaxy",
        "description": "Android smartphone",
        "price": "50000.00",
        "stock": 10,
        "created_at": "2026-08-25T06:00:08.265441Z"
    }
]
```

---

## Create Product

```text
POST /api/products/
```

🔒 Authentication required.

Example request:

```json
{
    "name": "Samsung Galaxy",
    "description": "Android smartphone",
    "price": "50000.00",
    "stock": 10
}
```

---

## Get Product Details

```text
GET /api/products/<id>/
```

Example:

```text
GET /api/products/1/
```

---

## Update Product

```text
PUT /api/products/<id>/
```

🔒 Authentication required.

Example:

```text
PUT /api/products/1/
```

Request body:

```json
{
    "name": "Samsung Galaxy S25",
    "description": "Updated Android smartphone",
    "price": "55000.00",
    "stock": 15
}
```

---

## Delete Product

```text
DELETE /api/products/<id>/
```

🔒 Authentication required.

Example:

```text
DELETE /api/products/1/
```

---

# 🛒 Shopping Cart

Each authenticated user has their own shopping cart.

## Get Cart

```text
GET /api/cart/
```

🔒 Authentication required.

Example response:

```json
{
    "id": 1,
    "user": 1,
    "items": [
        {
            "id": 1,
            "product": 2,
            "product_name": "Samsung Galaxy",
            "product_price": "50000.00",
            "quantity": 2
        }
    ],
    "created_at": "2026-08-25T06:10:00Z"
}
```

---

## Add Product to Cart

```text
POST /api/cart/
```

🔒 Authentication required.

Example request:

```json
{
    "product": 2,
    "quantity": 2
}
```

The API validates:

* Product exists
* Quantity is valid
* Requested quantity does not exceed available stock
* Existing cart items are updated correctly

---

## Update Cart Item

```text
PUT /api/cart/items/<id>/
```

🔒 Authentication required.

Example request:

```json
{
    "quantity": 3
}
```

---

## Remove Cart Item

```text
DELETE /api/cart/items/<id>/
```

🔒 Authentication required.

---

# 🧾 Checkout

Checkout converts the user's cart into an order.

```text
POST /api/checkout/
```

🔒 Authentication required.

No request body is required.

The checkout process:

```text
Get User Cart
      ↓
Check Cart
      ↓
Check Product Stock
      ↓
Calculate Total Amount
      ↓
Create Order
      ↓
Create Order Items
      ↓
Reduce Product Stock
      ↓
Clear Cart
      ↓
Return Order
```

The checkout operation uses a **database transaction** so that related database changes are handled consistently.

Example successful response:

```json
{
    "message": "Checkout successful",
    "order": {
        "id": 1,
        "user": 1,
        "total_amount": "100000.00",
        "status": "CONFIRMED"
    }
}
```

---

# 🗄️ Database Models

The project uses Django ORM for database operations.

Main models include:

### User

Django's built-in user model is used for authentication.

### Product

Stores product information.

```text
Product
├── id
├── name
├── description
├── price
├── stock
└── created_at
```

### Cart

Each user has one cart.

```text
Cart
├── id
├── user
└── created_at
```

### CartItem

Connects products with carts.

```text
CartItem
├── id
├── cart
├── product
└── quantity
```

### Order

Stores checkout information.

### OrderItem

Stores the products included in an order.

---

# 🔄 E-Commerce Workflow

The complete backend workflow is:

```text
Register
   ↓
Login
   ↓
Receive JWT Access Token
   ↓
View Products
   ↓
Add Product to Cart
   ↓
Update / Remove Cart Items
   ↓
Checkout
   ↓
Create Order
   ↓
Create Order Items
   ↓
Reduce Product Stock
   ↓
Clear Cart
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

Move into the project:

```bash
cd ecommerce_api
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
venv\Scripts\activate.bat
```

After activation, you should see:

```text
(venv)
```

in your terminal.

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Apply Migrations

```bash
python manage.py makemigrations
```

Then:

```bash
python manage.py migrate
```

---

## 6. Run Django Server

```bash
python manage.py runserver
```

The server will start at:

```text
http://127.0.0.1:8000/
```

---

# 🧪 Testing with Postman

The APIs were tested using **Postman**.

Recommended testing sequence:

```text
1. Register User
       ↓
2. Login
       ↓
3. Copy Access Token
       ↓
4. Get Products
       ↓
5. Create Product
       ↓
6. Add Product to Cart
       ↓
7. Get Cart
       ↓
8. Update Cart Item
       ↓
9. Remove Cart Item
       ↓
10. Checkout
       ↓
11. Verify Order
       ↓
12. Verify Product Stock
```

For protected APIs, use:

```text
Authorization
    ↓
Bearer Token
    ↓
<your_access_token>
```

---

# 🔒 Security

The project implements:

* JWT-based authentication
* Protected API endpoints
* Authentication checks
* Password hashing through Django authentication
* Request validation
* Permission checks
* User-specific shopping carts
* User-specific cart item access
* Database transactions during checkout

---

# 📊 Error Handling

The API handles common errors such as:

### Authentication required

```json
{
    "error": "Authentication required"
}
```

### Product not found

```json
{
    "error": "Product not found"
}
```

### Cart item not found

```json
{
    "error": "Cart item not found"
}
```

### Insufficient stock

```json
{
    "error": "Not enough stock"
}
```

### Empty cart

```json
{
    "error": "Cart is empty"
}
```

---

# 💡 Key Backend Concepts Demonstrated

This project demonstrates practical backend development concepts including:

* REST API development
* HTTP methods
* CRUD operations
* JWT authentication
* Authorization
* Django ORM
* Relational database modeling
* Foreign keys
* One-to-one relationships
* Many-to-one relationships
* Serialization
* Request validation
* Error handling
* Database transactions
* Inventory/stock management
* Cart management
* Order processing
* API testing with Postman

---

# 🎯 Project Objective

The objective of this project was to build a practical backend system that demonstrates how an E-Commerce application handles users, products, shopping carts, inventory, and checkout using RESTful APIs.

The project focuses on backend development, API design, authentication, database relationships, and business logic rather than frontend development.

---

# 🚀 Future Improvements

The project can be extended in the future with:

* PostgreSQL database
* Product search and filtering
* Product categories
* Product pagination
* User profile management
* Order history API
* Order cancellation
* Payment gateway integration
* Stripe integration
* Admin-specific permissions
* Docker deployment
* Cloud deployment
* Automated unit and API tests
* API documentation with Swagger/OpenAPI

---

# 👨‍💻 Author

**Hemanth Kumar Reddy**

B.Tech Information Technology Graduate

---

## 📌 Project Status

**Completed**

The current version implements the core E-Commerce backend workflow from:

```text
User Registration
        ↓
JWT Login
        ↓
Product Management
        ↓
Shopping Cart
        ↓
Checkout
        ↓
Order Creation
        ↓
Stock Management
```

This project was developed as a backend-focused application using **Django REST Framework**.
