import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:new_password@localhost:5432/banking_practice")
print("Connected successfully");