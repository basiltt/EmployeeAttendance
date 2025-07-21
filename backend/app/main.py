from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .database import get_db, engine
from . import crud, models

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.SQLModel.metadata.create_all)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/employees/", response_model=models.EmployeeRead)
async def create_employee(employee: models.EmployeeCreate, db: AsyncSession = Depends(get_db)):
    db_employee = await crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_employee(db=db, employee=employee)

@app.get("/employees/", response_model=List[models.EmployeeReadWithDetails])
async def read_employees(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    employees = await crud.get_employees(db, skip=skip, limit=limit)
    return employees

# New Address Endpoints
@app.put("/employees/{employee_id}/address", response_model=models.AddressRead)
async def upsert_employee_address(employee_id: int, address: models.AddressCreate, db: AsyncSession = Depends(get_db)):
    db_employee = await crud.get_employee(db, employee_id=employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return await crud.create_or_update_address(db=db, employee_id=employee_id, address_in=address)

@app.delete("/employees/{employee_id}/address", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_address(employee_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_address(db=db, employee_id=employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found for this employee")
    return

# Updated Attendance Endpoints
@app.post("/attendance/clock-in/", response_model=models.AttendanceRead)
async def clock_in_employee(attendance: models.AttendanceCreate, db: AsyncSession = Depends(get_db)):
    result = await crud.clock_in(db=db, employee_id=attendance.employee_id)
    if isinstance(result, str):
        if result == "NO_ADDRESS":
            raise HTTPException(status_code=400, detail="Employee must have an address to clock in.")
        if result == "ALREADY_CLOCKED_IN":
            raise HTTPException(status_code=400, detail="Employee already clocked in.")
        if result == "NO_EMPLOYEE":
            raise HTTPException(status_code=404, detail="Employee not found.")
    return result

@app.put("/attendance/clock-out/{employee_id}", response_model=models.AttendanceRead)
async def clock_out_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.clock_out(db=db, employee_id=employee_id)
    if not result:
        raise HTTPException(status_code=404, detail="No open clock-in found for this employee.")
    return result