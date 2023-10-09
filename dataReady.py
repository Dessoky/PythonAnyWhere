import pandas as pd
import numpy as np

df = pd.read_csv("Data\\Grinta_CaseDataset.csv")
df.dropna(subset=["CustomerNo"], axis=0, inplace=True)
df.drop_duplicates(inplace=True)
df = df.query("Quantity > 0")
df["totalPriceSold"] = round(df["Price"] * df["Quantity"], 3)
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
df["Year"] = df["Date"].dt.year
df["dayName"] = df["Date"].dt.day_name()
df["month"] = df["Date"].dt.month
months = [
    "December",
    "November",
    "October",
    "September",
    "August",
    "July",
    "June",
    "May",
    "April",
    "March",
    "February",
    "January",
]
months.reverse()
# df["monthName"] = pd.Categorical(
#     df["Date"].dt.month_name(),
#     categories=months,
#     ordered=True,
# )
df["monthName"] = df["Date"].dt.month_name()
df["CustomerNo"] = df["CustomerNo"].astype(int)
Regions = {
    "Europe": [
        "Sweden",
        "Denmark",
        "Norway",
        "Finland",
        "Iceland",
        "Netherlands",
        "Belgium",
        "France",
        "Germany",
        "Switzerland",
        "Austria",
        "Italy",
        "Spain",
        "Greece",
        "Portugal",
        "Malta",
        "Cyprus",
        "Czech Republic",
        "Lithuania",
        "Poland",
        "United Kingdom",
        "EIRE",
        "Channel Islands",
        "European Community",
    ],
    "North America": ["USA", "Canada"],
    "Middle East": [
        "Bahrain",
        "United Arab Emirates",
        "Israel",
        "Lebanon",
        "Saudi Arabia",
    ],
    "Asia Pacific": ["Japan", "Australia", "Singapore", "Hong Kong"],
    "RoW": ["Brazil", "RSA"],
    "Unspecified": ["Unspecified"],
}
country_to_region = {}
for region, countries in Regions.items():
    for country in countries:
        country_to_region[country] = region
df["Region"] = df["Country"].map(country_to_region)
df["UKvsRoW"] = np.where(df["Country"] == "United Kingdom", "UK", "RoW")

df_grouped = df.groupby(
    ["Year", "monthName", "Region", "Country", "ProductName"], as_index=False
).agg(
    totalPriceSold=("totalPriceSold", "sum"),
    meanPriceSold=("totalPriceSold", "mean"),
    n_Transactions=("TransactionNo", "nunique"),
    Quantity=("Quantity", "sum"),
    mean_Quantity=("Quantity", "mean"),
)

df_for_bundles = (
    df.groupby(["TransactionNo"])
    .apply(lambda x: list(x["ProductName"]))
)
# df_for_bundles.columns = [
#     "Year",
#     "Region",
#     "Country",
#     "TransactionNo",
#     "ProductName",
# ]


def customer_rank_classifier(total_amount):
    """
    Used to classify Customers
    """
    total_amount = int(total_amount)
    if total_amount <= 5000:
        return "BRONZE"
    if total_amount <= 20000:
        return "SILVER"
    if total_amount <= 100000:
        return "GOLD"
    if total_amount <= 250000:
        return "PLATINUM"
    if total_amount <= 500000:
        return "DIAMOND"
    return "VIP"


customer_segments_df = (
    df.copy()
    .groupby(["CustomerNo"], as_index=False)
    .agg(
        totalPriceSold=("totalPriceSold", "sum"),
        totalQuantity=("Quantity", "sum"),
        totalTransactions=("TransactionNo", "nunique"),
        uniqueProducts=("ProductNo", "nunique"),
    )
)
customer_segments_df["Rank"] = customer_segments_df["totalPriceSold"].apply(
    customer_rank_classifier
)
