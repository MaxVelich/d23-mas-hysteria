library(readr)
library(list)

# Set up dataframes
setwd("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results")
load("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/results_control.csv")
results_control <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/results_control.csv")
results_rooms <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/results_rooms.csv")
results_supermarket <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/results_supermarket.csv")

# clean up dataframes
results_control_clean <- subset(results_control, results_control$'Time steps' != 10000)
results_rooms_clean <- subset(results_rooms, results_rooms$'Time steps' != 10000)
results_supermarket_clean <- subset(results_supermarket, results_supermarket$'Time steps' != 10000)

# shorten names for efficiency
rcc <- results_control_clean
rrc <- results_rooms_clean
rsc <- results_supermarket_clean

current <- 0
count <- 0
x <- 0
mean_control <- list()
for (row in 1:nrow(rcc)){
  if(rcc[row,]$theory_of_mind == current){
    x <- x + rcc[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_control <- c(mean_control, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}
  
current <- 0
count <- 0
x <- 0
mean_rooms <- list()
for (row in 1:nrow(rrc)){
  if(rrc[row,]$theory_of_mind == current){
    x <- x + rrc[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_rooms <- c(mean_rooms, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}

current <- 0
count <- 0
x <- 0
mean_supermarket <- list()
for (row in 1:nrow(rsc)){
  if(rsc[row,]$theory_of_mind == current){
    x <- x + rsc[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_supermarket <- c(mean_supermarket, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}

# very ugly way to make plots
tom_agents <- 1:20
time<-mean_control
plot(tom_agents,time)

time <-mean_rooms
plot(tom_agents,time)

time<-mean_supermarket
tom_agents <- 1:39
plot(tom_agents,time)
 