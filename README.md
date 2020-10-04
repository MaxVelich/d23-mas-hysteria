
# MAS Hysteria

This is the beta version of our project. The implementation is not done at this point. When you run the program, you can see a square environment with 10 agents (blue dots) -- imagine a top down view of a room. The black bars are obstacles, or walls. The green square represents an exit. When you start the simulation, the agents will try to find their way to the exit. Currently, there is no collision detection to the agents will overlap. Also, the implementation of the path finding is not optimized yet, so it runs very sluggish -- we will fix that later.

The agents change color depending on their panic level. The dynamic behind this mechanism is also still in beta. One can see the levels in the legend.

## How to run?

In order to run the program, first install all requirements by running the following command in a fresh new Python 3.7.3 environment:

```
pip install -r requirements.txt
```

Then, run:

```
python main.py
```

## Authors

We are Prajakta Shouche, Kenneth Muller and Maximilian Velich. This is a project as part of the *Design of Multi-Agent Systems* course, in which we are group D23.