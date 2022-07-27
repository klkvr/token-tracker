from decimal import Decimal
import time
import traceback
from app.models import Chain, Transaction
from app.eth import Ethereum
from sqlalchemy.orm import Session
from .database import SessionLocal
from sqlalchemy.future import select
import logging
import sys
from concurrent.futures import Future, ThreadPoolExecutor


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def monitor_chain(chain_id: int):
    """Function for monitoring last blocks of given chain to find transfers of our token"""
    while True:
        session = SessionLocal()
        try:
            chain = session.execute(select(Chain).where(Chain.id == chain_id)).scalar_one()
            eth = Ethereum(chain)
            latest_block = eth.web3.eth.block_number
            decimals = Decimal(10 ** (eth.token_decimals()))
            while chain.last_checked_block < latest_block:
                from_block = chain.last_checked_block + 1
                to_block = min(from_block + 100, latest_block)
                logging.info(f"Scanning blocks {from_block} ~ {to_block} ({chain.name})")
                events = eth.get_transfer_events(from_block, to_block)
                for evt in events:
                    from_ = evt.args["from"]
                    to = evt.args["to"]
                    value = Decimal(evt.args["value"]) / decimals
                    logging.info(f"Found new token transfer: {value} token {from_} -> {to} ({chain.name})")
                    tx = Transaction(
                        from_address=from_, to_address=to, value=value, hash=evt.transactionHash.hex(), chain=chain
                    )
                    session.add(tx)
                chain.last_checked_block = to_block
                session.commit()
            session.close()
        except KeyboardInterrupt:
            session.close()
            return
        except:
            session.close()
            traceback.print_exc()


if __name__ == "__main__":
    session: Session = SessionLocal()
    tasks: dict[int, Future] = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        while True:
            for k, task in list(tasks.items()):
                if task.done():
                    del tasks[k]
            chains_ids = session.execute(select(Chain.id)).scalars().all()
            session.flush()
            for chain_id in chains_ids:
                if chain_id not in tasks:
                    tasks[chain_id] = executor.submit(monitor_chain, chain_id)
            time.sleep(10)
