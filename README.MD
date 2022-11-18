## Run benchmarks for `pandas` and `polars`
This small script allows you to compare the execution times of a number of
tasks written with `polars` and `pandas`, and store them for later comparison.

## The dataset
The original dataset that was used for this benchmark comes from
[here](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store). In
order to generate the data for this benchmark, you should:

- download both files, `2019-Oct.csv` and `2019-Nov.csv`
- concatenate them
- save as many partitions of the concatenated dataset as you like

For example, the datasets included in the presentations were produced with the
following code:

```python
import pandas as pd

df = pd.concat([pd.read_csv('2019-Oct.csv'), pd.read_csv('2019-Nov.csv')])

partitions = [
          1_000,
         10_000,
        100_000,
      1_000_000,
     10_000_000,
    100_000_000
]

for idx, partition in enumerate(partitions):
    df[:partition].to_csv(f'{idx}_{str(partition)}.csv')
```

Please keep in mind, this thing will squat on you RAM for a while, so in case
you don't have enough resources, you can limit the size of the partitions.

## How to
I suggest you create a virtual environment and install the requirements
specified in the `requirements.txt` file.

To start the benchmark, you can use the `run.py` script. It takes the following
arguments:

```
Usage: run.py [OPTIONS]

Options:
  -d, --data DIRECTORY  Data folder  [required]
  -r, --results FILE    Result destination folder  [required]
  -t, --task TEXT       Task script that should be included (multiple opt.)
  --help                Show this message and exit.
```

- `--data` is where the data should be placed. Data files are fetched in
  alphabetical order, and benchmarks are executed using that order.
- `--results` is the results file.
- `--task` is a multiple option for the tasks that should be included in the
  benchmark (to include `pandas` and `polars`, write `-t pandas -t
  polars`). Tasks are executed in the order they are provided.
  
To run the benchmark, with data in the `./data` folder and results stored in
the `results.csv` file, use this:

```
$ python run.py --data ./data --results results.csv --task pandas --task polars
```

The results provided in this repository were obtained on a system with the
following specs:

```
OS: Ubuntu 18.04.5 LTS x86_64
Kernel: 4.15.0-194-generic
Shell: zsh 5.4.2
CPU: AMD Ryzen 7 1700X (16) @ 3.400GHz
Memory: 3024MiB / 64413MiB
```

### Task conventions
Tasks are stored in the `./tasks` folder. Each file in this folder can be
interpreted as a module to add to the benchmark. Something to note about task
modules:

- Every task module should expose a `tasks` dictionary that contains the
  indices of the benchmark functions and the corresponding functions.
- The list of functions to call should be the same across all modules, with the
  same ids as well. A module with out-of-sync tasks will terminate the program.
  
The `./tasks/dummy.py` module provides a simple example of this.

You can use the same structure to add more modules or packages to the
benchmark.
