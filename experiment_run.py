import argparse
from pathlib import Path

from mesa.batchrunner import BatchRunner

from src.model.Model_Controller import Model_Controller


def parse_arguments():
    parser = argparse.ArgumentParser(description='Fire evacuation model ')
    parser.add_argument('--n_agents', type=int, default=50,
                        help='Maximum number of agents')
    args = parser.parse_args()
    return args.n_agents


if __name__ == '__main__':
    fixed_params = {
        "width": 500,
        "height": 500
    }
    variable_params = {
        "N": range(10, parse_arguments(), 10)
    }

    batch_run = BatchRunner(Model_Controller,
                            variable_params,
                            fixed_params,
                            iterations=5,
                            max_steps=10,
                            model_reporters={"Escaped Agents": Model_Controller.count_active_agents,
                                             "Time steps": Model_Controller.get_time}

                            )
    batch_run.run_all()

    batch_dir = Path.cwd() / " Experiment_results"
    if not batch_dir.exists():
        Path.mkdir(batch_dir)
    run_data = batch_run.get_model_vars_dataframe()
    run_data.to_csv(path_or_buf=(batch_dir / "results"))
