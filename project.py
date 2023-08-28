import pymongo
import certifi


'''
<집기 카테고리>
- 에스프레소머신
- 그라인더
- 온수기
- 제빙기
- 냉장고
- 블렌더

<가격 분배>
에스프레소머신
- 최소: 15%
- 최대: 40%

그라인더
- 최대: 10%

온수기
- 최대: 5%

제빙기
- 최소: 10%
- 최대: 15%

냉장고
- 최소: 5%
- 최대: 15%

블렌더
- 최소: 3%
- 최대: 10%


<I/O>
Input
- 총 예산

Output
- 각 집기 카테고리 별 제품 3개씩 추천
- 조합 최소 비용
- 조합 최대 비용
'''


client = pymongo.MongoClient("mongodb+srv://kk1109kk1109:sYFQfX5J28YD71Ls@cluster0.5pusjkc.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client["Cluster0"]

bud=30000000

plan = {"에스프레소머신":[15,40], "그라인더": [0, 10], "온수기": [0, 5], "제빙기":[10,15], "냉장고":[5,15], "블렌더":[3, 10]}

espresso_max = db.item.find({"category": "에스프레소머신", "price": {"$lte":bud*plan["에스프레소머신"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)
for doc in espresso_max:
    print("espresso_max", doc["name"], doc["price"])
espresso_min = db.item.find({"category": "에스프레소머신", "price": {"$gte":bud*plan["에스프레소머신"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in espresso_min:
    print("espresso_min", doc["name"], doc["price"])
espresso_median = db.item.find({"category": "에스프레소머신", "price": {"$gte":(bud*plan["에스프레소머신"][1]/100 + bud*plan["에스프레소머신"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in espresso_median:
    print("espresso_median", doc["name"], doc["price"])


grinder_max = db.item.find({"category": "그라인더", "price": {"$lte":bud*plan["그라인더"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)
for doc in grinder_max:
    print("grinder_max", doc["name"], doc["price"])
grinder_min = db.item.find({"category": "그라인더", "price": {"$gte":bud*plan["그라인더"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in grinder_min:
    print("grinder_min", doc["name"], doc["price"])
grinder_median = db.item.find({"category": "그라인더", "price": {"$gte":(bud*plan["그라인더"][1]/100 + bud*plan["그라인더"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in grinder_median:
    print("grinder_median", doc["name"], doc["price"])


boiler_max = db.item.find({"category": "온수기", "price": {"$lte":bud*plan["온수기"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)
for doc in boiler_max:
    print("boiler_max", doc["name"], doc["price"])
boiler_min = db.item.find({"category": "온수기", "price": {"$gte":bud*plan["온수기"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in boiler_min:
    print("boiler_min", doc["name"], doc["price"])
boiler_median = db.item.find({"category": "온수기", "price": {"$gte":(bud*plan["온수기"][1]/100 + bud*plan["온수기"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in boiler_median:
    print("boiler_median", doc["name"], doc["price"])


ice_max = db.item.find({"category": "제빙기", "price": {"$lte":bud*plan["제빙기"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)
for doc in ice_max:
    print("ice_max", doc["name"], doc["price"])
ice_min = db.item.find({"category": "제빙기", "price": {"$gte":bud*plan["제빙기"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in ice_min:
    print("ice_min", doc["name"], doc["price"])
ice_median = db.item.find({"category": "제빙기", "price": {"$gte":(bud*plan["제빙기"][1]/100 + bud*plan["제빙기"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in ice_median:
    print("ice_median", doc["name"], doc["price"])


fridge_max = db.item.find({"category": "냉장고", "price": {"$lte":bud*plan["냉장고"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)
for doc in fridge_max:
    print("fridge_max", doc["name"], doc["price"])
fridge_min = db.item.find({"category": "냉장고", "price": {"$gte":bud*plan["냉장고"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in fridge_min:
    print("fridge_min", doc["name"], doc["price"])
fridge_median = db.item.find({"category": "냉장고", "price": {"$gte":(bud*plan["냉장고"][1]/100 + bud*plan["냉장고"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in fridge_median:
    print("fridge_median", doc["name"], doc["price"])


blender_max = db.item.find({"category": "블렌더", "price": {"$lte":bud*plan["블렌더"][1]/100}}).sort("price", pymongo.DESCENDING).limit(1)
for doc in blender_max:
    print("blender_max", doc["name"], doc["price"])
blender_min = db.item.find({"category": "블렌더", "price": {"$gte":bud*plan["블렌더"][0]/100}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in blender_min:
    print("blender_min", doc["name"], doc["price"])
blender_median = db.item.find({"category": "블렌더", "price": {"$gte":(bud*plan["블렌더"][1]/100 + bud*plan["블렌더"][0]/100)/2}}).sort("price", pymongo.ASCENDING).limit(1)
for doc in blender_median:
    print("blender_median", doc["name"], doc["price"])

