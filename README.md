Authentek
=========

Auth API

Examples:
---------


**Request Headers**

Content-Type:
application/json
```http
POST http://0.0.0.0:8888/v1/users/
{
    "email": "pogo@pogo.de",
    "password": "321321321",
    "username": "pogo"
}
```

```http
POST http://0.0.0.0:8888/v1/auth/login
{
    "password": "321321321",
    "email": "pogo@pogo.de"
}
```
**Request Headers**

Authorization:
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Mjc3MTc2MTUsImlhdCI6MTYyNTEyNTYxNSwic3ViIjozfQ.byPIvI7eg1lJ6l-z3vrhazEhIXRrt6-2yB2HNsYCTqo
```http
GET http://0.0.0.0:8888/v1/auth/info
```


**Request Headers**

Authorization:
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Mjc3MTc2MTUsImlhdCI6MTYyNTEyNTYxNSwic3ViIjozfQ.byPIvI7eg1lJ6l-z3vrhazEhIXRrt6-2yB2HNsYCTqo
```http
POST http://0.0.0.0:8888/v1/auth/logout
```