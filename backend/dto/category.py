from pydantic import BaseModel


class CategoryCreate(BaseModel):
    type: str
    main: str
    sub: str = ""


class CategoryDelete(BaseModel):
    type: str
    main: str = ""
    sub: str = ""


class CategoryUpdate(BaseModel):
    old_type: str
    old_main: str = ""
    old_sub: str = ""
    new_type: str
    new_main: str = ""
    new_sub: str = ""
