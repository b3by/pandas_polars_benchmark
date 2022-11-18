from pathlib import Path

import pandas as pd

from rich.console import Console
from rich.progress import Progress

import src.utils as utils


console = Console()


def call(args):
    data_dir = Path(args['data'])
    result_file = Path(args['results'])

    datasets = sorted(list(Path(data_dir).glob('*.csv')))

    task_modules = utils.get_task_modules(args['task'])
    no_tasks = len(list(task_modules.values())[0])

    console.print('Running benchmarks...')

    with Progress(console=console, transient=True) as progress:
        ds_prog = progress.add_task('[green]Datasets...', total=len(datasets))
        ts_prog = progress.add_task('Tasks...', total=no_tasks)
        md_prog = progress.add_task('Modules...',
                                    total=len(task_modules.keys()))

        for dataset in datasets:
            progress.update(ds_prog, description=utils.in_space(
                f'DATA: {dataset.name}'), sdvance=1)

            for task_id in range(no_tasks):
                task_name = task_modules[args['task'][0]][task_id].__name__

                progress.update(ts_prog, description=utils.in_space(
                    f'TASK: {task_name}'), advance=1)
                module_times = {}

                for module_name in task_modules.keys():
                    load_fn = task_modules[module_name][0]

                    progress.update(md_prog, description=utils.in_space(
                        f'MOD : {module_name}'), advance=1)

                    task_data, load_time = load_fn(dataset)

                    if task_id != 0:
                        task_function = task_modules[module_name][task_id]
                        _, task_time = task_function(task_data)
                    else:
                        task_time = load_time

                    module_times[module_name] = task_time

                res = {
                    'task': task_name,
                    'dataset': dataset.name}
                res.update(module_times)

                utils.dump_results(res, result_file)
                progress.reset(md_prog)

            progress.reset(ts_prog)
