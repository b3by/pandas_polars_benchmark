import polars as pl

from src.utils import timeit


@timeit
def load(file_path):
    return pl.read_csv(file_path)


@timeit
def get_shape(dataframe):
    dataframe.shape


@timeit
def describe(dataframe):
    dataframe.describe()


@timeit
def get_unique_values(dataframe):
    dataframe.lazy().select([
        pl.col('*').unique().count()
    ]).collect()


@timeit
def value_count(dataframe):
    for c in dataframe.columns:
        dataframe.lazy().select([
            pl.col(c).value_counts()
        ]).collect()


@timeit
def check_isnull(dataframe):
    dataframe.null_count()


@timeit
def sort_by_int_column(dataframe):
    dataframe.sort(by='price')


@timeit
def sort_by_column_union(dataframe):
    dataframe.sort(by=['price', 'brand'])


@timeit
def sort_datetime_column(dataframe):
    dataframe.lazy().select([
        pl.col('event_time').str.strptime(pl.Datetime, fmt='%F %X UTC').sort()
    ]).collect()


@timeit
def logical_select(dataframe):
    dataframe.filter(pl.col('price') > 100)


@timeit
def groupby_price_stats(dataframe):
    dataframe.lazy().groupby('brand').agg([
        pl.col('price').min().alias('price_min'),
        pl.col('price').max().alias('price_max'),
        pl.col('price').mean().alias('price_avg'),
        pl.col('price').std().alias('price_std')
    ]).collect()


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
