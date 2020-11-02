import argparse
from pathlib import Path

from mesa.batchrunner import BatchRunner

from src.model.entities.Hazard import Hazard
from src.model.entities.Obstacle import Obstacle
from src.model.entities.Exit import Exit

from model import Model_Controller
from src.model.utils.Data_Collector_Helper import Data_Collector_Helper
from src.model.entities import Person


config_free_space = { "dimensions": (500, 500),
                      "num_agents": 20,
                      "theory_of_mind": 10,
                      "panic_dynamic": [3, 4],
                      "agent_boundaries": [175, 325, 175, 325],
                      "obstacles": [],
                      "exits": [Exit(0, 25), Exit(0, 475), Exit(500, 25), Exit(500, 475)],
                      "hazard": Hazard(50, 100)
                    }


def record_time(times, agents):
    if agents > 0:
        return times/agents
    else:
        return 0


def parse_arguments():
    parser = argparse.ArgumentParser(description='Fire evacuation model ')
    # parser.add_argument('--n_agents', type=int, default=50,
    #                    help='Maximum number of agents')
    parser.add_argument('--tom_agents', type=int, default=21, help='Maximum number of ToM agents')
    args = parser.parse_args()
    return args.tom_agents


if __name__ == '__main__':
    current_configuration = config_free_space
    width, height = current_configuration["dimensions"]

    fixed_params = {
        "configuration": current_configuration,
        "save_plots": False,
        "batch_run": True,
        "batch_panic": [0, 0],
        "width": width,
        "height": height,
        "N": current_configuration["num_agents"]
    }
    variable_params = {
        "batch_tom": range(0, parse_arguments(), 1)
    }

    batch_run = BatchRunner(Model_Controller,
                            variable_params,
                            fixed_params,
                            iterations=10,
                            max_steps=300,
                            model_reporters={"Time steps": lambda m: Data_Collector_Helper.get_time(m),
                                             "ToM times": lambda m: Data_Collector_Helper.get_tom_times(m),
                                             "ToM average": lambda m: record_time(sum(Data_Collector_Helper.get_tom_times(m)),len(Data_Collector_Helper.get_tom_times(m))),
                                             "Regular times": lambda m: Data_Collector_Helper.get_regular_times(m),
                                             "Regular average": lambda m: record_time(sum(Data_Collector_Helper.get_regular_times(m)),len(Data_Collector_Helper.get_regular_times(m)))
                                             }

                            )
    batch_run.run_all()

    batch_dir = Path.cwd() / " Experiment_results"
    if not batch_dir.exists():
        Path.mkdir(batch_dir)
    run_data = batch_run.get_model_vars_dataframe()
    run_data.to_csv(path_or_buf=(batch_dir / "results.csv"))
