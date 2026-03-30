from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Optional, List
from datetime import datetime

DATABASE_URL = "sqlite:///./pizza.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PizzaDB(Base):
    __tablename__ = "pizzas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    size = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    ingredients = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(String, default=lambda: str(datetime.now()))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic схемы БЕЗ описаний и Field
class PizzaCreate(BaseModel):
    name: str
    category: str
    size: str
    price: float
    ingredients: List[str]
    is_available: bool = True

class PizzaUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    size: Optional[str] = None
    price: Optional[float] = None
    ingredients: Optional[List[str]] = None
    is_available: Optional[bool] = None

class PizzaOut(BaseModel):
    id: int
    name: str
    category: str
    size: str
    price: float
    ingredients: List[str]
    is_available: bool
    created_at: str

app = FastAPI()

# Функция для добавления тестовых данных (запустится один раз)
def init_db(db: Session):
    if db.query(PizzaDB).count() == 0:
        test_pizzas = [
            PizzaDB(name="Маргарита", category="vegetarian", size="30", price=599.0, ingredients='["томаты", "сыр", "базилик"]', is_available=True),
            PizzaDB(name="Пепперони", category="meat", size="30", price=699.0, ingredients='["пепперони", "сыр", "томатный соус"]', is_available=True),
            PizzaDB(name="Диабло", category="spicy", size="40", price=899.0, ingredients='["острый соус", "паприка", "курица"]', is_available=False),
        ]
        db.add_all(test_pizzas)
        db.commit()

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    init_db(db)
    db.close()

# Получить все пиццы (с фильтрами)
@app.get("/pizzas")
def get_pizzas(db: Session = Depends(get_db), category: Optional[str] = None, size: Optional[str] = None, max_price: Optional[float] = None):
    query = db.query(PizzaDB)
    if category:
        query = query.filter(PizzaDB.category == category)
    if size:
        query = query.filter(PizzaDB.size == size)
    if max_price:
        query = query.filter(PizzaDB.price <= max_price)
    return query.all()

# Получить пиццу по ID
@app.get("/pizzas/{pizza_id}")
def get_pizza(pizza_id: int, db: Session = Depends(get_db)):
    pizza = db.query(PizzaDB).filter(PizzaDB.id == pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    return pizza

# Создать пиццу
@app.post("/pizzas")
def create_pizza(pizza: PizzaCreate, db: Session = Depends(get_db)):
    db_pizza = PizzaDB(**pizza.dict(), ingredients=str(pizza.ingredients), created_at=str(datetime.now()))
    db.add(db_pizza)
    db.commit()
    db.refresh(db_pizza)
    return db_pizza

# Обновить пиццу
@app.put("/pizzas/{pizza_id}")
def update_pizza(pizza_id: int, pizza_update: PizzaUpdate, db: Session = Depends(get_db)):
    db_pizza = db.query(PizzaDB).filter(PizzaDB.id == pizza_id).first()
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    update_data = pizza_update.dict(exclude_unset=True)
    if "ingredients" in update_data:
        update_data["ingredients"] = str(update_data["ingredients"])
    for field, value in update_data.items():
        setattr(db_pizza, field, value)
    db.commit()
    return db_pizza

# Удалить пиццу
@app.delete("/pizzas/{pizza_id}")
def delete_pizza(pizza_id: int, db: Session = Depends(get_db)):
    db_pizza = db.query(PizzaDB).filter(PizzaDB.id == pizza_id).first()
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    db.delete(db_pizza)
    db.commit()
    return {"message": "Pizza deleted"}

# Получить категории (уникальные)
@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(PizzaDB.category).distinct().all()
    return [c[0] for c in categories]

# Получить доступные пиццы
@app.get("/pizzas/available")
def get_available_pizzas(db: Session = Depends(get_db)):
    pizzas = db.query(PizzaDB).filter(PizzaDB.is_available == True).all()
    return pizzas