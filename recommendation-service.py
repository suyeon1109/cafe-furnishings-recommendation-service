import pymongo
import certifi

# 몽고디비 불러오기
client = pymongo.MongoClient("mongodb+srv://kk1109kk1109:sYFQfX5J28YD71Ls@cluster0.5pusjkc.mongodb.net/", tlsCAFile=certifi.where())
db = client["Cluster0"]

# 답변 불러오기
bud = int(input("예산 (기준: 원): "))
store_size = int(input("카페 평수 (기준: 평): "))

# 기준 설정
# bud=30000000 # korean won
# store_size = 30 # korean pyeong
# will be replaced by the actual input of client
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



"""
mongodb .find() 함수 썼을때 나오는 리스트? 딕셔너리? 의 길이 구하는 법...!!!!!!!
"""

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
    weight = float(description[0])
    # print("weight", weight)
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

# # 프린트하는 함수
# def print_machines(machine_list, option, standard):
#     for doc in machine_list:
#         weight = get_weight(doc)
#         standard = weight_range(store_size)
#         if (weight >= standard[option][0] and weight<= standard[option][1]):
#             print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#             return True
#         else: 
#             return False




# set standard as a public value
standard = weight_range(store_size)

# 에스프레소 머신
printed = 0
# 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
espresso_max = db.item.find({
    "option": "에스프레소 머신", 
    "price": {"$lte":bud*plan_price["에스프레소머신"][1]/100}
}).sort("price", pymongo.DESCENDING).limit(10)

price=0

print("추천드리는 에스프레소 머신")
if len(espresso_max)!=0:
    price+=1
    for doc in espresso_max:
        weight = get_weight(doc)
        standard = weight_range(store_size)
        if (weight >= standard["에스프레소머신"][0] and weight<= standard["에스프레소머신"][1]):
            print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
            printed+=1
        if printed==2:
            break

# 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
espresso_min = db.item.find(
    {"option": "에스프레소머신", 
    "price": {"$gte":bud*plan_price["에스프레소머신"][0]/100}
}).sort("price", pymongo.ASCENDING).limit(10)

if len(espresso_min)!=0:
    price+=1
    for doc in espresso_min:
        weight = get_weight(doc)
        standard = weight_range(store_size)
        if (weight >= standard["에스프레소머신"][0] and weight<= standard["에스프레소머신"][1]):
            print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
            printed+=1
        if printed==4:
            break

# 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
espresso_median = db.item.find(
    {"option": "에스프레소머신", 
    "price": {"$gte":(bud*plan_price["에스프레소머신"][1]/100 + bud*plan_price["에스프레소머신"][0]/100)/2}}
).sort("price", pymongo.ASCENDING).limit(10)

if espresso_median!=0:
    price+=1
    for doc in espresso_median:
        weight = get_weight(doc)
        standard = weight_range(store_size)
        if (weight >= standard["에스프레소머신"][0] and weight<= standard["에스프레소머신"][1]):
            print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
            printed+=1
        if printed==6:
            break


# 기준에 맞는 제품이 하나도 없을 때 

if price==0:
    espresso_left = espresso_min = db.item.find(
        {"option": "에스프레소머신", 
        "price": {"$lte":bud*plan_price["에스프레소머신"][0]/100}
    }).sort("price", pymongo.ASCENDING).limit(10)
    espresso_right = db.item.find({
        "option": "에스프레소머신", 
        "price": {"$gte":bud*plan_price["에스프레소머신"][1]/100}
    }).sort("price", pymongo.DESCENDING).limit(10)

    for doc in espresso_left:
        if (weight >= standard["에스프레소머신"][0] and weight<= standard["에스프레소머신"][1]):
            print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
            printed+=1
        if printed==2:
            break
    
    for doc in espresso_right:
        if (weight >= standard["에스프레소머신"][0] and weight<= standard["에스프레소머신"][1]):
            print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
            printed+=1
        if printed==4:
            break
elif printed==0:
    machine_lists = [espresso_max,espresso_median, espresso_min]
    for list in machine_lists:
        for doc in list:
            weight = get_weight(doc)
            standard = weight_range(store_size)
            if (weight >= standard["에스프레소머신"][0]-10 and weight<= standard["에스프레소머신"][1]+10):
                print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
                printed+=1
            if printed==2:
                break
print()





# # 그라인더
# printed = 0
# # 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
# grinder_max = db.item.find({
#     "option": "그라인더", 
#     "price": {"$lte":bud*plan_price["그라인더"][1]/100}
# }).sort("price", pymongo.DESCENDING).limit(10)

