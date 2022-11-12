import argparse

parser = argparse.ArgumentParser(description='Display graph of cumulative distance cycled over time')
parser.add_argument('start_date', type=str,
                    help='Start date')
parser.add_argument('end_date', type=str,
                    help='End date')

args = parser.parse_args()
print(f'Starting on {args.start_date}, end on {args.end_date}')
