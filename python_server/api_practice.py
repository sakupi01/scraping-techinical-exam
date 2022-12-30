# APIのすべての機能を提供するPythonクラス
from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from typing import Union
from fastapi.params import Body

# 変数方宣言しなくても，戻り値の値がこれに従っていなければならないということを理解してくれる
# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# To declare request body, use Pydamic
# Union type gives option of the types. [str, None] means that you can take str or None or those combination
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

# Create a FastAPI instance == app
app = FastAPI()


# 直下の関数が下記のリクエストの処理を担当することをFastAPIに伝えます
# Pythonにおける@somethingシンタックスはデコレータと呼ばれます
# 「デコレータ」は直下の関数を受け取り、それを使って何かを行います。
# @app.post()
# @app.put()
# @app.delete()
# https://fastapi.tiangolo.com/ja/async/#in-a-hurry
# Path parameter/Path variableも設定できる
# Query: When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
@app.get("/items/{item_id}")
async def read_item(item_id: int, update: bool = False):
    item = {"item_id": item_id}
    if update != False:
        item.update({"id": item_id})
    else:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# not only send the data to postman, but also, we can extract the data.
@app.post("/create_post")
async def create_item():
    print(name)
    return {"newpost": f'This is {name["name"]}'}
    return {"message": 'success posting!'}

'''uvicorn main:appは以下を示します:
main: main.pyファイル (Python "module")。
app: main.py内部で作られるobject（app = FastAPI()のように記述される）。
--reload: コードの変更時にサーバーを再起動させる。開発用。'''
