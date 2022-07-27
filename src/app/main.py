from decimal import Decimal

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import admin, crud, schemas, config
from .database import SessionLocal, engine


app = FastAPI(root_path=config.ROOT_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin.setup(app, engine, config.ADMIN_PANEL_PATH)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/chains", response_model=list[schemas.Chain])
def get_chains(session: Session = Depends(get_db)):
    return crud.get_chains(session)


@app.get("/holders", response_model=list[schemas.Holder])
def get_holders(session: Session = Depends(get_db)):
    holders: list[schemas.AddressBalance] = map(schemas.AddressBalance.from_orm, crud.get_balances_list(session))
    holders_dict: dict[str, schemas.Chain] = {}
    for holder in holders:
        if holder.address not in holders_dict:
            holders_dict[holder.address] = {}
        holders_dict[holder.address][holder.chain.id] = holder.balance
    top_holders: list[schemas.Holder] = []
    for address, balances in holders_dict.items():
        holder = schemas.Holder(address=address, balances=balances)
        top_holders.append(holder)
    top_holders.sort(key=lambda h: h.total_balance, reverse=True)
    return top_holders


@app.get("/total_supplies")
def get_supplies(session: Session = Depends(get_db)):
    supplies: dict[int, Decimal] = {}
    for supply in crud.get_total_supplies(session):
        supplies[supply.chain.id] = supply.value
    return supplies
