- Orders API
    This is an API for managing orders.

- Endpoints
    - orders/:
        - GET: Returns all orders if user is a superuser, else returns orders for authenticated user.
        - POST: Creates a new order for authenticated user.
    - orders/<int:pk>/:
        - GET: Returns an order with specified ID if user is a superuser or owner of the order.
        - PUT: Updates an order with specified ID if user is a superuser or owner of the order.
        - DELETE: Deletes an order with specified ID if user is a superuser or owner of the order.
    - users/:
        - GET: Returns a list of all users if user is a superuser.
        - POST: Creates a new user if user is a superuser.
    - users/<int:pk>/:
        - GET: Returns a user with specified ID if user is a superuser.
        - PUT: Updates a user with specified ID if user is a superuser.
        - DELETE: Deletes a user with specified ID if user is a superuser.
    - orders/by-email/:
        - GET: Returns orders owned by users with specified email addresses.
    - emails/:
        - GET: Returns a list of all email addresses of all users.

- Authentication
The API requires authentication to perform most actions. The orders/ endpoint requires authentication, while the users/ endpoint requires superuser status.

- Errors
    The API returns standard HTTP errors as well as custom error messages when applicable. The custom error messages are returned in the following format:

    - json-response
        {
        "error": "Error message."
        }


- Installation
To use this API, you must have Django and Django REST framework installed.

After installing Django and Django REST framework, you can run the server with the following command:

`python manage.py runserver`
The API will be available at http://localhost:8000/.