from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from . import models


# Employee CRUD
async def get_employee_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.Employee).where(models.Employee.email == email))
    return result.scalars().first()


async def get_employee(db: AsyncSession, employee_id: int):
    # Eager load address and attendances
    query = select(models.Employee).where(models.Employee.id == employee_id).options(
        selectinload(models.Employee.attendances),
        selectinload(models.Employee.address)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def get_employees(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Employee).options(
            selectinload(models.Employee.attendances),
            selectinload(models.Employee.address)
        ).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_employee(db: AsyncSession, employee: models.EmployeeCreate):
    db_employee = models.Employee.model_validate(employee)
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee


# Address CRUD
async def create_or_update_address(db: AsyncSession, employee_id: int, address_in: models.AddressCreate):
    # Get the existing address
    existing_address = await db.get(models.Address, employee_id)
    if existing_address:
        # Update existing address
        address_data = address_in.model_dump(exclude_unset=True)
        for key, value in address_data.items():
            setattr(existing_address, key, value)
        db.add(existing_address)
        await db.commit()
        await db.refresh(existing_address)
        return existing_address
    else:
        # Create new address
        new_address = models.Address(**address_in.model_dump(), employee_id=employee_id)
        db.add(new_address)
        await db.commit()
        await db.refresh(new_address)
        return new_address


async def delete_address(db: AsyncSession, employee_id: int):
    address = await db.get(models.Address, employee_id)
    if address:
        await db.delete(address)
        await db.commit()
        return True
    return False


# Attendance CRUD
async def clock_in(db: AsyncSession, employee_id: int):
    # Get employee and check for an address
    employee = await get_employee(db, employee_id)
    if not employee:
        return "NO_EMPLOYEE"
    if not employee.address:
        return "NO_ADDRESS"

    # Check for existing open clock-in
    query = select(models.Attendance).where(models.Attendance.employee_id == employee_id, models.Attendance.clock_out == None)
    existing_attendance = await db.execute(query)
    if existing_attendance.scalars().first():
        return "ALREADY_CLOCKED_IN"  # Already clocked in

    db_attendance = models.Attendance(employee_id=employee_id)
    db.add(db_attendance)
    await db.commit()
    await db.refresh(db_attendance)
    return db_attendance


async def clock_out(db: AsyncSession, employee_id: int):
    query = select(models.Attendance).where(models.Attendance.employee_id == employee_id, models.Attendance.clock_out == None)
    result = await db.execute(query)
    db_attendance = result.scalars().first()

    if db_attendance:
        db_attendance.clock_out = models.datetime.utcnow()
        await db.commit()
        await db.refresh(db_attendance)
    return db_attendance