# print("추천드리는 그라인더")
# for doc in grinder_max:
#     weight = get_weight(doc)
#     if (weight >= standard["그라인더"][0] and weight<= standard["그라인더"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
# grinder_min = db.item.find({"option": "그라인더", 
#     "price": {"$gte":bud*plan_price["그라인더"][0]/100}}
# ).sort("price", pymongo.ASCENDING).limit(10)

# for doc in grinder_min:
#     weight = get_weight(doc)
#     if (weight >= standard["그라인더"][0] and weight<= standard["그라인더"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==4:
#         break

# # 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
# grinder_median = db.item.find(
#     {"option": "그라인더", 
#     "price": {"$gte":(bud*plan_price["그라인더"][1]/100 + bud*plan_price["그라인더"][0]/100)/2}}
# ).sort("price", pymongo.ASCENDING).limit(10)

# for doc in grinder_median:
#     weight = get_weight(doc)
#     if (weight >= standard["그라인더"][0] and weight<= standard["그라인더"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==6:
#         break

# # 기준에 맞는 제품이 하나도 없을 때 
# if printed==0:
#     grinder_left = db.item.find(
#         {"option": "그라인더", 
#         "price": {"$lte":bud*plan_price["그라인더"][0]/100}
#     }).sort("price", pymongo.ASCENDING).limit(10)
#     grinder_right = db.item.find({
#         "option": "그라인더", 
#         "price": {"$gte":bud*plan_price["그라인더"][1]/100}
#     }).sort("price", pymongo.DESCENDING).limit(10)

#     for doc in grinder_left:
#         if (weight >= standard["그라인더"][0] and weight<= standard["그라인더"][1]):
#             print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
#             printed+=1
#         if printed==2:
#             break
    
#     for doc in grinder_right:
#         if (weight >= standard["그라인더"][0] and weight<= standard["그라인더"][1]):
#             print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
#             printed+=1
#         if printed==4:
#             break





# # 온수기
# printed=0
# # 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
# printed = 0
# boiler_max = db.item.find({
#     "option": "온수기", 
#     "price": {"$lte":bud*plan_price["온수기"][1]/100}
# }).sort("price", pymongo.DESCENDING).limit(10)

# print("추천드리는 온수기")
# for doc in boiler_max:
#     weight = get_weight(doc)
#     if (weight >= standard["온수기"][0] and weight<= standard["온수기"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
# boiler_median = db.item.find(
#     {"option": "온수기", 
#     "price": {"$gte":(bud*plan_price["온수기"][1]/100 + bud*plan_price["온수기"][0]/100)/2}}
# ).sort("price", pymongo.ASCENDING).limit(10)

# for doc in boiler_median:
#     weight = get_weight(doc)
#     if (weight >= standard["온수기"][0] and weight<= standard["온수기"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
# boiler_min = db.item.find({"option": "온수기", 
#     "price": {"$gte":bud*plan_price["온수기"][0]/100}}
# ).sort("price", pymongo.ASCENDING).limit(10)

# for doc in boiler_min:
#     weight = get_weight(doc)
#     if (weight >= standard["온수기"][0] and weight<= standard["온수기"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 기준에 맞는 제품이 하나도 없을 때 
# if printed==0:
#     boiler_left = boiler_min = db.item.find(
#         {"option": "온수기", 
#         "price": {"$lte":bud*plan_price["온수기"][0]/100}
#     }).sort("price", pymongo.ASCENDING).limit(10)
#     boiler_right = db.item.find({
#         "option": "온수기", 
#         "price": {"$gte":bud*plan_price["온수기"][1]/100}
#     }).sort("price", pymongo.DESCENDING).limit(10)

#     for doc in boiler_left:
#         if (weight >= standard["온수기"][0]-10 and weight<= standard["온수기"][1]+10):
#             print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
#             printed+=1
#         if printed==2:
#             break
    
#     for doc in boiler_right:
#         if (weight >= standard["온수기"][0]-10 and weight<= standard["온수기"][1]+10):
#             print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
#             printed+=1
#         if printed==4:
#             break
# print()





# # 제빙기
# printed=0
# # 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
# ice_max = db.item.find({
#     "option": "제빙기", 
#     "price": {"$lte":bud*plan_price["제빙기"][1]/100}
# }).sort("price", pymongo.DESCENDING).limit(10)

