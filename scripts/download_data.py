from ucimlrepo import fetch_ucirepo
import pandas as pd
from pathlib import Path

#output path:

output_path = Path("data/online_shoppers.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

# fetch dataset 
dataset = fetch_ucirepo(id=468) 


# data (as pandas dataframes) 
X = dataset.data.features 
y = dataset.data.targets 

df = pd.concat((X,y), axis=1)
df.to_csv(path_or_buf = output_path, index = False)

print(f"data file saved in {output_path}, shape : {df.shape}")