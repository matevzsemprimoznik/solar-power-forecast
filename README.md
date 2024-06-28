# Solar Power Forecast

This project focuses on predicting the energy production of the E.W. Brown Solar Facility using machine learning techniques. The E.W. Brown Solar Facility located in US Kentucky is a large-scale solar power plant, and accurate predictions of its energy output are crucial for efficient grid management and energy planning.

Key features:

 - Data Acquisition: Gather historical energy production data and relevant meteorological data from reliable sources.
 - Data Processing: Clean, preprocess, and integrate the data to prepare it for modeling.
 - Model Training: Develop and train machine learning models using processed data to predict daily energy production.
 - Results Validation: Validate model predictions using appropriate metrics to ensure accuracy and reliability.
 - Web Application for Results Display: Create a web application to visualize and display prediction results in an accessible format.
 - Model Management via Web Application: Implement features in the web application for managing and updating the prediction model.


Project structure:

```
├── README.md <- File containing project description and setup instructions
├── data
    ├── processed <- Processed data, prepared for training
    └── raw <- Raw downloaded data
├── reports <- Generated analysis files from data testing and validation
├── gx <- Configuration files for great expectations
├── pyproject.toml <- File defining dependencies, library versions, etc.
├── src <- Source code of the project
  ├── apps <- Application code
      ├── api <- Forecast API
      ├── client <- Forecast dashboard
      ├── model management api <- Model management API
      └── model management client <- Model management dashboard
  ├── config <- Configuration files
  ├── data <- Scripts for data downloading, processing, etc.
  ├── models <- Scripts for training predictive models and using models for prediction
  ├── serve <- Scripts for serving models as web services
  └── validation <- Scripts for data validation
```

## Getting started

Setup:

- Python 3.12
- Poetry 1.8.2
- Docker 20.10.21
- Node.js 20.10.0
- npm 10.5.0

Steps:

1. Clone the repository
2. Install dependencies using Poetry
```bash
poetry install
```
3. Install Node.js dependencies inside the `src/apps/client` and `src/apps/model_management_client` directories
```bash
cd src/apps/client
npm install
```
```bash
cd src/apps/model_management_client
npm install
```
4. Run the application through scripts in pyproject.toml

