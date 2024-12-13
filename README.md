# Cisia

Cisia is a collection of implementations designed to assist researchers with newly developed papers, both from our own team and other outstanding scientific papers.

sales_monthly_state(): monthly fuel sales data by state from the ANP database
    
sales_yearly_state(): yearly fuel sales data by state from ANP database

sales_yearly_city(): yearly fuel sales data by city from ANP database


## Installation

```bash
pip install cisia
```


To run locally, in your target python environment and in this project folder type:
```bash
pip install -e .
```


After that you can import using the target python environment:

```python
from cisia.datasets import DatasetLoader
loader = DatasetLoader()
result, flag = loader.sales_yearly_state()

df, metadata = loader.read_tsf(path_tsf=result)

