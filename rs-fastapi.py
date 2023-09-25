from fastapi import FastAPI, Path
from pymongo import MongoClient
from pydantic import BaseModel
import certifi

project = FastAPI()

@project.on_event("startup")
def startup_db_client():
    project.mongodb_client = MongoClient("mongodb+srv://kk1109kk1109:sYFQfX5J28YD71Ls@cluster0.5pusjkc.mongodb.net/", tlsCAFile=certifi.where())
    project.database = project.mongodb_client["Cluster0"]

inventory = {
    1: {
        "name": "Milk",
        "price": "3.99",
        "brand": "Regular"
    },
    2: {
        "name": "Sprite",
        "price": "1.99",
        "brand": "Regular"
    }
}

class Plan(BaseModel):
    bud: str
    store_size: str
   
@project.get("")
async def input_plans(plan: Plan):
    plan_price = {"에스프레소머신":[15,40], "그라인더": [0, 10], "온수기": [0, 5], "제빙기":[10,15], "냉장고":[5,15]} 

    em_range = [4,101]
    gr_range = [1,35]
    bo_range = [10,13]
    ice_range = [50,300]
    fr_range = [70,110]

    weight_1020 = {
        "에스프레소머신":[em_range[0],em_range[1]/4], 
        "그라인더": [gr_range[0],gr_range[1]/4], 
        "온수기": [bo_range[0],bo_range[1]/4], 
        "제빙기":[ice_range[0],ice_range[1]/4], 
        "냉장고":[fr_range[0],fr_range[1]/4]
        }
    weight_2030 = {
        "에스프레소머신":[em_range[1]/4,em_range[1]/2], 
        "그라인더": [gr_range[1]/4,gr_range[1]/2], 
        "온수기": [bo_range[1]/4,bo_range[1]/2], 
        "제빙기":[ice_range[1]/4,ice_range[1]/2], 
        "냉장고":[fr_range[1]/4,fr_range[1]/2]
        }
    weight_3050 = {
        "에스프레소머신":[em_range[1]/2,em_range[1]*3/4], 
        "그라인더": [gr_range[1]/2,gr_range[1]*3/4], 
        "온수기": [bo_range[1]/2,bo_range[1]*3/4], 
        "제빙기":[ice_range[1]/2,ice_range[1]*3/4], 
        "냉장고":[fr_range[1]/2,fr_range[1]*3/4]
        }
    weight_50100 = {
        "에스프레소머신":[em_range[1]*3/4,em_range[1]], 
        "그라인더": [gr_range[1]/2,gr_range[1]*3/4], 
        "온수기": [bo_range[1]/2,bo_range[1]*3/4], 
        "제빙기":[ice_range[1]/2,ice_range[1]*3/4], 
        "냉장고":[fr_range[1]/2,fr_range[1]*3/4]
        }

    if plan["store_size"] < 20:
        return weight_1020 
    if plan["store_size"] < 30:
        return weight_2030 
    if plan["store_size"] < 50:
        return weight_3050 
    if plan["store_size"] < 100:
        return weight_50100 

# @project.post(".list/")
# async def create_item(item: Item):
#     data=item.dict()
#     project.database.suyeon.insert_one(data)
#     return {"message": "The data is stored successfully."}
#     return item

# @project.get("/list/{item_name}")
# async def get_item(item_name: str):
#     data = project.database.students.find_one({"name": item_name})
#     data["_id"] = str(data["_id"])
#     return data