import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class UserBaseAttrs(BaseModel):
    name: str
    surname: str
    age: Optional[int] = None
    country: Optional[str] = None

class User(UserBaseAttrs):
    id: int

users_list = [
    User(id=2, name='Alistair', surname='Hamerlock', age=51, country="England"),
    User(id=10, name='Lilith', surname='Turner', country="USA"),
    User(id=114, name='Austin', surname='Wintory'),
    User(id=3, name='Elizabeth', surname='Shaw', age=33),
    User(id=4, name='Elly', surname='Fisher', age=39, country="Honduras"),
    User(id=15, name='Takeshi', surname='Kitano', country="Japan"),
    User(id=71, name='Melissa', surname='Johnes'),
]

@app.get("/")
async def home():
    return {"Home page."}

@app.get('/users/')
def users():
    return users_list

@app.get('/users/{id}')
def user(id: int):
    for user in users_list:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="No such user exists.")

@app.post('/users/')
def add_user(attrs: UserBaseAttrs):
    user = User(id=len(users_list) + 1, **attrs.dict())
    users_list.append(user)
    return user

@app.put('/users/{id}')
def update_user(id: int, attrs: UserBaseAttrs):
    for user in users_list:
        if user.id == id:
            user.name = attrs.name
            user.surname = attrs.surname
            user.age = attrs.age
            user.country = attrs.country
            return user
    raise HTTPException(status_code=404, detail="No such user exists.")

@app.delete('/users/{id}')
def delete_user(id: int):
    for user in users_list:
        if user.id == id:
            users_list.remove(user)
            return {'message': 'User deleted successfully.'}
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)