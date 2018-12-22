register_schema = {
    "type": "object",
    "properties": {
        "email": {type: "string"},
        "username": {type: "string"},
        "password": {type: "string"},
        "role": {type: "string"}
    },
    "required": ["email", "password", "role"]
}

login_schema = {
    "type": "object",
    "properties": {
        "email": {type: "string"},
        "password": {type: "string"},
    },
    "required": ["email", "password"]
}

product_schema = {
    "type": "object",
    "properties": {
        "name": {type: "string"},
        "description": {type: "string"},
        "category": {type: "string"},
        "quantity": {type: "integer"},
        "price": {type: "integer"},
        "image_url": {type: "string"}

    },
    "required": ["name", "description", "category", "quantity", "price", "image_url"]
}

sale_schema = {
    "type": "object",
    "properties": {
        "name": {type: "string"},
        "quantity": {type: "integer"},
    },
    "required": ["name", "quantity"]
}
