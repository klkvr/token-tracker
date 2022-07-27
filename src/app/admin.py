from sqladmin import Admin, ModelAdmin
from fastapi import FastAPI
from .models import Chain, Transaction
from sqlalchemy.engine import Engine


class ChainAdmin(ModelAdmin, model=Chain):
    name = "Chain"
    name_plural = "Chains"
    column_list = [Chain.name, Chain.last_checked_block]
    form_excluded_columns = [Chain.transactions, Chain.last_checked_block]


class TransactionAdmin(ModelAdmin, model=Transaction):
    name = "Transaction"
    name_plural = "Transactions"

    column_list = [Transaction.from_address, Transaction.to_address, Transaction.value, Transaction.chain]
    column_searchable_list = [Transaction.from_address, Transaction.to_address]
    column_sortable_list = [Transaction.value]


def setup(app: FastAPI, engine: Engine, path: str):
    admin = Admin(app, engine, base_url=path)

    admin.register_model(ChainAdmin)
    admin.register_model(TransactionAdmin)
