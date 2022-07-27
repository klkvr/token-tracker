from app.database import SessionLocal
from sqlalchemy.future import select
from app.models import Transaction, Chain
from sqlalchemy import Numeric, func, case, String, column, join, true, desc, text
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import Values


def get_chains(session: Session):
    sql = select(Chain)
    return session.execute(sql).scalars().all()


def _get_balances_table(session: Session):
    """
    Function for creating complicated expression for generation of balance table
    from transactions table
    """
    c = aliased(Chain, name="chain")
    t = aliased(Transaction, name="transaction")
    balance_changes = (
        Values(column("address", String), column("balance_change", Numeric), name="balance_changes")
        .data([(t.to_address, t.value), (t.from_address, -t.value)])
        .lateral()
    )
    balances = (
        select(
            balance_changes.c.address.label("address"), func.sum(balance_changes.c.balance_change).label("balance"), c
        )
        .select_from(join(join(t, c, t.chain_id == c.id), balance_changes, true()))
        .group_by(balance_changes.c.address)
        .group_by(c.id)
        .subquery("balances")
    )
    return (
        select(balances.c.balance, balances.c.address, c)
        .select_from(join(balances, c, balances.c.id == c.id))
        .where(balances.c.balance > 0)
        .order_by(desc(balances.c.balance))
    )


def get_balances_list(session: Session):
    balances = _get_balances_table(session)
    return session.execute(balances).all()


def get_total_supplies(session: Session):
    c = aliased(Chain, name="chain")
    balances = _get_balances_table(session)
    supplies = select(func.sum(balances.c.balance).label("value"), c).where(balances.c.id == c.id).group_by(c.id)
    return session.execute(supplies).all()
