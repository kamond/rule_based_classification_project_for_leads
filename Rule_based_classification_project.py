# With Rule Based Classification
# Calculation of Lead Yield
#################################################
import pandas as pd

df = pd.read_csv("../datasets/persona.csv")

print(df)

# Task1
# Answer the following questions
#########

# Question1: Read persona.csv and show general information about the dataset

df = pd.read_csv("../datasets/persona.csv")


def check_df(dataframe, head=5, tail=5, quan=False):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(tail))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())

    if quan:
        print("##################### Quantiles #####################")
        print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


check_df(df, quan=True)

# Question 2: How many unique sources are there? What are their frequencies?

print(df["SOURCE"].nunique())

# sources = df["SOURCE"].unique()

print(pd.DataFrame({"SOURCE": df["SOURCE"].value_counts()}))

# Question 3: How many unique prices are there?

print(df["PRICE"].nunique())

# Question 4: How many sales were made from which price?

print(pd.DataFrame({"#Records": df["PRICE"].value_counts()}))

# Question 5: How many sales were made from which country?

print(pd.DataFrame({"#Records": df["COUNTRY"].value_counts()}))

# Question 6: How much was earned in total from sales by country?

print(df.groupby(["COUNTRY"])["PRICE"].sum())

# Question 7: What are the sales numbers by source types?

print(df.groupby(["SOURCE"])["PRICE"].count())

print(pd.DataFrame({"#Records": df["SOURCE"].value_counts()}))

# Question 8: : What are the PRICE averages by country?

print(df.groupby(["COUNTRY"])["PRICE"].mean())

# Question 9: What are the price averages according to sources?

print(df.groupby(["SOURCE"])["PRICE"].mean())

# Question 10: What are the PRICE averages in the COUNTRY-SOURCE breakdown?

print(df.groupby(["COUNTRY", "SOURCE"])["PRICE"].mean())


# Task 2
# In COUNTRY, SOURCE, SEX, AGE breakdown, what are average earnings?
#########

def target_summary_with_cat(dataframe, target, categorical_col):
    print(pd.DataFrame({"PRICE": dataframe.groupby(categorical_col)[target].mean()}), end="\n\n\n")


target_summary_with_cat(df, "PRICE", ["COUNTRY", "SOURCE", "SEX", "AGE"])


# Task 3
# Sort the output by PRICE.
#########


def target_summary_with_cat(dataframe, target, categorical_col):
    return pd.DataFrame({"PRICE": dataframe.groupby(categorical_col)[target].mean()})


agg_df = target_summary_with_cat(df, "PRICE", ["COUNTRY", "SOURCE", "SEX", "AGE"]).sort_values(by=["PRICE"],
                                                                                               ascending=False)

print(agg_df)

# Task 4
# Convert the names in the index to variable names.
#########

agg_df = agg_df.reset_index()

print(agg_df)

# Task 5
# Convert age variable to categorical variable and
# Add it to agg_df.
#########

agg_df["AGE"].max()
agg_df["AGE"].min()

age_intervals = ["0_18", "19_24", "25_30", "31_40", "41_70"]
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 24, 30, 40, 70], labels=age_intervals)

agg_df.dtypes

"""
2nd method:
agg_df["AGE_CAT"] = ""
for index, row in agg_df.iterrows():
    if row["AGE"] <= 18:
        agg_df.loc[index, "AGE_CAT"] = "0_18"
    elif 18 < row["AGE"] <= 24:
        agg_df.loc[index, "AGE_CAT"] = "19_24"
    elif 24 < row["AGE"] <= 30:
        agg_df.loc[index, "AGE_CAT"] = "25_30"
    elif 30 < row["AGE"] <= 40:
        agg_df.loc[index, "AGE_CAT"] = "31_40"
    else:
        agg_df.loc[index, "AGE_CAT"] = "41_70"
"""

# Task 6
# Identify new level-based customers (personas).
#########

agg_df["customers_level_based"] = agg_df[["COUNTRY", "SOURCE", "SEX", "AGE_CAT"]].apply(lambda x: '_'.join(x).upper(),
                                                                                        axis=1)

agg_df

agg_df.groupby(["customers_level_based"])["PRICE"].mean()

# Görev7
#########

agg_df['SEGMENT'] = pd.qcut(agg_df['PRICE'], 4, ['D', 'C', 'B', 'A'])

agg_df.groupby('SEGMENT').agg({'PRICE': ['max', 'mean', 'sum']})

agg_df[agg_df['SEGMENT'] == 'C'].describe().T

new_user = 'TUR_ANDROID_FEMALE_31_40'
new_user_1 = 'FRA_IOS_FEMALE_31_40'

def profit(new_user):
    s = agg_df[agg_df['customers_level_based'] == new_user]
    print("Profit: ", s['PRICE'].mean())
    return pd.DataFrame({"Profit": s.groupby('SEGMENT')['PRICE'].mean()})

profit(new_user)
profit(new_user_1)

#s.groupby('SEGMENT').agg({'PRICE': ['mean']})

