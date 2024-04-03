from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import models
from schemas import schemas
from handlers import handlers as crud
from storage.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Products",
        "description": "Operations related to products.",
    },
    {
        "name": "Materials",
        "description": "Manage materials for products.",
    },
]

app = FastAPI(
    title="Product Info API",
    description="This is a very custom description of Product Info. It supports Markdown.",
    version="1.0.0",
    openapi_tags=tags_metadata
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------- Products ----------------------------------------------------------------------------

@app.post("/products/", response_model=schemas.ProductRead,  tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)


@app.get("/products/", response_model=List[schemas.ProductRead],  tags=["Products"])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/products/{product_id}", response_model=schemas.ProductRead,  tags=["Products"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put("/products/{product_id}", response_model=schemas.ProductRead,  tags=["Products"])
def update_product(product_id: int, product_update: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db=db, product_id=product_id, product_update=product_update)


@app.patch("/products/{product_id}", response_model=schemas.ProductRead,  tags=["Products"])
def partial_update_product(product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db=db, product_id=product_id, product_update=product_update)


@app.delete("/products/{product_id}", response_model=schemas.ProductRead,  tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db=db, product_id=product_id)


# --------------------------------- Materials ----------------------------------------------------------------------------  

@app.post("/materials/product/{product_id}", response_model=schemas.MaterialRead,  tags=["Materials"])
def create_material_for_product(product_id: int, material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_material_for_product(db=db, material=material, product_id=product_id)


@app.get("/materials/", response_model=List[schemas.MaterialRead],  tags=["Materials"])
def read_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    materials = crud.get_materials(db, skip=skip, limit=limit)
    return materials

@app.get("/materials/{material_id}", response_model=schemas.MaterialRead,  tags=["Materials"])
def read_material(material_id: int, db: Session = Depends(get_db)):
    db_material = crud.get_material(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_material


@app.get("/materials/{product_id}", response_model=schemas.MaterialRead,  tags=["Materials"], description="Read all materials of a product")
def read_materials_of_product(product_id: int, db: Session = Depends(get_db)):
    db_material = crud.get_materials_of_product(db, product_id=product_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_material


@app.put("/materials/{material_id}", response_model=schemas.MaterialRead, tags=["Materials"])
def update_material(material_id: int, material_update: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return crud.update_material(db=db, material_id=material_id, material_update=material_update)


@app.patch("/materials/{material_id}", response_model=schemas.MaterialRead, tags=["Materials"])
def partial_update_material(material_id: int, material_update: schemas.MaterialUpdate, db: Session = Depends(get_db)):
    db_material = crud.get_material(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return crud.update_material(db=db, material_id=material_id, material_update=material_update)


@app.delete("/materials/{material_id}", response_model=schemas.MaterialRead, tags=["Materials"])
def delete_material(material_id: int, db: Session = Depends(get_db)):
    return crud.delete_material(db=db, material_id=material_id)
