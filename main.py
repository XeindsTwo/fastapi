from fastapi import FastAPI

app = FastAPI(
    title="Dodo Pizza API",
    description="""
API для управления меню пиццерии

### Категории пицц:
- **meat** — Мясные (Пепперони, Мясная, Бургер-пицца)
- **vegetarian** — Вегетарианские (Маргарита, Овощная)
- **spicy** — Острые (Диабло, Острая чикен)
- **seafood** — С морепродуктами (Дары моря, Лосось)
- **cheese** — Сырные (Четыре сыра, Сырная сторона)
    """,
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в мир пицц"}

@app.get("/pizzas")
def get_pizzas():
    return {"pizzas": ["Маргарита", "Пепперони", "Гавайская"]}