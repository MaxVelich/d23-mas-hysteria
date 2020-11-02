
from src.model.entities.Person import Person

import matplotlib.pyplot as plt
import time

class Data_Collector_Helper():

    def get_collectors(self):

        collectors = {
            "Active": lambda m: self.count_active_agents(m, False),
            # "Escaped": lambda m: self.count_active_agents(m, True),
            "Low Panic": lambda m: self.count_panic(m, 0),
            "Medium Panic": lambda m: self.count_panic(m, 1),
            "High Panic": lambda m: self.count_panic(m, 2),
            "ToM0": lambda m: self.count_tom(m, 0),
            "ToM1": lambda m: self.count_tom(m, 1)
        }

        return collectors

    def save_figures(self, results, num_agents):
        print("we're plotting")

        dpi = 100
        fig, axes = plt.subplots(figsize=(1920 / dpi, 1080 / dpi), dpi=dpi, nrows=1, ncols=3)

        status_results = results.loc[:, ['Active']]
        status_plot = status_results.plot(ax=axes[0])
        status_plot.set_xlim(xmin=0)
        status_plot.set_ylim(ymin=0)
        status_plot.set_title("# of agents still in building")
        status_plot.set_xlabel("Simulation Step")
        status_plot.set_ylabel("Count")

        panic_results = results.loc[:, ['Low Panic', 'Medium Panic', 'High Panic']]
        panic_plot = panic_results.plot(ax=axes[1])
        panic_plot.set_xlim(xmin=0)
        panic_plot.set_ylim(ymin=0)
        panic_plot.set_title("Panic levels")
        panic_plot.set_xlabel("Simulation Step")
        panic_plot.set_ylabel("Count")

        tom_results = results.loc[:, ['ToM0', 'ToM1']]
        tom_plot = tom_results.plot(ax=axes[2])
        tom_plot.set_xlim(xmin=0)
        tom_plot.set_ylim(ymin=0)
        tom_plot.set_title("ToM levels")
        tom_plot.set_xlabel("Simulation Step")
        tom_plot.set_ylabel("Count")

        timestr = time.strftime("%Y%m%d-%H%M%S")
        plt.suptitle("Number of Agents: " + str(num_agents), fontsize=16)
        plt.savefig(timestr + ".png")
        plt.cla()
        plt.close(fig)

    @staticmethod
    def count_active_agents(model, status):
        """
        Count how many agents are still active in the model
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Person):
                if agent.escaped == status:
                    count += 1
        return count

    @staticmethod
    def count_panic(model, panic):
        """
        Count how many agents have a particular panic level
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Person):
                if agent.panic == panic:
                    count += 1
        return count

    @staticmethod
    def count_tom(model, tom=1):
        """
        Count how many agents have a particular level of Theory of Mind
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Person):
                if agent.theory_of_mind == tom:
                    count += 1
        return count

    @staticmethod
    def get_time(model):
        return model.time

    @staticmethod
    def get_tom_times(model):
        return model.tom_times

    @staticmethod
    def get_regular_times(model):
        return model.regular_times
