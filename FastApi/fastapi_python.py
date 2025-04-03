from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class AvailableCuisines(str, Enum):
    indian = 'indian'
    american = 'american'
    italian = 'italian'

food_items = {
    'indian':['Samosa', 'Dosa'],
    'american': ['Hot dog', 'Apple pie'],
    'italian': ['Ravioli','Pizza']
}
valid_cuisines = food_items.keys()

coupon_code = {
    1: '10%',
    2: '20%',
    3: '30%'
}

@app.get('/get_coupon/{code}')
async def get_items(code:int):
    return {'discount amount' : coupon_code.get(code)}


@app.get("/hello/{name}")
async def hello(name):
    return {"message": f"Hello {name}"} 

# @app.get('/get_items/{cuisine}')
# async def available(cuisine):
#     if cuisine not in valid_cuisines:
#         return f"Supported cuisines are {valid_cuisines}"
#     return food_items.get(cuisine)

@app.get('/get_items/{cuisine}')
async def get_items(cuisine:AvailableCuisines):
    return food_items.get(cuisine)