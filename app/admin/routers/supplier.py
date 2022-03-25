from typing import Optional
from fastapi import APIRouter,HTTPException, UploadFile,status,Depends,File,Response
from app.database import get_db
from app import models,schemas,oauth,utils
from sqlalchemy.orm import Session

router=APIRouter(prefix="/supplier",tags=['supplier'])

@router.get("/")
def get_suppliers(db:Session=Depends(get_db)):

    get_supplier=db.query(models.Supplier).all()
    return get_supplier

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_suppliers(payload:schemas.CreateSuppliers,db:Session=Depends(get_db)):
    query_phone=db.query(models.Supplier).filter(models.Supplier.supplier_phone==payload.supplier_phone).first()
    if query_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"a supplier with {payload.supplier_phone} already exist")
    create_supplier=models.Supplier(**payload.dict())
    db.add(create_supplier)
    db.commit()
    db.refresh(create_supplier)
    return create_supplier

@router.get("/{id}")
def get_supplier_by_id(id:int,db:Session=Depends(get_db)):
 
    result=db.query(models.Supplier).filter(models.Supplier.id==id).first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the Supplier with id {id} was not found")
    return result

@router.put("/{id}")
def update_suppliers(payload:schemas.CreateSuppliers,id:int,db:Session=Depends(get_db)):
    
    update_supplier=db.query(models.Supplier).filter(models.Supplier.supplier_id==id)
    if not update_supplier.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the supplier with id {id} was not found")
    
    
    update_supplier.update(payload.dict())
    db.commit()

    return update_supplier.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_suppliers(id:int,db:Session=Depends(get_db)):
    
    delete_supplier=db.query(models.Supplier).filter(models.Supplier.supplier_id==id)
    if not delete_supplier.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the supplier with id {id} was not found")

    delete_supplier.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
   

    