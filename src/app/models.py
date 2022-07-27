from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship


class Chain(Base):
    """Single chain of token"""
    __tablename__ = "chains"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rpc = Column(String, nullable=False)
    token_contract_address = Column(String, nullable=False)
    last_checked_block = Column(Integer, nullable=False, server_default="0")

    transactions = relationship("Transaction", back_populates="chain", cascade="all, delete-orphan")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} (Chain ID: {self.id})"


class Transaction(Base):
    """Single token transfer"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(String)
    chain_id = Column(Integer, ForeignKey("chains.id", ondelete="CASCADE"))
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    value = Column(Numeric(20, 10), nullable=False)

    chain = relationship("Chain", back_populates="transactions")

    def __str__(self):
        return f"{self.from_address} -> {self.to_address} {self.value} token"


class NamedAddress(Base):
    """Model used for marking addresses with nicknames"""
    __tablename__ = "named_addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)
    name = Column(String)