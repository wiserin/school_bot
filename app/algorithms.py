from random import randint
from app.arrays import objects

# algorithm for token generation
async def token_generator():
    pre_token = []
    token = ''

    for i in range(20):
        number = randint(0, 69)
        object = objects[number]
        pre_token.append(object)

    return token.join(pre_token)
    
    