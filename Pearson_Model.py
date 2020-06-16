import pandas as pd

print("Reading Data")
ratings = pd.read_csv("proc_data.csv", index_col=0)
print("Replacing Nans")
ratings = ratings.fillna(0)
ratings.head()

print("Computing correlation")
item_similarity_df = ratings.corr(method="pearson")

item_similarity_df.to_csv('pearson_model.csv', index=False, header=True)
