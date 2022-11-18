import time
import functools
import sys

from typing import Callable
from typing import Sequence
from types import ModuleType

from pathlib import Path
from importlib import util

import pandas as pd


TASK_DIR = Path('./tasks')


def timeit(f: Callable) -> Callable:
    """Timing decorator for benchmark functions

    Use it to measure the exectution time of a function. In order to preserve
    the returned value of the wrapped call, the wrapper returns a tuple where
    the first element is the result of wrapped function, and the second element
    is the execution time expressed in seconds.

    Arguments
    ---------
    f : Callable
        The function to wrap in the returned callable function.

    Returns
    -------
    Callable
        The wrapped target function.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        end = time.perf_counter()

        return result, end - start

    return wrapper


def get_task_modules(task_names: Sequence, task_dir: Path = TASK_DIR) -> dict:
    """Fetch all the available task modules

    The task modules can be loaded in form of a dictionary where keys are the
    name of the benchmark modules, and values are dictionaries of task ids and
    corresponding functions. So, if my benchmark contains 2 modules with 3
    functions each, the returned dictionary will look like this:
    
    ```
    {
        'mod1': { 0: <function>, 1: <function>, 2: <function> },
        'mod2': { 0: <function>, 1: <function>, 2: <function> }
    }
    ```

    Arguments
    ---------
    task_names : Sequence
        A list or a tuple of the modules to add in the benchmark.
    task_dir : Path
        The folder where tasks should be included. Defaulted to a ./task folder
        in the project root.

    Returns
    -------
    dict
        A dictionary where keys are the module names, and values are nested
        dictionaries with task_id / task_function pairs.
    """
    return {x: load_task_module(Path(task_dir, f'{x}.py')).tasks
            for x in task_names}


def load_task_module(task_path: Path) -> ModuleType:
    """Load task modules

    A task file is loaded as a module, then returned.
    
    Arguments
    ---------
    task_path : Path
        The path of the task file to load.

    Returns
    -------
    ModuleType
        A module containing the benchmark functions and the list of tasks.
    """
    m_name = f'tasks.{task_path.stem}'
    spec = util.spec_from_file_location(m_name, task_path)
    task_module = util.module_from_spec(spec)

    sys.modules[m_name] = task_module
    spec.loader.exec_module(task_module)

    return task_module


def in_space(s: str, m: int = 20) -> str:
    """Take the effort to print pretty

    Make sure the passed string is not longer than m characters.

    Arguments
    ---------
    s : str
        The string to compress in m characters.
    m : str
        The maximum length allowed for string s.

    Returns
    -------
    str
        The compressed string.
    """
    return s[:m - 3] + '...' if len(s) > m else s + ' ' * (m + 1 - len(s))


def dump_results(results: dict, f: Path):
    """Append a result entry to a file

    Take a dictionary of results, convert it in pandas format, then append it
    to a specified file. If the file already exists, the append will skip the
    header.

    Arguments
    ---------
    results : dict
        A dictionary of results. Each key will become a column.
    """
    r = pd.json_normalize(results, sep='_')
    opts = {'index': None}

    if Path(f).exists():
        opts['mode'] = 'a'
        opts['header'] = False

    r.to_csv(f, **opts)
