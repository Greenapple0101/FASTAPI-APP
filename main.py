from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import os

app = FastAPI()

# To-Do 항목 모델
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

# To-Do 생성용 모델 (id 없음)
class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

# JSON 파일 경로
TODO_FILE = "todo.json"

# JSON 파일에서 To-Do 항목 로드
def load_todos():
    try:
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r") as file:
                data = json.load(file)
                # Ensure we always return a list
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'todos' in data:
                    return data['todos']
                else:
                    return []
        return []
    except (json.JSONDecodeError, FileNotFoundError, KeyError):
        return []

# JSON 파일에 To-Do 항목 저장
def save_todos(todos):
    try:
        with open(TODO_FILE, "w") as file:
            json.dump(todos, file, indent=4)
        print(f"DEBUG: Successfully saved {len(todos)} todos to {TODO_FILE}")
    except Exception as e:
        print(f"ERROR: Failed to save todos: {e}")
        raise

# To-Do 목록 조회
@app.get("/todos", response_model=list[TodoItem])
def get_todos():
    return load_todos()

# 신규 To-Do 항목 추가
@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoCreate):
    todos = load_todos()
    print(f"DEBUG: todos type: {type(todos)}, content: {todos}")
    
    # Ensure todos is a list
    if not isinstance(todos, list):
        print(f"ERROR: todos is not a list, it's {type(todos)}")
        todos = []
    
    # Generate new ID
    new_id = max([t.get("id", 0) for t in todos], default=0) + 1
    new_todo = TodoItem(
        id=new_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    todos.append(new_todo.dict())
    save_todos(todos)
    return new_todo

# To-Do 항목 수정
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(updated_todo.dict())
            save_todos(todos)
            return updated_todo
    raise HTTPException(status_code=404, detail="To-Do item not found")

# To-Do 항목 삭제
@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    todos = load_todos()
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)
    return {"message": "To-Do item deleted"}

# HTML 파일 서빙
@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Template file not found</h1>", status_code=500)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading template: {str(e)}</h1>", status_code=500)