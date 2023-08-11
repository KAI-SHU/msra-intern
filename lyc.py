import json
feature_map_test = {}
feature_map_train = {}
with open("train.jsonl",'r',encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        feature = data["text"].split()[0]
        if feature in feature_map_train.keys():
            feature_map_train[feature].append(data)
        else:
            feature_map_train[feature] = [data]
with open("testA.jsonl",'r',encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        feature = data["text"].split()[0]
        if feature in feature_map_test.keys():
            feature_map_test[feature].append(data)
        else:
            feature_map_test[feature] = [data]

a = set(feature_map_test.keys())
b = set(feature_map_train.keys())
respond_map_ = {}
for i in a&b:
    respond_map_[i] = {"train":[],"test":[]}
    for j in feature_map_test[i]:
        respond_map_[i]["test"].append(j)
    for j in feature_map_train[i]:
        respond_map_[i]["train"].append(j)
print(a&b,len(a-b))
sec_test = {}
sec_train = {}
for i in a-b : 
    for j in feature_map_test[i]:
        if j["text"].split()[1] in sec_test.keys():
            sec_test[j["text"].split()[1]].append(j)
        else:
            if len(j["text"].split()[1]) > 4:
                sec_test[j["text"].split()[1]] = [j]
            else:
                sec_test[j["text"].split()[1] + j["text"].split()[2]] = [j]
for i in b-a : 
    for j in feature_map_train[i]:
        if j["text"].split()[1] in sec_train.keys():
            sec_train[j["text"].split()[1]].append(j)
        else:
            if len(j["text"].split()[1]) > 4:
                sec_train[j["text"].split()[1]] = [j]
            else:
                sec_train[j["text"].split()[1] + j["text"].split()[2]] = [j]

test = set(sec_test.keys())
train = set(sec_train.keys())
respond_map = {}
for i in test&train:
    respond_map[i] = {"train":[],"test":[]}
    for j in sec_test[i]:
        respond_map[i]["test"].append(j)
    for j in sec_train[i]:
        respond_map[i]["train"].append(j)


print("same:", test&train)
print("diff",test-train,len(test-train))      
for i in test-train:
    for j in sec_test[i]:
        print(j["id"])
with open("correspond.json",'w',encoding="utf-8") as f:
    f.write(json.dumps(respond_map,ensure_ascii=False))

        