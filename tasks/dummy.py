import pandas as pd
import time

from src.utils import timeit


@timeit
def load(file_path):
    time.sleep(0.3)


@timeit
def get_shape(dataframe):
    time.sleep(0.3)


@timeit
def describe(dataframe):
    time.sleep(0.3)


@timeit
def get_unique_values(dataframe):
    time.sleep(0.3)


@timeit
def value_count(dataframe):
    time.sleep(0.3)


@timeit
def check_isnull(dataframe):
    time.sleep(0.3)


@timeit
def sort_by_int_column(dataframe):
    time.sleep(0.3)


@timeit
def sort_by_column_union(dataframe):
    time.sleep(0.3)


@timeit
def sort_datetime_column(dataframe):
    time.sleep(0.3)


@timeit
def logical_select(dataframe):
    time.sleep(0.3)


@timeit
def groupby_price_stats(dataframe):
    time.sleep(0.3)


benchmarks = [
    load,
    get_shape,
    describe,
    get_unique_values,
    value_count,
    check_isnull,
    sort_by_int_column,
    sort_by_column_union,
    sort_datetime_column,
    logical_select,
    groupby_price_stats
]

tasks = {idx: fn for idx, fn in enumerate(benchmarks)}
