# Script: python3 /Users/grantarbuckle/Desktop/Data\ Analytics/Python/Projects/Practice/current_month_discover_trans.py
import pandas as pd
from datetime import datetime

# Get current period
year = str(datetime.now().year)
month = str(datetime.now().month)
if len(year + "-" + month) == 6:
    cur_period = year + "-0" + month
else:
    cur_period = year + "-" + month
cur_period

df = pd.read_csv("/Users/grantarbuckle/Desktop/Data Analytics/Datasets/Discover Purchases.csv")
df["month_year"] = pd.to_datetime(df['Post Date']).dt.to_period('M').astype(str)

# Group by category, current month
curr_month_cat_filter = df[~df["Category"].isin(["Payments and Credits", "Awards and Rebate Credits"])]
curr_month_cat_filter = curr_month_cat_filter.rename(columns= {"Amount":"CUR_MONTH_AMT", "Category":"CATEGORY"})######
curr_month_cat_filter = curr_month_cat_filter[curr_month_cat_filter["month_year"].str.contains(cur_period)]
curr_month_cat_filter = curr_month_cat_filter.groupby(["CATEGORY", "month_year"]).sum().reset_index().sort_values("CUR_MONTH_AMT", ascending = False)
curr_month_cat_filter = curr_month_cat_filter.reset_index().drop(columns = ["month_year", "index"])
print(curr_month_cat_filter, '\n')

# Group by description, current month
curr_month_descr_filter = df[~df["Category"].isin(["Payments and Credits", "Awards and Rebate Credits"])]
curr_month_descr_filter = curr_month_descr_filter.rename(columns= {"Amount":"CUR_MONTH_AMT", "Description":"DESCRIPTION"})######
curr_month_descr_filter = curr_month_descr_filter[curr_month_descr_filter["month_year"].str.contains(cur_period)]
curr_month_descr_filter["DESCRIPTION"] = curr_month_descr_filter["DESCRIPTION"].str[:10] # Only keep first 10 characters of desc
curr_month_descr_filter = curr_month_descr_filter.groupby(["DESCRIPTION", "month_year"]).sum().reset_index().sort_values("CUR_MONTH_AMT", ascending = False)
curr_month_descr_filter = curr_month_descr_filter.reset_index().drop(columns = ["month_year", "index"])
print(curr_month_descr_filter.head(20), '\n')

# Get current month total
cur_mo_total = df[~df["Category"].isin(["Payments and Credits", "Awards and Rebate Credits"])]
cur_mo_total = cur_mo_total[cur_mo_total["month_year"].str.contains(cur_period)]
cur_mo_total = cur_mo_total.drop(columns = ["month_year", "Trans. Date", "Post Date", "Description", "Category"])
cur_mo_total = cur_mo_total.rename(columns= {"Amount":"CUR_MONTH_TOTAL"})######
cur_mo_total = cur_mo_total.sum()
print(cur_mo_total, '\n')