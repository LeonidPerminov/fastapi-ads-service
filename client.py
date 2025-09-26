import requests


base = "http://localhost:8000"


# create
r = requests.post(
f"{base}/advertisement",
json={
"title": "MacBook Pro 14",
"description": "M3, 18GB RAM, как новый",
"price": 1899.0,
"author": "leonid",
},
)
print("CREATE:", r.status_code, r.text)


ad_id = r.json()["id"]


# get
r = requests.get(f"{base}/advertisement/{ad_id}")
print("GET:", r.status_code, r.json())


# search
r = requests.get(f"{base}/advertisement", params={"author": "leon"})
print("SEARCH:", r.status_code, r.json())


# update
r = requests.patch(
f"{base}/advertisement/{ad_id}",
json={"price": 1799.0, "title": "MacBook Pro 14 M3"},
)
print("PATCH:", r.status_code, r.text)


# delete
r = requests.delete(f"{base}/advertisement/{ad_id}")
print("DELETE:", r.status_code, r.text)