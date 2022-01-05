import pandas as pd
import numpy as np

a = np.array([1])
df = pd.DataFrame({"Maintanance_price": a})
df["Maintanance_price"] = df["Maintanance_price"].replace({"a":1})

print(df)
