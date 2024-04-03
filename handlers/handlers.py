from sqlalchemy.orm import Session
from models import models
from schemas import schemas


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        update_data = product_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


def create_material_for_product(db: Session, material: schemas.MaterialCreate, product_id: int):
    # Assuming product_id is not in MaterialCreate, it will not be included in material.dict()
    db_material = models.Material(**material.dict(), product_id=product_id)
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def get_materials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Material).offset(skip).limit(limit).all()


def get_material(db: Session, material_id: int):
    return db.query(models.Material).filter(models.Material.id == material_id).first()


def get_materials_of_product(db: Session, product_id: int):
    return db.query(models.Material).filter(models.Material.product_id == product_id).all()


def update_material(db: Session, material_id: int, material_update: schemas.MaterialUpdate):
    db_material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if db_material:
        update_data = material_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_material, key, value)
        db.commit()
        db.refresh(db_material)
    return db_material


def delete_material(db: Session, material_id: int):
    db_material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if db_material:
        db.delete(db_material)
        db.commit()
    return db_material
