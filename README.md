# Cisia

Cisia is a collection of implementations designed to assist researchers with newly developed papers, both from our own team and other outstanding scientific papers.

sales_monthly_state(): monthly fuel sales data by state from the ANP database
    
sales_yearly_state(): yearly fuel sales data by state from ANP database

sales_yearly_city(): yearly fuel sales data by city from ANP database

oil_gas_operations_monthly_state(): monthly oil production, LGN production, natural gas production, reinjection, flaring and losses, self-consumption, and available natural gas. It provides a comprehensive view of petroleum and gas operations.
  


<!-- ## Installation

```bash
pip install cisia
``` -->


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
```

### Yearly sales of petroleum derivatives in the states of Brazil.
![image](https://github.com/user-attachments/assets/ab1d0ac8-9574-4229-81e6-2e3ef32e959c)

### Monthly sales of petroleum derivatives in the states of Brazil.
![image](https://github.com/user-attachments/assets/4894d0cf-eb92-421b-8b8a-d0a1522ccc0d)

### Monthly oil and gas operations in the states of Brazil.
![image](https://github.com/user-attachments/assets/ab9b18b5-54ee-41f8-8948-9458b6e96343)

### Yearly sales of petroleum derivatives in the cities of Brazil.

![image](https://github.com/user-attachments/assets/26ac0d96-73f9-43a8-b9bf-47106cafeba4)



