# CSC 46000 Project: Air Quality in NYC
By: Daniel Aguilar-Rodriguez, Anvinh Truong, Jia Cong Lin

Project Proposal:\
[Click Here](https://github.com/daniel-a-r/ccny_data_science_project/blob/main/Project%20Proposal.pdf)

# Motivation

For our group, what we are trying to solve and predict is the air quality in New York City
based on the traffic levels. It’s important to take into consideration the air quality and what we
breathe in, especially in a dense place like New York City. There will be times when the air
quality will be unhealthy to breathe in and there will also be times when it is fine, so it would be
helpful to predict future air quality based on the traffic volumes and determine whether or not the
air quality would be safe to inhale on any given day

# Blog Post & Presentation 
[Blog Post](https://github.com/daniel-a-r/ccny_data_science_project/blob/main/Blog%20Air%20Quality%20in%20NYC.pdf)

# Data

For the datasets, we have one on Air Quality and another on Traffic Volume, with the Air
Quality data being sourced from the EPA, and Traffic Volume from NYC OpenData. The Air
Quality dataset contains the type of sample in the air, how it's measured, neighborhood, time
frame, and start date, which are all relevant in having a more precise measurement in a particular
area in New York City. The Traffic Volume dataset contains the boroughs for where the total
traffic is measured within 15 minute increments, the streets from the start to end at where the
traffic is located, and date/time at when it took place. These two datasets would help us predict
air quality based on the amount of traffic there is, however there are some limitations to this in
which we are not taking the weather into account as that can have an impact on both air quality
and traffic.

# Data Dictionary

- boro: specific borough in nyc
- date: the date in which the datasets align
- vol: traffic volume
- arithmetic_mean: mean of data
- aqi: air quality index

# Future Work

For the future, more datasets could be incorporated that provide a lot more information in
terms of quantity over the years as we had one dataset that we removed due to insufficient
amount of data covered over a longer period of time. Different types of models could further be
explored and used as well to obtain higher accuracy scores and better prediction. We also
broadened the scope. We also used the 5 boroughs as locations, which is a very broad scope, so
for the future, it would be better to narrow it down into neighborhoods within each borough to
make the data more precise to a specific area instead of a borough.

