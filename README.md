
# MAS Hysteria

This is a simulation in order to analyze how agents behave in case of a panic in a building-like environment. Each agent has a plan in order to leave the building. This plan is calculated using A* over the discretized space in the environment. If agents come close to one another, their panic level increase and they start to act less 'rational'. They will follow the nearby agents by adapting to their average direction. On the other hand, some other agents implement a weak form of Theory of Mind. This results in the agents to see what the goal of the nearby agents is, and to follow a different goal, since that might mean that the exit everyone else is going for will be blocked. This results in a group-following behaviour -- form the sides of the panicked agents; and a group-avoiding behaviour -- from the sides of the Theory of Mind agents. 

The environment consists of obstacles (black, e.g. walls), exits (green) and a hazard (dark red, with a danger radius around it -- agents avoid it). Agents are blue circles when they are initialized; the change color depending on their panic level. Theory of Mind agents have a purple extra circle around them; they appear bigger.

Agents cannot collide with one another, they have to stop if their next step is occupied. However, they can replan the route if they deem it neccessary. For that reason, the simulation is not smooth, as replanning can take a second or two. You can adjust the frames per second with the included slider. 

## How to run?

In order to run the program, first install all requirements by running the following command in a fresh new Python 3.7.3 environment:

```
pip install -r requirements.txt
```

To start a normal (single) simulation, first select the configuration you want in `server.py` (the empty room one is the default) and then run
```
mesa runserver
```

If you want to run experiments, you can call the script for that by using
```
python experiment_run.py
```

If you are running Windows, you might run into an issue which can be resolved by uncommenting the first few lines in `server.py`.

## Code Structure

The root level consists of mainly four files: 
- `run.py` which launches the server
- `server.py` which configures the setting and spins up the `Model_Controller`
- `model.py` which implements the `Model_Controller`
- `experiment_run.py` which handles the batches and records the results for multiple runs (without visuals)

In the `src` folder one can find two subfolder: `model` and `view`.
- `view` includes all necessary files to display the simulation. One can find the `Canvas_Controller` here that handles the proper setup, as well as the `Portrayals.py` that describe how each entitiy looks like. Also, there is a HTML version of the legends together with a Java Script file `visualization.js` to handle the layout of the website.
- `model` includes all the logic and entities of our model. Here you can find all entities: `Exit`, `Hazard`, `Obstacle` and `Person`, especially the latter one does some heavy lifting. In the `logic` folder we bury all necessary logic and we separate it into the five classes `A_star`, `Panic_Dynamic`, `Path_Finder`, `Theory_Of_Mind` and `World_Manager`. These classes each handle separate parts of the model; they are fairly self-explanatory. Laslty, we have three helper files in the `utils` folder with a bunch of static functions that are commonly used throughout the code base.

## Authors

We are Prajakta Shouche, Kenneth Muller and Maximilian Velich. This is a project as part of the *Design of Multi-Agent Systems* course, in which we are group D23.