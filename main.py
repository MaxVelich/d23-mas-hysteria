from src.model import MoneyModel
from src.model import compute_gini

import matplotlib.pyplot as plt
import numpy as np

from mesa.batchrunner import BatchRunner


def main():

    fixed_params = {"width": 10,
                    "height": 10}
    variable_params = {"N": range(10, 500, 10)}

    batch_run = BatchRunner(MoneyModel,
                            variable_params,
                            fixed_params,
                            iterations=5,
                            max_steps=100,
                            model_reporters={"Gini": compute_gini})
    batch_run.run_all()

    # agent_counts = np.zeros((model.grid.width, model.grid.height))
    # for cell in model.grid.coord_iter():
    #     cell_content, x, y = cell
    #     agent_count = len(cell_content)
    #     agent_counts[x][y] = agent_count
    # plt.imshow(agent_counts, interpolation='nearest')
    # plt.colorbar()
    # plt.show()


if __name__ == "__main__":
    main()
