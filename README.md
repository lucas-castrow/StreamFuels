# Cisia

Cisia is a collection of implementations designed to assist researchers with newly developed papers, both from our own team and other outstanding scientific papers.

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

df, frequency, horizon, contain_missing_values, contain_equal_length  = loader.read_tsf(path_tsf=result)

