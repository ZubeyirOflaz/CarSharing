# Car Sharing
> Project to solve the multi travelling salesman problem using optimization research models

<p align="center">
<img src="https://img.shields.io/github/license/ZubeyirOflaz/Deep-Learning-Uncertainty-Quantification-Methods" alt="plot" width="75">
<img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="plot" width="85">

</p>

This project finds the most cost-efficient solution to a variant of multi traveling salesman problem where:
- There exist, multiple groups of people in different locations,
- There exists a number of rental cars available for transportation each of which has different costs of rent, capacity and fuel consumption
- All groups aim to arrive at the same location but return to their original destinations
- Groups have additional requirements regarding which transportation option they can take according to their needs

The python scripts retrieve and process the necessary input data and then relay it to the Minizinc optimization research (OR) model created for retrieving solutions. The master script is also used to compare the performance of OR solvers on this problem.

![](header.png)

## Features

- Easy to use and flexible model for finding optimal routes for most economical car-sharing solution


- Adapts to current fuel prices and available rental cars easily


- Automated distance matrix creation


- Use of excel for data to enable easy data input and testing


- Can be used with many solvers

- Still, ride-sharing is a multiple traveling salesman problem that requires an extremely high computational resource


## Usage
Groups file             |  AvailableCars file
:-------------------------:|:-------------------------:
![](docs\groups.png)  |  ![](docs\Cars.png)

The script uses two CSV files, namely Groups and AvailableCars, as the information source. The Groups file contains all the destinations as well as groups and their requirements. AvailableCars file contains all the rental cars and the relevant information about these rentals. The instances in these files are grouped into small, medium and large datasets in order to measure the solver performance with different size MTSP instances. The distance matrix is created for all the locations and the information in these CSV files are converted to be used in the Minizinc model. Then the master script runs the OR model and returns the result as well as the model's performance with the solver that is used.

