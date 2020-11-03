library(readr)
library(list)

# Set up dataframes
setwd("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/csv files")

#empty room
results_emptyroom_nopanic <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/csv files/emptyroom_nopanic.csv")
results_emptyroom_panic <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/csv files/emptyroom_panic.csv")
results_emptyroom_panic_nohazard <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/csv files/emptyroom_panic_nohazard.csv")

#two rooms
results_tworooms_nopanic <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/csv files/tworooms_nopanic.csv")
results_tworooms_panic <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/csv files/tworooms_panic.csv")
results_tworooms_panic_nohazard <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/csv files/tworooms_panic_nohazard.csv")

#supermarket
results_supermarket_nopanic <- read_csv("D:/uni/DMAS/d23-mas-hysteria/ Experiment_results/csv files/supermarket_nopanic.csv")


# clean up dataframes
emptyroom_nopanic <- subset(results_emptyroom_nopanic, results_emptyroom_nopanic$'Time steps' < 120)
emptyroom_panic <- subset(results_emptyroom_panic, results_emptyroom_panic$'Time steps' < 120)
emptyroom_panic_nohazard <- subset(results_emptyroom_panic_nohazard, results_emptyroom_panic_nohazard$'Time steps' < 120)

tworooms_nopanic <- subset(results_tworooms_nopanic, results_tworooms_nopanic$'Time steps' < 120)
tworooms_panic <- subset(results_tworooms_panic, results_tworooms_panic$'Time steps' < 120)
tworooms_panic_nohazard <- subset(results_tworooms_panic_nohazard, results_tworooms_panic_nohazard$'Time steps' < 120)

supermarket_nopanic <- subset(results_supermarket_nopanic, results_supermarket_nopanic$'Time steps' < 120)
#supermarket_panic <- subset(results_supermarket_panic, results_supermarket_panic$'Time steps' < 120)
#supermarket_panic_nohazard <- subset(results_supermarket_panic_nohazard, results_supermarket_panic_nohazard$'Time steps' < 120)


#abbreviate dataframes to make code shorter/more readable
enp <- emptyroom_nopanic
ep <- emptyroom_panic
epnh <- emptyroom_panic_nohazard

tnp <- tworooms_nopanic
tp <- tworooms_panic
tpnh <- tworooms_panic_nohazard

snp <- supermarket_nopanic
#sp <- supermarket_panic
#spnh <- supermarket_panic_nohazard


# collect mean timesteps for #of tom_agents in simulation

