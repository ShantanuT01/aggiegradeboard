# Texas A&M Grade Distribution/AEFIS Results dashboard repository

Shantanu Thorat

## About

This app shows grade distribution data and AEFIS course evaluations for professors. This repository contains the source code for the published app hosted on Streamlit. 

All data is obtained from publicly available datasets. 

To view the complete dataset see [the Kaggle dataset](https://www.kaggle.com/datasets/sst001/texas-a-and-m-university-grades-and-aefis-dataset?datasetId=3633358).

## Running

Clone the GitHub repository, and navigate to the directory on the command line. Set up Python 3.10 using Anaconda. Make a brand new virtual environment:
``` shell
conda create --name myenv python=3.10
conda activate myenv
pip install -r requirements.txt
```
Additionally, make a `.env` file and add your Kaggle API credentials - see the [Kaggle docs](https://www.kaggle.com/docs/api).

To run the app:
```
streamlit run app.py
```
