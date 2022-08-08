from marshmallow import Schema, fields

# user登入
# Parameter (Schema)
class UserPostRequest(Schema):
    name = fields.Str(doc="name", required=True)
    gender = fields.Str(doc="gender", required=True)
    birth = fields.Str(doc="birth", required=True)
    note = fields.Str(doc="note")
    account = fields.Str(doc="account", required=True)
    password = fields.Str(doc="password", required=True)

class UserPatchRequest(Schema):
    name = fields.Str(doc="name")
    gender = fields.Str(doc="gender")
    birth = fields.Str(doc="birth")
    note = fields.Str(doc="note")
    account = fields.Str(doc="account")
    password = fields.Str(doc="password")


# Common
class UserCommonResponse(Schema):
    message = fields.Str(example="success")

# Response
# Get
class UserGetResponse(UserCommonResponse):
    data = fields.List(
        fields.Dict(), 
        example={
            "id": 1,
            "name": "name",
            "birth": "1970/01/01",
            "gender": "male",
            "note": ""
        }
    )
    datetime = fields.Str()

class LoginSchema(Schema):
    account = fields.Str(doc="account", required=True)
    password = fields.Str(doc="password", required=True)

# --------------------------
# 購物車
# Parameter (Schema)
class CartPostRequest(Schema):
    iname = fields.Str(doc="iname", required=True)
    iprice = fields.Int(doc="iprice", required=True)
    stock = fields.Int(doc="stock", required=True)

class CartPatchRequest(Schema):
    iname = fields.Str(doc="iname")
    iprice = fields.Int(doc="iprice", required=True)
    stock = fields.Int(doc="stock", required=True)


# Common
class CartCommonResponse(Schema):
    message = fields.Str(example="success")

# Response
# Get
class CartGetResponse(CartCommonResponse):
    data = fields.List(
        fields.Dict(), 
        example={
            "id": 1,
            'iname': 'iname',
            'iprice': 'iprice',
            'stock': 'stock'
        }
    )
    datetime = fields.Str()