#emptyroom_nopanic
current <- 0
count <- 0
x <- 0
mean_empty_np <- list()
for (row in 1:nrow(enp)){
  if(enp[row,]$batch_tom == current){
    x <- x + enp[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_empty_np <- c(mean_empty_np, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}
mean <- x / count
mean_empty_np <- c(mean_empty_np, mean)
current <- current + 1
count <- 0
x <- 0


#emptyroom_panic
current <- 0
count <- 0
x <- 0
mean_empty_p <- list()
for (row in 1:nrow(ep)){
  if(ep[row,]$batch_tom == current){
    x <- x + ep[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_empty_p <- c(mean_empty_p, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}
mean <- x / count
mean_empty_p <- c(mean_empty_p, mean)
current <- current + 1
count <- 0
x <- 0


#emptyroom_panic_nohazard
current <- 0
count <- 0
x <- 0
mean_empty_pnh <- list()
for (row in 1:nrow(epnh)){
  if(epnh[row,]$batch_tom == current){
    x <- x + epnh[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_empty_pnh <- c(mean_empty_pnh, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}
mean <- x / count
mean_empty_pnh <- c(mean_empty_pnh, mean)
current <- current + 1
count <- 0
x <- 0


#tworooms_nopanic
current <- 0
count <- 0
x <- 0
mean_rooms_np <- list()
for (row in 1:nrow(tnp)){
  if(tnp[row,]$batch_tom == current){
    x <- x + tnp[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_rooms_np <- c(mean_rooms_np, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}
mean <- x / count
mean_rooms_np <- c(mean_rooms_np, mean)
current <- current + 1
count <- 0
x <- 0


#tworooms_panic
current <- 0
count <- 0
x <- 0
mean_rooms_p <- list()
for (row in 1:nrow(tp)){
  if(tp[row,]$batch_tom == current){
    x <- x + tp[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_rooms_p <- c(mean_rooms_p, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}
mean <- x / count
mean_rooms_p <- c(mean_rooms_p, mean)
current <- current + 1
count <- 0
x <- 0


#tworooms_panic_nohazard
current <- 0
count <- 0
x <- 0
mean_rooms_pnh <- list()
for (row in 1:nrow(tpnh)){
  if(tpnh[row,]$batch_tom == current){
    x <- x + tpnh[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_rooms_pnh <- c(mean_rooms_pnh, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}
mean <- x / count
mean_rooms_pnh <- c(mean_rooms_pnh, mean)
current <- current + 1
count <- 0
x <- 0


#supermarket_nopanic
current <- 0
count <- 0
x <- 0
mean_supermarket_np <- list()
for (row in 1:nrow(snp)){
  if(snp[row,]$batch_tom == current){
    x <- x + snp[row,]$'Time steps'
    count <- count + 1
  } else {
    mean <- x / count
    mean_supermarket_np <- c(mean_supermarket_np, mean)
    current <- current + 1
    count <- 0
    x <- 0
  }
}
mean <- x / count
mean_supermarket_np <- c(mean_supermarket_np, mean)
current <- current + 1
count <- 0
x <- 0


#supermarket_panic
# current <- 0
# count <- 0
# x <- 0
# mean_supermarket_p <- list()
# for (row in 1:nrow(sp)){
#   if(sp[row,]$batch_tom == current){
#     x <- x + sp[row,]$'Time steps'
#     count <- count + 1
#   } else {
#     mean <- x / count
#     mean_supermarket_p <- c(mean_supermarket_p, mean)
#     current <- current + 1
#     count <- 0
#     x <- 0
#   }
# }
# mean <- x / count
# mean_supermarket_p <- c(mean_supermarket_p, mean)
# current <- current + 1
# count <- 0
# x <- 0


#supermarket_panic_nohazard
# current <- 0
# count <- 0
# x <- 0
# mean_supermarket_pnh <- list()
# for (row in 1:nrow(spnh)){
#   if(spnh[row,]$batch_tom == current){
#     x <- x + spnh[row,]$'Time steps'
#     count <- count + 1
#   } else {
#     mean <- x / count
#     mean_supermarket_pnh <- c(mean_supermarket_pnh, mean)
#     current <- current + 1
#     count <- 0
#     x <- 0
#   }
# }
# mean <- x / count
# mean_supermarket_pnh <- c(mean_supermarket_pnh, mean)
# current <- current + 1
# count <- 0
# x <- 0

# very ugly way to make plots


tom_agents <- 0:20
time<-mean_empty_np
plot(tom_agents,time)
title("emptyroom_nopanic")

time<-mean_empty_p
plot(tom_agents,time)
title("emptyroom_panic")

time<-mean_empty_pnh
plot(tom_agents,time)
title("emptyroom_panic_nohazard")

time <-mean_rooms_np
plot(tom_agents,time)
title("tworooms_nopanic")

time <-mean_rooms_p
plot(tom_agents,time)
title("tworooms_panic")

time <-mean_rooms_pnh
plot(tom_agents,time)
title("tworooms_panic_nohazard")

time<-mean_supermarket_np
tom_agents <- 0:60
plot(tom_agents,time)
title("supermarket_nopanic")

# time<-mean_supermarket_p
# plot(tom_agents,time)
# title("supermarket_panic")
# 
# time<-mean_supermarket_pnh
# plot(tom_agents,time)
# title("supermarket_panic_nohazard")