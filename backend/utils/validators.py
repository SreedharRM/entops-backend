# Empty validators.py file
from pydantic import BaseModel, EmailStr
from typing import List, Dict

class TaskRequest(BaseModel):
    type: str
    data: Dict

class EmailData(BaseModel):
    from_: EmailStr
    subject: str
    body: str

class ContractorInfo(BaseModel):
    name: str
    email: EmailStr
    role: str
    start_date: str

class LeadList(BaseModel):
    leads: List[Dict]
