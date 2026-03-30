from pydantic import BaseModel
from typing import Optional

class Pizza(BaseModel):
    id: Optional[int] = None
    name: str
    price: float

