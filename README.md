# Store-Manager-Api-V2

[![Build Status](https://travis-ci.org/JoshuaKodhe/Store-Manager-Api-V2.svg?branch=ft-products-sales-161499526)](https://travis-ci.org/JoshuaKodhe/Store-Manager-Api-V2)
[![Coverage Status](https://coveralls.io/repos/github/JoshuaKodhe/Store-Manager-Api-V2/badge.svg?branch=ch-role-based-authentication-161932691)](https://coveralls.io/github/JoshuaKodhe/Store-Manager-Api-V2?branch=ch-role-based-authentication-161932691)
[![Maintainability](https://api.codeclimate.com/v1/badges/1244b02159ef166cb31d/maintainability)](https://codeclimate.com/github/JoshuaKodhe/Store-Manager-Api-V2/maintainability)
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/06667185f01946854464)

## Introduction

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.

### Features

1. Admin can add a product.
2. Admin/store attendant can get all products
3. Admin/store attendant can get a specific product
4. Store attendant can add a sale order
5. Admin can get all sale records

### Prerequisites

[virtualenv](https://realpython.com/python-virtual-environments-a-primer/#using-virtual-environments)
[Git](https://git-scm.com/)

### Installing

### Change into the directory you'd prefer the project to live

```
$ cd <name of a certain folder on your local>
```

### Clone the project and change into the directory

```
$ git clone [Store-Manager-Api](https://github.com/JoshuaKodhe/Store-Manager-API/tree/ch-deploy-to-heroku-161363243)
```

```
$ cd Store-Manager-Api
```

### Create and activate virtual Environment

```
$ python3 -m venv env

```

```
$ source env/bin/activate
```

### Install project dependencies in your environment

```
$ pip install -r requirements.txt
```

### Export environment variables

```
export FLASK_APP="run.py"
export APP_SETTINGS="development"
export SECRET_KEY=<your secret key>

```

### Run the application

```
$ python run.py
```

### API-Endpoints

`Prefix - /api/v2`

| Endpoint                  | Functionality                 |
| ------------------------- | ----------------------------- |
| GET /products             | Fetch all products            |
| GET /products/<productId> | Fetch a single product record |
| GET /sales                | /questions                    | Fetch all sale records |
| GET /sales/<saleId>       | Fetch a single sale record    |
| POST /products            | Create a product              |
| POST /sales               | Create a sale order           |
| POST /auth/register       | Create a user                 |
| POST /auth/login          | Login a user                  |
