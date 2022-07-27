from decimal import Decimal
from logging import root
from pydantic import BaseModel, root_validator


class Chain(BaseModel):
    id: int
    name: str
    token_contract_address: str

    class Config:
        orm_mode = True


class AddressBalance(BaseModel):
    address: str
    balance: Decimal
    chain: Chain

    class Config:
        orm_mode = True


class ChainBalance(BaseModel):
    chain: Chain
    balance: Decimal

    class Config:
        orm_mode = True


class Holder(BaseModel):
    address: str
    balances: dict[int, Decimal]
    total_balance: Decimal | None

    @root_validator
    def compute_total_balance(cls, values) -> dict:
        total_balance = sum([b for _, b in values["balances"].items()])
        values["total_balance"] = total_balance
        return values
