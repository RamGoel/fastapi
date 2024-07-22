from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    id:int
    title: str
    completed:bool=False

class TodoBody(BaseModel):
    title: str

todos:list[Todo]=[
    {
        "id":1,
        "title":"Learn FastAPI",
        "completed":False
    },
    {
        "id":2,
        "title":"Learn Golang",
        "completed":False
    }
]


@app.get("/")
async def root():
    return {"message": "Hello World, Server is running"}


@app.get("/todos")
async def root(q:Union[str,None]=None):
    print(q)
    if q:
        return [todo for todo in todos if q in todo["title"].lower()]
    return todos

@app.post("/todos/new")
async def create_item(todo:TodoBody) -> dict:
        todos.append({
            "id":len(todos)+1,
            "title":todo.title,
            "completed":False
        })
        return {"message": "Todo added"}


@app.delete("/todos/delete")
async def delete_item(id:str) -> dict:
        try:
             if(int(id)>=len(todos)):
                return {"message": "Todo not found"}
             else:
                todos.remove([todo for todo in todos if todo["id"]==int(id)][0])
                return {"message": "Todo deleted"}
        except:
            return {"message": "Some error occured"}


@app.put("/todos/update")
async def update_item(body:TodoBody, id:str) -> dict:
  newTodos=[]
  for i in len(todos):
      if(todos[i].id==int(id)):
        newTodos.append({"id":todos[i].id,"title":body.title,"completed":todos[i].completed})
      else:
        newTodos.append(todos[i])
  todos.clear()
  todos.extend(newTodos)
  return {"message": "Todo Updated"}