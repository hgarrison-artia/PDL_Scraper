import pandas as pd

x = [1,2,3]
y = [4,5,6]

df = pd.DataFrame()
df['x'] = x
df['y'] = y

print(1 in df['x'])