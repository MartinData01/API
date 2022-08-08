import pymysql
from flask import jsonify
import util
from flask_apispec import doc,use_kwargs,MethodResource,marshal_with
from shop_route_model import *
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta

# 資料庫
def db_init():
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        port=3306,
        db='api_class'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

# 登入token
def get_access_token(account):
    token = create_access_token(
        identity={"account": account},
        expires_delta=timedelta(days=20)
    )
    return token

# Get Post
class Users(MethodResource):
    @doc(description="Get users info",tags=["User"])
    @marshal_with(UserGetResponse,code=200)
    @jwt_required()
    def get(self):
        db, cursor = db_init()

        sql = "SELECT * FROM api_class.member;"
        cursor.execute(sql)

        users = cursor.fetchall()
        db.close()
        return util.success(users)

    @doc(description="Add user",tags=["User"])
    @use_kwargs(UserPostRequest,location="json")
    @marshal_with(UserCommonResponse,code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        

        user = {
            'name': kwargs['name'],
            'gender': kwargs['gender'],
            'birth': kwargs.get('birth') or '1900-01-01',
            'note': kwargs.get('note'),
            'account': kwargs.get('account'),
            'password': kwargs.get('password')
        }
        sql = """

        INSERT INTO `api_class`.`member` (`name`,`gender`,`account`,`password`,`birth`,`note`)
        VALUES ('{}','{}','{}','{}','{}','{}');

        """.format(
            user['name'], user['gender'], user['account'], user['password'], user['birth'], user['note'])
        
        result = cursor.execute(sql)

        db.commit()
        db.close()
        
        
        if result == 1:
            return util.success()
        else:
            return util.failure()
        
        
        
        
# patch delete
class User(MethodResource):
    @doc(description="Update users info",tags=["User"])
    @use_kwargs(UserPatchRequest,location="json")
    @marshal_with(UserCommonResponse,code=200)
    def patch(self, id, **kwargs):
        db,cursor = db_init()
        user = {
            'name': kwargs.get('name'),
            'gender': kwargs.get('gender'),
            'birth': kwargs.get('birth'),
            'note': kwargs.get('note'),
            'account': kwargs.get('account'),
            'password': kwargs.get('password')
        }

        query = []
        print(user)
        '''{'name': None, 'gender': 'Double', 'birth': None, 'note': None}'''
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE id=1;

        '''
        sql = """
            UPDATE api_class.member
            SET {}
            WHERE id = {};
        """.format(query, id)

        result = cursor.execute(sql)
        
        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
        else:
            return util.failure()

        

    @doc(description="Delete users info",tags=["User"])
    @marshal_with(UserCommonResponse,code=200)
    def delete(self, id):
        db, cursor = db_init()
        sql = f'DELETE FROM `api_class`.`member` WHERE id = {id};'
        result = cursor.execute(sql)
        
        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
        else:
            return util.failure()

# 登入訊息
class Login(MethodResource):
    @doc(description='User Login', tags=['Login'])
    @use_kwargs(LoginSchema, location="json")
    # @marshal_with(user_router_model.UserGetResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM api_class.member WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall() #空值會回傳()
        db.close()

        if user != ():
            token = get_access_token(account)
            data = {
                "message": f"Welcome back {user[0]['name']}",
                "token": token}
            return util.success(data)
        
        return util.failure({"message":"Account or password is wrong"})

# 改成購物車 查看 新增
class Cart(MethodResource):
    @doc(description="Shopping Cart",tags=["Cart"])
    @marshal_with(UserGetResponse,code=200)
    @jwt_required()
    def get(self):
        db, cursor = db_init()

        sql = "SELECT * FROM api_class.shop;"
        cursor.execute(sql)

        users = cursor.fetchall()
        db.close()
        return util.success(users)

    @doc(description="Add item",tags=["Cart"])
    @use_kwargs(CartPostRequest,location="json")
    @marshal_with(CartCommonResponse,code=201) ##重點
    @jwt_required()
    def post(self, **kwargs):
        db, cursor = db_init()

        user = {
            'iname': kwargs['iname'],
            'iprice': kwargs['iprice'],
            'stock': kwargs['stock']
        }
        sql = """

        INSERT INTO `api_class`.`shop` (`iname`,`iprice`,`stock`)
        VALUES ('{}','{}','{}');

        """.format(
            user['iname'], user['iprice'],user['stock'])
        
        result = cursor.execute(sql)

        db.commit()
        db.close()
        
        
        if result == 1:
            return util.success()
        else:
            return util.failure()

# 改成購物車 修改 刪除
class Cart2(MethodResource):
    @doc(description="Update cart item",tags=["Cart"])
    @use_kwargs(CartPatchRequest,location="json")
    @marshal_with(CartCommonResponse,code=201)
    @jwt_required()
    def patch(self, id, **kwargs):
        db,cursor = db_init()
        user = {
            'iname': kwargs.get('iname'),
            'iprice': kwargs.get('iprice'),
            'stock': kwargs.get('stock')
        }

        query = []
        print(user)
        '''{'iname': None, 'iprice': 'Double'}'''
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE id=1;

        '''
        sql = """
            UPDATE api_class.shop
            SET {}
            WHERE id = {};
        """.format(query, id)

        result = cursor.execute(sql)
        
        db.commit()
        # 總價測試
        sql = "SELECT * FROM api_class.shop;"
        cursor.execute(sql)

        users = cursor.fetchall()
        count = 0
        for row in users:
            count += (row["iprice"] * row["stock"])

        db.close()
        return util.total(user,count)
        # if result == 1:
        #     return util.success()
        # else:
        #     return util.failure()
    # 刪除購物車商品
    @doc(description="Delete cart item",tags=["Cart"])
    @marshal_with(CartCommonResponse,code=200)
    @jwt_required()
    def delete(self, id):
        db, cursor = db_init()
        sql = f'DELETE FROM `api_class`.`shop` WHERE id = {id};'
        result = cursor.execute(sql)
        
        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
        else:
            return util.failure()
# 搜尋
class search(MethodResource):
    @doc(description='Search cart info',tags=['Cart'])
    @marshal_with(CartGetResponse,code=201)
    @jwt_required()
    def get(self, iname):
        db, cursor = db_init()
        
        sql = f'select * FROM `api_class`.`shop` WHERE iname like "%{iname}%";'
        cursor.execute(sql)

        db.commit()

        users = cursor.fetchall()
        db.close()
        return util.success(users)