from typing import Optional
from fastapi import APIRouter,HTTPException, Response, UploadFile,status,Depends,File
from app.database import get_db
from app import models,schemas,oauth,utils
from sqlalchemy.orm import Session

router=APIRouter(prefix="/product",tags=['product'])

@router.get("/")
def get_product(db:Session=Depends(get_db)):

    get_product=db.query(models.Product).all()
    return get_product

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_product(payload:schemas.CreateProduct,db:Session=Depends(get_db)):

    payload_dict=payload.dict()
    find_supplier=payload_dict["supplier_name"]
    query=db.query(models.Supplier).filter(models.Supplier.supplier_name ==find_supplier).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the supplier named {find_supplier} was not found")
    product_name=db.query(models.Product).filter(models.Product.product_title==payload.product_title).first()
    if product_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"the product with title {payload.product_title} already exists")
    # if file:
    #     img_destination=utils.store_file('product',file,payload.product_title)
    #     payload_dict['product_img']=img_destination
    # print(query.salary_id)
    payload_dict.pop("supplier_name")
    payload_dict['supplier_id']=query.supplier_id
    create_product=models.Product(**payload_dict)
    db.add(create_product)
    db.commit()
    db.refresh(create_product)
    return create_product


@router.get("/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
 
    result=db.query(models.Product).filter(models.Product.product_id==id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the Product with id {id} was not found")
    return result

@router.put("/{id}")
def update_product(id:int,payload:schemas.CreateProduct,db:Session=Depends(get_db)):

    update_product=db.query(models.Product).filter(models.Product.product_id==id)
    if not update_product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the product with id {id} was not found")
    payload_dict=payload.dict()
    # if file:
    #     img_destination=utils.store_file('product',file,payload.product_title)
    #     payload_dict['product_img']=img_destination
    find_supplier=payload_dict["supplier_name"]
    query=db.query(models.Supplier).filter(models.Supplier.supplier_name ==find_supplier).first()
    # print(query.salary_id)
    payload_dict.pop("supplier_name")
    payload_dict['supplier_id']=query.supplier_id
    update_product.update(payload_dict)
    db.commit()
    return update_product.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db:Session=Depends(get_db)):
    del_product=db.query(models.Product).filter(models.Product.product_id==id)
    if not del_product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the product with the id {id} was not found")

    del_product.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    