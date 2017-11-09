import click
import csv


@click.command()
@click.argument("input_file", type=click.File())
@click.argument("output_file", type=click.File("w"))
def main(input_file, output_file):
    writer = csv.writer(output_file)
    reader = csv.reader(input_file)
    header = reader.__next__()
    writer.writerow(header)
    current_id = 0
    current_txid = 0
    current_source = 0
    current_timestamp = 0
    current_target = 0
    current_value = 0
    for line in reader:
        txid, timestamp, source, target, value = line
        value = int(float(value))
        if source == current_source and target == current_target:
            current_id += 1
            current_value += value
        else:
            if current_id > 1:
                txid_string = "{} transactions".format(current_id)
            else:
                txid_string = current_txid
            if current_id:
                writer.writerow([
                    txid_string,
                    current_timestamp,
                    current_source,
                    current_target,
                    current_value
                ])
            current_id = 1
            current_txid = txid
            current_timestamp = timestamp
            current_source = source
            current_target = target
            current_value = value



if __name__ == "__main__":
    main()
