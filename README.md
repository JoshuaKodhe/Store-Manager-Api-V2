# Store-Manager-Api-V2


## Introduction

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.

### Features

1. Admin can add a product.
2. Admin/store attendant can get all products
3. Admin/store attendant can get a specific product
4. Store attendant can add a sale order
5. Admin can get all sale records


### API-Endpoints
``` Prefix - /api/v2```
 Endpoint | Functionality
 --- | ---
GET /products | Fetch all products
GET /products/<productId> | Fetch a single product record
GET /sales| /questions | Fetch all sale records
GET /sales/<saleId> | Fetch a single sale record
POST /products | Create a product
POST /sales | Create a sale order
POST /auth/register| Create a user
POST /auth/login | Login a user
