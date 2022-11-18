import pandas as pd

from src.utils import timeit


@timeit
def load(file_path):
    return pd.read_csv(file_path)


@timeit
def get_shape(dataframe):
    dataframe.shape


@timeit
def describe(dataframe):
    dataframe.describe()


@timeit
def get_unique_values(dataframe):
    dataframe.apply(lambda col: len(col.unique()))


@timeit
def value_count(dataframe):
    for c in dataframe.columns:
        dataframe[c].value_counts()


@timeit
def check_isnull(dataframe):
    dataframe.isnull().sum()


@timeit
def sort_by_int_column(dataframe):
    dataframe.sort_values(by='price')


@timeit
def sort_by_column_union(dataframe):
    dataframe.sort_values(by=['price', 'brand'])


@timeit
def sort_datetime_column(dataframe):
    pd.to_datetime(dataframe.event_time).sort_values()


@timeit
def logical_select(dataframe):
    dataframe[dataframe['price'] > 100]


@timeit
def groupby_price_stats(dataframe):
    dataframe.groupby('brand')['price'].agg(['min', 'max', 'mean', 'std'])


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
