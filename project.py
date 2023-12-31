import pymongo
import certifi

"""
효율적으로 바꾸기
1. As a general rule, databases are slower than files.
==> 몽고디비에서 데이터 베이스 처음에 읽어오고  csv 로 저장해서 앞으로의 코딩에서 그 파일 하나만 쓰기 ???

2.  try to sort on _id as well or hint the _id index to be used
do the task in smaller batches fetching x first Ids and moving them to a another process to continue with the next batch
(아직 이해 완벽히 안됨)
https://www.mongodb.com/community/forums/t/how-to-speed-up-find-projection-id-true-on-a-large-collection/124514

3. To load the data efficiently, you would need to split the file and process them in parallel.
There are two options of parallelism. You can use multi-threading or multi-processing.
You might be using sequential processing or multi-threading and hence the delay. 
Since the processing is done in single core by spawning multiple threads.
But in reality you need multi-processing, that utilizes all of the 16 cores in your server.
in python you have separate commands for doing something multi-threading vs multi-processing
https://www.mongodb.com/community/forums/t/what-is-the-fastest-and-most-accurate-way-to-import-data/123986
"""

client = pymongo.MongoClient("mongodb+srv://kk1109kk1109:sYFQfX5J28YD71Ls@cluster0.5pusjkc.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client["Cluster0"]

bud=30000000 # korean won
store_size = 30 # korean pyeong
# will be replaced by the actual input of client

plan_price = {"에스프레소머신":[15,40], "그라인더": [0, 10], "온수기": [0, 5], "제빙기":[10,15], "냉장고":[5,15], "블렌더":[3, 10]}
# espresso machine - min 15%, max 40% of of budget | grinder - min 0%, max 10% of budget ... 

plan_weight = {"에스프레소머신":[10,40], "그라인더": [10, 21], "온수기": [10, 15], "제빙기":[18,50], "냉장고":[30,50], "블렌더":[30, 40]}
# exact proportions need to be updated 
# espresso machine - min 15%, max 40% of of store size | grinder - min 0%, max 10% of store size ... 



# espresso machine recommendation
espresso_max = db.item.find({"category": "에스프레소머신", 
    "price": {"$lte":bud*plan_price["에스프레소머신"][1]/100}, 
    "weight": {"$lte":bud*plan_weight["에스프레소머신"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)

for doc in espresso_max:
    print("espresso_max", doc["name"], doc["price"])

espresso_min = db.item.find({"category": "에스프레소머신", 
    "price": {"$gte":bud*plan_price["에스프레소머신"][0]/100}, 
    "weight": {"$gte":bud*plan_weight["에스프레소머신"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in espresso_min:
    print("espresso_min", doc["name"], doc["price"])

espresso_median = db.item.find({"category": "에스프레소머신", 
    "price": {"$gte":(bud*plan_price["에스프레소머신"][1]/100 + bud*plan_price["에스프레소머신"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in espresso_median:
    print("espresso_median", doc["name"], doc["price"], doc["weight"])




# grinder recommendation
grinder_max = db.item.find({"category": "그라인더", 
    "price": {"$lte":bud*plan_price["그라인더"][1]/100},
    "weight": {"$lte":bud*plan_weight["그라인더"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)

for doc in grinder_max:
    print("grinder_max", doc["name"], doc["price"])

grinder_min = db.item.find({"category": "그라인더", 
    "price": {"$gte":bud*plan_price["그라인더"][0]/100},
    "weight": {"$gte":bud*plan_weight["그라인더"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in grinder_min:
    print("grinder_min", doc["name"], doc["price"])

grinder_median = db.item.find({"category": "그라인더", 
    "price": {"$gte":(bud*plan_price["그라인더"][1]/100 + bud*plan_price["그라인더"][0]/100)/2},
    "weight": {"$gte":(bud*plan_weight["그라인더"][1]/100 + bud*plan_weight["그라인더"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in grinder_median:
    print("grinder_median", doc["name"], doc["price"], doc["weight"])



# boiler recommendation
boiler_max = db.item.find({"category": "온수기", 
    "price": {"$lte":bud*plan_price["온수기"][1]/100},
    "weight": {"$lte":bud*plan_weight["온수기"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)

for doc in boiler_max:
    print("boiler_max", doc["name"], doc["price"])

boiler_min = db.item.find({"category": "온수기", 
    "price": {"$gte":bud*plan_price["온수기"][0]/100},
    "weight": {"$gte":bud*plan_weight["온수기"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in boiler_min:
    print("boiler_min", doc["name"], doc["price"])

boiler_median = db.item.find({"category": "온수기", 
    "price": {"$gte":(bud*plan_price["온수기"][1]/100 + bud*plan_price["온수기"][0]/100)/2},
    "weight": {"$gte":(bud*plan_weight["온수기"][1]/100 + bud*plan_weight["온수기"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in boiler_median:
    print("boiler_median", doc["name"], doc["price"], doc["weight"])



# ice maker recommendation
ice_max = db.item.find({"category": "제빙기", 
    "price": {"$lte":bud*plan_price["제빙기"][1]/100},
    "weight": {"$lte":bud*plan_weight["제빙기"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)

for doc in ice_max:
    print("ice_max", doc["name"], doc["price"])

ice_min = db.item.find({"category": "제빙기", 
    "price": {"$gte":bud*plan_price["제빙기"][0]/100},
    "weight": {"$gte":bud*plan_weight["제빙기"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in ice_min:
    print("ice_min", doc["name"], doc["price"])

ice_median = db.item.find({"category": "제빙기", 
    "price": {"$gte":(bud*plan_price["제빙기"][1]/100 + bud*plan_price["제빙기"][0]/100)/2},
    "weight": {"$gte":(bud*plan_weight["제빙기"][0]/100 + bud*plan_weight["제빙기"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in ice_median:
    print("ice_median", doc["name"], doc["price"], doc["weight"])


# refrigerator recommendation
fridge_max = db.item.find({"category": "냉장고", 
    "price": {"$lte":bud*plan_price["냉장고"][1]/100},
    "weight": {"$lte":bud*plan_weight["냉장고"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)

for doc in fridge_max:
    print("fridge_max", doc["name"], doc["price"], doc["weight"])

fridge_min = db.item.find({"category": "냉장고", 
    "price": {"$gte":bud*plan_price["냉장고"][0]/100},
    "weight": {"$gte":bud*plan_weight["냉장고"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in fridge_min:
    print("fridge_min", doc["name"], doc["price"])

fridge_median = db.item.find({"category": "냉장고", 
"price": {"$gte":(bud*plan_price["냉장고"][1]/100 + bud*plan_price["냉장고"][0]/100)/2},
"weight": {"$gte":(bud*plan_weight["냉장고"][1]/100 + bud*plan_weight["냉장고"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in fridge_median:
    print("fridge_median", doc["name"], doc["price"], doc["weight"])



# blender recommendation
blender_max = db.item.find({"category": "블렌더", 
    "price": {"$lte":bud*plan_price["블렌더"][1]/100},
    "weight": {"$lte":bud*plan_weight["블렌더"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)

for doc in blender_max:
    print("blender_max", doc["name"], doc["price"])

blender_min = db.item.find({"category": "블렌더", 
    "price": {"$gte":bud*plan_price["블렌더"][0]/100},
    "weight": {"$gte":bud*plan_weight["블렌더"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in blender_min:
    print("blender_min", doc["name"], doc["price"])

blender_median = db.item.find({"category": "블렌더", 
"price": {"$gte":(bud*plan_price["블렌더"][1]/100 + bud*plan_price["블렌더"][0]/100)/2},
"weight": {"$gte":(bud*plan_weight["블렌더"][1]/100 + bud*plan_weight["블렌더"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)

for doc in blender_median:
    print("blender_median", doc["name"], doc["price"], doc["weight"])