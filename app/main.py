from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas 

#create tables in the databse
models.Base.metadata.create_all(bind=database.engine)

app=FastAPI()

#Dependency:get a database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
# create post->add new employee

@app.post("/employees/")
def create_employee(employee: schemas.EmployeeCreate):
    db = database.SessionLocal() # open session
    new_employee = models.Employee(
        name=employee.name,
        role=employee.role,
        email=employee.email
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    db.close()      # close session
    return new_employee

@app.get("/employees/")
def read_employees():
    db = database.SessionLocal()
    employees = db.query(models.Employee).all()
    db.close()
    return employees
@app.get("/employees/{employee_id}")
def read_employee(employee_id: int):
    db = database.SessionLocal()
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    db.close()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, updated: schemas.EmployeeCreate):
    db = database.SessionLocal()
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        db.close()
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.name = updated.name
    employee.role = updated.role
    employee.email = updated.email
    db.commit()
    db.refresh(employee)
    db.close()
    return employee
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    db = database.SessionLocal()
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        db.close()
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    db.close()
    return {"message": "Employee deleted successfully"}





