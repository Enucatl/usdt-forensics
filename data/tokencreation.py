import click
import requests
import csv
import time
import json
from tqdm import tqdm


@click.command()
@click.argument("output", type=click.File("w"))
def main(output):
    address = "3MbYQMMmSkC3AgWkj9FMo5LsPTW1zBTwXL"
    url = "http://omniexplorer.info/ask.aspx"
    params = {
        "api": "gethistory",
        "address": address
    }
    response = requests.get(url, params=params).json()
    print(response)
    transactions = response["transactions"]
    writer = csv.writer(output)
    writer.writerow([
        "blocktime",
        "amount"
        ])
    for transaction in tqdm(transactions):
        time.sleep(1)
        params = {
            "api": "gettx",
            "txid": transaction
        }
        response = requests.get(url, params=params)
        t = json.loads("{" + response.text + "}")
        if t["type"] == "Grant Property Tokens":
            writer.writerow([t["blocktime"], t["amount"]])


if __name__ == "__main__":
    main()
