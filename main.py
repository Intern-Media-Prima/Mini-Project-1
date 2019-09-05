import pandas as pd
import numpy

data = pd.read_excel('data.xlsx')[11:3706]
data.columns = ['A','B','C','D','E','F','G','H','I','J','K']
data = data.drop(columns=['A','F','G','H','I'])
data = data.reset_index(drop=True)

print(data)

# # stacked = data.melt(id_vars=['B'])
# # print(stacked.head())

# with open('data.csv','w') as file:
# 	file.write(data.to_csv())

# print(data)

# for line in range(len(data)):
# 	if data['B'][line] == pd.isnan:
# 		print(line)

# making dataframe 
# df = pd.read_csv("https://cdncontribute.geeksforgeeks.org/wp-content/uploads/nba.csv") 
  
# it was print the first 5-rows 
# print(df.head()) 

# df_stacked = df.stack()
# print(df_stacked.head())