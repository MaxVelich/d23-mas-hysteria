import argparse
from pathlib import Path

from mesa.batchrunner import BatchRunner

from model import Model_Controller
from src.model.entities import Person


def record_time(times, agents):
    if agents > 0:
        return times/agents
    else:
        return 0


def parse_arguments():
    parser = argparse.ArgumentParser(description='Fire evacuation model ')
    parser.add_argument('--tom_agents', type=int, default=21)
    # parser.add_argument('--n_agents', type=int, default=50,
    #                    help='Maximum number of agents')
    args = parser.parse_args()
    return args.tom_agents


if __name__ == '__main__':
    fixed_params = {
        "N": 20,
        "width": 500,
        "height": 500,
        # "theory_of_mind": 5,
        "panic_dynamic": [2, 7],
        "save_plots": False
    }
    variable_params = {
        "theory_of_mind": range(0, parse_arguments(), 1)
    }

    batch_run = BatchRunner(Model_Controller,
                            variable_params,
                            fixed_params,
                            iterations=5,
                            max_steps=10000,
                            model_reporters={"Time steps": lambda m: Model_Controller.get_time(m),
                                             "ToM times": lambda m: Model_Controller.get_tom_times(m),
                                             "ToM average": lambda m: record_time(sum(Model_Controller.get_tom_times(m)),len(Model_Controller.get_tom_times(m))),
                                             "Regular times": lambda m: Model_Controller.get_regular_times(m),
                                             "Regular average": lambda m: record_time(sum(Model_Controller.get_regular_times(m)),len(Model_Controller.get_regular_times(m)))
                                             }
                            )
    batch_run.run_all()

    batch_dir = Path.cwd() / " Experiment_results"
    if not batch_dir.exists():
        Path.mkdir(batch_dir)
    run_data = batch_run.get_model_vars_dataframe()
    run_data.to_csv(path_or_buf=(batch_dir / "results.csv"))
