"""Run benchmarks

This script works as an entry point for the benchmark. From the command line
interface, you can specify:

- the folder where the data sit
- the folder where the results will be saved
- the tasks that should be included in the benchmark

"""
import click

from src.benchmark import call


@click.command()
@click.option('--data', '-d',
              type=click.Path(file_okay=False, readable=True, exists=True),
              required=True,
              help='Data folder')
@click.option('--results', '-r',
              type=click.Path(
                  dir_okay=False, readable=True, writable=True), required=True,
              help='Result destination folder')
@click.option('--task', '-t', multiple=True, default=['pandas', 'polars'],
              help='Task script that should be included (multiple opt.)')
def run_benchmark(**args):
    call(args)


if __name__ == '__main__':
    run_benchmark()
