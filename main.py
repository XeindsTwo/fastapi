from fastapi import FastAPI

tags_metadata = [
    {
        "name": "Pizzas",
        "description": "Управление меню пицц — просмотр, добавление, обновление, удаление",
    },
    {
        "name": "Categories",
        "description": "Категории пицц: мясные, вегетарианские, острые, с морепродуктами, сырные",
    },
]

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
    openapi_tags=tags_metadata
)


@app.get("/", tags=["Pizzas"])
def read_root():
    return {"message": "Добро пожаловать в мир пицц"}


@app.get(
    "/pizzas",
    tags=["Pizzas"],
    summary="Получить список пицц",
    description="Возвращает пиццы из меню. Можно фильтровать по категории, размеру и максимальной цене",
)
def get_pizzas():
    return {"message": "Пиццы"}


@app.get("/categories", tags=["Categories"])
def get_categories():
    return {"pizzas": ["Маргарита", "Пепперони", "Гавайская"]}
