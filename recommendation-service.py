import pymongo
import certifi
import json
from multiprocessing.pool import ThreadPool

# 몽고디비 불러오기
client = pymongo.MongoClient("mongodb+srv://kk1109kk1109:sYFQfX5J28YD71Ls@cluster0.5pusjkc.mongodb.net/", tlsCAFile=certifi.where())
db = client["Cluster0"]

# 기준 설정
bud=30000000 # korean won
store_size = 30 # korean pyeong
# will be replaced by the actual input of client
plan_price = {"에스프레소머신":[15,40], "그라인더": [0, 10], "온수기": [0, 5], "제빙기":[10,15], "냉장고":[5,15], "블렌더":[3, 10]}
# espresso machine - min 15%, max 40% of of budget | grinder - min 0%, max 10% of budget ... 
plan_weight = {"에스프레소머신":[10,40], "그라인더": [10, 21], "온수기": [10, 15], "제빙기":[18,50], "냉장고":[30,50], "블렌더":[30, 40]}
# exact proportions need to be updated 
# espresso machine - min 15%, max 40% of of store size | grinder - min 0%, max 10% of store size ... 


# 무게 가져오는 함수들
def get_weights(items):
# 여러개
    weight_list = []
    for doc in items:
        description = doc["optDescription"].split(": ",maxsplit=1)
        description = description[1].split("\n",maxsplit=1)
        # size_list = description[0].split(" x ")
        # size_list = [eval(i) for i in size_list]
        # print("size_list", size_list)

        description = description[1].split(": ",maxsplit=1)
        description = description[1].split("\n",maxsplit=1)
        weight = int(description[0])
        # print("weight", weight)

        weight_list.append([doc["name"],weight])
    return weight_list

def get_weight(item):
# 한개
    description = item["optDescription"].split(": ",maxsplit=1)
    description = description[1].split("\n",maxsplit=1)
    description = description[1].split(": ",maxsplit=1)
    description = description[1].split("\n",maxsplit=1)
    weight = int(description[0])
    # print("weight", weight)
    return weight
    


# 에스프레소 머신
# 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
espresso_max = db.item.find({
    "option": "에스프레소 머신", 
    "price": {"$lte":bud*plan_price["에스프레소머신"][1]/100}
}).sort("price", pymongo.DESCENDING).limit(10)

for doc in espresso_max:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 60):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
espresso_min = db.item.find({"category": "에스프레소머신", 
    "price": {"$gte":bud*plan_price["에스프레소머신"][0]/100}, 
    "weight": {"$gte":bud*plan_weight["에스프레소머신"][0]/100}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_min:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
espresso_median = db.item.find(
    {"category": "에스프레소머신", 
    "price": {"$gte":(bud*plan_price["에스프레소머신"][1]/100 + bud*plan_price["에스프레소머신"][0]/100)/2}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_median:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")



# 그라인더
# 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
espresso_max = db.item.find({
    "option": "그라인더", 
    "price": {"$lte":bud*plan_price["그라인더"][1]/100}
}).sort("price", pymongo.DESCENDING).limit(10)

for doc in espresso_max:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 60):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
espresso_min = db.item.find({"category": "그라인더", 
    "price": {"$gte":bud*plan_price["그라인더"][0]/100}, 
    "weight": {"$gte":bud*plan_weight["그라인더"][0]/100}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_min:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
espresso_median = db.item.find(
    {"category": "그라인더", 
    "price": {"$gte":(bud*plan_price["그라인더"][1]/100 + bud*plan_price["그라인더"][0]/100)/2}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_median:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")




# 온수기
# 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
espresso_max = db.item.find({
    "option": "온수기", 
    "price": {"$lte":bud*plan_price["온수기"][1]/100}
}).sort("price", pymongo.DESCENDING).limit(10)

for doc in espresso_max:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 60):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
espresso_min = db.item.find({"category": "온수기", 
    "price": {"$gte":bud*plan_price["온수기"][0]/100}, 
    "weight": {"$gte":bud*plan_weight["온수기"][0]/100}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_min:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
espresso_median = db.item.find(
    {"category": "온수기", 
    "price": {"$gte":(bud*plan_price["온수기"][1]/100 + bud*plan_price["온수기"][0]/100)/2}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_median:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")



# 제빙기
# 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
espresso_max = db.item.find({
    "option": "제빙기", 
    "price": {"$lte":bud*plan_price["제빙기"][1]/100}
}).sort("price", pymongo.DESCENDING).limit(10)

for doc in espresso_max:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 60):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
espresso_min = db.item.find({"category": "제빙기", 
    "price": {"$gte":bud*plan_price["제빙기"][0]/100}, 
    "weight": {"$gte":bud*plan_weight["제빙기"][0]/100}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_min:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
espresso_median = db.item.find(
    {"category": "제빙기", 
    "price": {"$gte":(bud*plan_price["제빙기"][1]/100 + bud*plan_price["제빙기"][0]/100)/2}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_median:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")



# 냉장고
# 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
espresso_max = db.item.find({
    "option": "냉장고", 
    "price": {"$lte":bud*plan_price["냉장고"][1]/100}
}).sort("price", pymongo.DESCENDING).limit(10)

for doc in espresso_max:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 60):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
espresso_min = db.item.find({"category": "냉장고", 
    "price": {"$gte":bud*plan_price["냉장고"][0]/100}, 
    "weight": {"$gte":bud*plan_weight["냉장고"][0]/100}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_min:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
espresso_median = db.item.find(
    {"category": "냉장고", 
    "price": {"$gte":(bud*plan_price["냉장고"][1]/100 + bud*plan_price["냉장고"][0]/100)/2}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_median:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")




# 블렌더
# 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
espresso_max = db.item.find({
    "option": "블렌더", 
    "price": {"$lte":bud*plan_price["블렌더"][1]/100}
}).sort("price", pymongo.DESCENDING).limit(10)

for doc in espresso_max:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 60):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
espresso_min = db.item.find({"category": "블렌더", 
    "price": {"$gte":bud*plan_price["블렌더"][0]/100}, 
    "weight": {"$gte":bud*plan_weight["블렌더"][0]/100}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_min:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")

# 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
espresso_median = db.item.find(
    {"category": "블렌더", 
    "price": {"$gte":(bud*plan_price["블렌더"][1]/100 + bud*plan_price["블렌더"][0]/100)/2}}
).sort("price", pymongo.ASCENDING).limit(10)

for doc in espresso_median:
    weight = get_weight(doc)
    if (weight >= 30 and weight<= 50):
        print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")