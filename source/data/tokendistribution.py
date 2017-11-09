import click
import requests
import csv
import time
import json
import logging
import logging.config


from log_config import log_config


logger = logging.getLogger(__name__)


@click.command()
@click.option("-v", "--verbose", count=True)
@click.argument("nodes", type=click.File("w"))
@click.argument("links", type=click.File("w"))
def main(verbose, nodes, links):
    current_node = 0
    min_transaction_size = 10000
    min_transaction_timestamp = 1509742213
    logging.config.dictConfig(log_config(verbose))
    node_writer = csv.writer(nodes)
    node_writer.writerow([
        "address",
        "balance"
        ])
    link_writer = csv.writer(links)
    link_writer.writerow([
        "id",
        "timestamp",
        "source",
        "target",
        "value",
    ])
    known_nodes = set()
    new_nodes = set(["3MbYQMMmSkC3AgWkj9FMo5LsPTW1zBTwXL"])
    # new_nodes = set(["1KYiKJEfdJtap9QX2v9BXJMpz2SfU4pgZw"])
    while new_nodes:
        logger.debug("found %s new nodes", len(new_nodes))
        node = new_nodes.pop()
        url = "http://omniexplorer.info/ask.aspx"
        params = {
            "api": "gethistory",
            "address": node,
        }
        logger.debug("requesting %s", params)
        response = requests.get(url, params=params).json()
        logger.debug("got response %s", response)
        transactions = response["transactions"]
        params = {
            "api": "getbalance",
            "prop": 31,
            "address": node,
        }
        time.sleep(1)
        balance = requests.get(url, params=params).json()
        logger.debug("got response %s", response)
        node_writer.writerow([node, balance])
        known_nodes.update([node])
        logger.debug("found %s transactions", len(transactions))
        for transaction in transactions:
            time.sleep(0.2)
            params = {
                "api": "gettx",
                "txid": transaction
            }
            response = requests.get(url, params=params)
            try:
                logger.debug("transaction %s", response.text)
                t = json.loads("{" + response.text + "}")
            except JSONDecodeError:
                continue
            # keep only last two batches of 25 + 20 MUSDT
            try:
                blocktime = t["blocktime"]
                if blocktime < min_transaction_timestamp:
                    break
                txid = t["txid"]
                source = t["sendingaddress"]
                target = t["referenceaddress"]
                amount = float(t["amount"])
            except KeyError:
                continue
            if source != node or amount < min_transaction_size:
                continue
            link_writer.writerow([
                txid, blocktime, source, target, amount
            ])
            if target not in known_nodes:
                new_nodes.update([target])
        time.sleep(1)
        logger.debug("new nodes: %s", new_nodes)
        current_node += 1
        logger.debug("analized %s nodes", current_node)


if __name__ == "__main__":
    main()
