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

config_two_rooms = { "dimensions": (500, 500),
                     "num_agents": 20,
                     "theory_of_mind": 5,
                     "panic_dynamic": [3, 4],
                     "agent_boundaries": [25, 475, 115, 475],
                     "obstacles": [ Obstacle((250,300), 20,400),
                                    Obstacle((75,90), 150,20),
                                    Obstacle((250,90), 75,20),
                                    Obstacle((425,90), 150,20) ],
                     "exits": [ Exit(0, 25), Exit(500, 25) ],
                     "hazard" : Hazard(30,30)
                   }

config_supermarket = { "dimensions": (1000, 500),
                       "num_agents": 60,
                       "theory_of_mind": 5,
                       "panic_dynamic": [3, 4],
                       "agent_boundaries": [25, 975, 25, 475],
                       "obstacles": [ Obstacle((125,20), 250,40),
                                      Obstacle((970,125), 60,250),
                                      Obstacle((175,470), 350,60),
                                      Obstacle((600,125), 400,50),
                                      Obstacle((600,250), 400,50),
                                      Obstacle((625,375), 350,50),
                                      Obstacle((150,250), 200,30) ],
                       "exits": [ Exit(0, 75), Exit(0, 425) ],
                       "hazard" : Hazard(550,200)
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
    parser.add_argument('--tom_agents', type=int, default=61, help='Maximum number of ToM agents')
    args = parser.parse_args()
    return args.tom_agents


if __name__ == '__main__':
    current_configuration = config_supermarket
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
                            iterations=5,
                            max_steps=200,
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
