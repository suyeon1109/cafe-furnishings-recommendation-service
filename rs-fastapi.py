from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Path
from pymongo import MongoClient
from pydantic import BaseModel
import pymongo
import certifi

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
# 몽고디비 불러오기
    app.mongodb_client = MongoClient("mongodb+srv://kk1109kk1109:sYFQfX5J28YD71Ls@cluster0.5pusjkc.mongodb.net/", tlsCAFile=certifi.where())
    app.database = app.mongodb_client["Cluster0"]

class Item(BaseModel):
    bud: int
    store_size: int
    user_id: str
    user_name: str

# 기준 설정
plan_price = {"에스프레소머신":[15,40], "그라인더": [0, 10], "온수기": [0, 5], "제빙기":[10,15], "냉장고":[5,15]} 
# , "블렌더":[3, 10]}
# espresso machine - min 15%, max 40% of of budget | grinder - min 0%, max 10% of budget ...

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
    

# 무게 가져오는 함수들
def get_weights(items):
# 여러개
    weight_list = []
    for doc in items:
        description = doc["optDescription"].split(": ",maxsplit=1)
        description = description[1].split("\n",maxsplit=1)
        description = description[1].split(": ",maxsplit=1)
        description = description[1].split("\n",maxsplit=1)
        weight = int(description[0])
        weight_list.append([doc["name"],weight])
    return weight_list

def get_weight(item):
# 한개
    description = item["optDescription"].split(": ",maxsplit=1)
    description = description[1].split("\n",maxsplit=1)
    description = description[1].split(": ",maxsplit=1)
    description = description[1].split("\n",maxsplit=1)
    weight = float(description[0])
    return weight

def weight_range(store_size):
    if store_size < 20:
        return weight_1020 
    if store_size < 30:
        return weight_2030 
    if store_size < 50:
        return weight_3050 
    if store_size < 100:
        return weight_50100 

@app.get(".answers/")
async def set_user(user_input:Item):
    data = user_input.dict()
    app.database.answers.insert_one(data)
    return {"message": "The data is stored successfully."}


@app.post("/recommend_grinders", response_model=List[str])
def recommend_grinders(item: Item):
    bud = item.bud
    store_size = item.store_size
    standard = weight_range(store_size)
    
    printed = 0
    recommendations = []

    # Find the most expensive grinders within budget and weight range
    grinder_max = app.database.item.find(
        {
            "option": "그라인더",
            "price": {"$lte": bud * plan_price["그라인더"][1] / 100}
        }
    ).sort("price", pymongo.DESCENDING).limit(10)

    for doc in grinder_max:
        weight = get_weight(doc)
        if (weight >= standard[0] and weight <= standard[1]):
            recommendations.append(f"{doc['name']}, {weight}kg, {doc['price']}원")
            printed += 1
        if printed == 2:
            break

    # Find the cheapest grinders within budget and weight range
    grinder_min = app.database.item.find(
        {
            "option": "그라인더",
            "price": {"$gte": bud * plan_price["그라인더"][0] / 100}
        }
    ).sort("price", pymongo.ASCENDING).limit(10)

    for doc in grinder_min:
        weight = get_weight(doc)
        if (weight >= standard[0] and weight <= standard[1]):
            recommendations.append(f"{doc['name']}, {weight}kg, {doc['price']}원")
            printed += 1
        if printed == 4:
            break

    # Find grinders with prices in between budget and weight range
    grinder_median = app.database.item.find(
        {
            "option": "그라인더",
            "price": {
                "$gte": (bud * plan_price["그라인더"][1] / 100 + bud * plan_price["그라인더"][0] / 100) / 2
            }
        }
    ).sort("price", pymongo.ASCENDING).limit(10)

    for doc in grinder_median:
        weight = get_weight(doc)
        if (weight >= standard[0] and weight <= standard[1]):
            recommendations.append(f"{doc['name']}, {weight}kg, {doc['price']}원")
            printed += 1
        if printed == 6:
            break

    # If there are no items within the specified weight range
    if printed == 0:
        grinder_left = app.database.item.find(
            {
                "option": "그라인더",
                "price": {"$lte": bud * plan_price["그라인더"][0] / 100}
            }
        ).sort("price", pymongo.ASCENDING).limit(10)

        grinder_right = app.database.item.find(
            {
                "option": "그라인더",
                "price": {"$gte": bud * plan_price["그라인더"][1] / 100}
            }
        ).sort("price", pymongo.DESCENDING).limit(10)

        for doc in grinder_left:
            weight = get_weight(doc)
            if (weight >= standard[0] and weight <= standard[1]):
                recommendations.append(f"{doc['name']}, {weight}kg, {doc['price']}원")
                printed += 1
            if printed == 2:
                break

        for doc in grinder_right:
            weight = get_weight(doc)
            if (weight >= standard[0] and weight <= standard[1]):
                recommendations.append(f"{doc['name']}, {weight}kg, {doc['price']}원")
                printed += 1
            if printed == 4:
                break

    return recommendations