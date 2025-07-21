from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime


# Address Schemas and Model
class AddressBase(SQLModel):
    street: str
    city: str
    state: str
    zip_code: str


class Address(AddressBase, table=True):
    # By making the foreign key the primary key, we enforce a one-to-one relationship
    employee_id: Optional[int] = Field(
        default=None, foreign_key="employees.id", primary_key=True
    )
    employee: "Employee" = Relationship(back_populates="address")


class AddressCreate(AddressBase):
    pass


class AddressRead(AddressBase):
    pass


# Shared properties
class EmployeeBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)


class AttendanceBase(SQLModel):
    clock_in: datetime = Field(default_factory=datetime.utcnow)
    clock_out: Optional[datetime] = None


# Database Model for Employee
class Employee(EmployeeBase, table=True):
    __tablename__ = "employees"
    id: Optional[int] = Field(default=None, primary_key=True)

    attendances: List["Attendance"] = Relationship(back_populates="employee")
    # Add the one-to-one relationship to Address
    address: Optional[Address] = Relationship(back_populates="employee", sa_relationship_kwargs={'cascade': "all, delete-orphan"})


# Database Model for Attendance
class Attendance(AttendanceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    employee_id: Optional[int] = Field(default=None, foreign_key="employees.id")
    employee: Optional[Employee] = Relationship(back_populates="attendances")


# Properties to receive via API on creation
class EmployeeCreate(EmployeeBase):
    pass


class AttendanceCreate(SQLModel):
    employee_id: int


# Properties to return via API, hiding sensitive data
class EmployeeRead(EmployeeBase):
    id: int


class AttendanceRead(AttendanceBase):
    id: int


# Properties to return via API with relationships
class EmployeeReadWithDetails(EmployeeRead):
    attendances: List[AttendanceRead] = []
    address: Optional[AddressRead] = None