# print("추천드리는 제빙기")
# for doc in ice_max:
#     weight = get_weight(doc)
#     if (weight >= standard["제빙기"][0] and weight<= standard["제빙기"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
# ice_min = db.item.find({"option": "제빙기", 
#     "price": {"$gte":bud*plan_price["제빙기"][0]/100}}
# ).sort("price", pymongo.ASCENDING).limit(10)

# for doc in ice_min:
#     weight = get_weight(doc)
#     if (weight >= standard["제빙기"][0] and weight<= standard["제빙기"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
# ice_median = db.item.find(
#     {"option": "제빙기", 
#     "price": {"$gte":(bud*plan_price["제빙기"][1]/100 + bud*plan_price["제빙기"][0]/100)/2}}
# ).sort("price", pymongo.ASCENDING).limit(10)

# for doc in ice_median:
#     weight = get_weight(doc)
#     if (weight >= standard["제빙기"][0] and weight<= standard["제빙기"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 기준에 맞는 제품이 하나도 없을 때 
# if printed==0:
#     ice_left = ice_min = db.item.find(
#         {"option": "제빙기", 
#         "price": {"$lte":bud*plan_price["제빙기"][0]/100}
#     }).sort("price", pymongo.ASCENDING).limit(10)
#     ice_right = db.item.find({
#         "option": "제빙기", 
#         "price": {"$gte":bud*plan_price["제빙기"][1]/100}
#     }).sort("price", pymongo.DESCENDING).limit(10)

#     for doc in ice_left:
#         if (weight >= standard["제빙기"][0] and weight<= standard["제빙기"][1]):
#             print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
#             printed+=1
#         if printed==2:
#             break
    
#     for doc in ice_right:
#         if (weight >= standard["제빙기"][0] and weight<= standard["제빙기"][1]):
#             print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
#             printed+=1
#         if printed==4:
#             break
# print()





# # 냉장고
# printed=0
# # 예산 안에서 가장 비싼 & 무게 기준 안에 들어오는 기계
# fridge_max = db.item.find({
#     "option": "냉장고", 
#     "price": {"$lte":bud*plan_price["냉장고"][1]/100}
# }).sort("price", pymongo.DESCENDING).limit(15)

# print("추천드리는 냉장고")
# for doc in fridge_max:
#     weight = get_weight(doc)
#     if (weight >= standard["냉장고"][0] and weight<= standard["냉장고"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 예산 안에서 가장 싼 & 무게 기준 안에 들어오는 기계
# fridge_min = db.item.find({"option": "냉장고", 
#     "price": {"$gte":bud*plan_price["냉장고"][0]/100}}
# ).sort("price", pymongo.ASCENDING).limit(15)

# for doc in fridge_min:
#     weight = get_weight(doc)
#     if (weight >= standard["냉장고"][0] and weight<= standard["냉장고"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 예산 안에서 중간 & 무게 기준 안에 들어오는 기계
# fridge_median = db.item.find(
#     {"option": "냉장고", 
#     "price": {"$gte":(bud*plan_price["냉장고"][1]/100 + bud*plan_price["냉장고"][0]/100)/2}}
# ).sort("price", pymongo.ASCENDING).limit(15)

# for doc in fridge_median:
#     weight = get_weight(doc)
#     if (weight >= standard["냉장고"][0] and weight<= standard["냉장고"][1]):
#         print(doc["name"]+",", str(weight)+"kg,", str(doc["price"])+"원")
#         printed+=1
#     if printed==2:
#         break

# # 기준에 맞는 제품이 하나도 없을 때 
# if printed==0:
#     fridge_left = fridge_min = db.item.find(
#         {"option": "냉장고", 
#         "price": {"$lte":bud*plan_price["냉장고"][0]/100}
#     }).sort("price", pymongo.ASCENDING).limit(10)
#     fridge_right = db.item.find({
#         "option": "냉장고", 
#         "price": {"$gte":bud*plan_price["냉장고"][1]/100}
#     }).sort("price", pymongo.DESCENDING).limit(10)

#     for doc in fridge_left:
#         if (weight >= standard["냉장고"][0] and weight<= standard["냉장고"][1]):
#             print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
#             printed+=1
#         if printed==2:
#             break
    
#     for doc in fridge_right:
#         if (weight >= standard["냉장고"][0] and weight<= standard["냉장고"][1]):
#             print(doc["name"]+",", str(get_weight(doc))+"kg,", str(doc["price"])+"원")
#             printed+=1
#         if printed==4:
#             break