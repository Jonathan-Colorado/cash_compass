from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from enum import Enum
from bson import ObjectId
from pydantic import Field, BaseModel
from moneyed import Money, USD, EUR

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class AccountType(str, Enum):
    CHECKING = 'Checking'
    SAVINGS = 'Savings'
    CREDIT_CARD = 'Credit Card'
    CD = 'CD'
    MONEY_MARKET = 'Money Market'
    PAYPAL = 'PayPal'
    AUTO_LOAN = 'Auto Loan'
    MORTGAGE = 'Mortgage'
    HOME_EQUITY = 'Home Equity Line of Credit'
    LOAN = 'loan'
    STUDENT_LOAN = 'Student Loan'
    TUITION_529 = '529'
    RETIREMENT_401K = '401(k)'
    BROKERAGE = 'brokerage'
    CRYPTO = 'crypto'
    ESA = 'Coverdell ESA'
    ANNUITY = 'Annuity'
    TRAD_IRA = 'Traditional IRA'
    ROTH_IRA = 'Roth IRA'
    MUTUAL_FUND = 'Mutual Fund'
    ROTH_401K = 'Roth 401(k)'

class AccountStatus(str, Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    HIDDEN = 'hidden'

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    class Config:
        json_encoders = {ObjectId: str}

class Institution(MongoBaseModel):
    name: str = Field(...)

class AccountBase(MongoBaseModel):
    account_number: str | None = None
    account_type: AccountType = Field(...)
    rate: float | None = None
    name: str = Field(...)
    institution: Institution | None = None

class AccountUpdate(MongoBaseModel):
    rate: float | None = None

class AccountDB(AccountBase):
    pass    
    