import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

from dataReady import df_for_bundles


def top_products_by_quantity(_df: pd.DataFrame):
    """
    To produce best 10 products by Quantity
    """
    _df = _df.groupby(["ProductName"], as_index=False)["Quantity"].sum()
    _df = _df.sort_values(by=["Quantity"], ascending=False).head(10)
    return _df["ProductName"].unique()


def best_city_sales(_df: pd.DataFrame, groupbylist):
    """
    To produce a dataframe used to visualize
    Best Countries for sales by totalPriceSold
    """
    _df = _df.groupby(groupbylist, as_index=False)[["Quantity", "totalPriceSold"]]
    _df = _df.sum().query("Quantity > 0").sort_values("totalPriceSold", ascending=False)
    return _df


def top_product_by_revenue(_df: pd.DataFrame):
    """
    To produce a dataframe used to visualize
    Best Products for sales by Quantity
    """
    _df = _df.groupby(["ProductName"], as_index=False)["totalPriceSold"].sum()
    _df = _df.sort_values(by=["totalPriceSold"], ascending=False).head(10)
    return _df["ProductName"].unique()


def best_transactions_sold_price(_df: pd.DataFrame, groupbylist):
    """
    To produce a dataframe user to visualize
    Best transactions by totalPriceSold
    """
    _df = _df.groupby(groupbylist, as_index=False)[["totalPriceSold"]].sum()
    _df.sort_values(by=["totalPriceSold"], ascending=False)


def region_dataframe(_df: pd.DataFrame):
    """
    To produce a dataframe to study regions by:
        > Total price sold
        > Mean price sold
        > Number of transactions
        > Mean of quantity
    """
    byregion = (
        _df.groupby(["Region"], as_index=False)
        .agg(
            tot_amount=("totalPriceSold", "sum"),
            mean_amount=("totalPriceSold", "mean"),
            n_Transactions=("TransactionNo", "nunique"),
            mean_Quantity=("Quantity", "mean"),
        )
        .sort_values("mean_amount", ascending=False)
    )
    byregion["tot_amount"] = round(byregion["tot_amount"], 2)
    byregion["mean_amount"] = round(byregion["mean_amount"], 2)
    byregion["mean_Quantity"] = round(byregion["mean_Quantity"], 2)
    byregion.sort_values("mean_amount", ascending=False)
    return byregion


def items_bundles(filtered_transactions):
    """
    To produce a dataFrame for Bundled items
    """
    transactions = df_for_bundles.filter(items=filtered_transactions[:2],axis=0).to_list()

    encoder = TransactionEncoder().fit(transactions)
    onehot = encoder.transform(transactions)
    onehot = pd.DataFrame(onehot, columns=encoder.columns_)
    frequent_itemsets = apriori(onehot, min_support=0.05, max_len=3, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
    rules["antecedents"] = rules["antecedents"].apply(lambda x: ",".join(list(x)))
    rules["consequents"] = rules["consequents"].apply(lambda x: ",".join(list(x)))
    rules["support"] = round(rules["support"], 2)
    rules["confidence"] = round(rules["confidence"], 2)
    rules["lift"] = round(rules["lift"], 2)
    rules["n_antecedents"] = rules["antecedents"].apply(lambda x: len(x))
    rules["n_consequents"] = rules["consequents"].apply(lambda x: len(x))
    return rules[
        [
            "antecedents",
            "consequents",
            "support",
            "confidence",
            "lift",
        ]
    ].head(10)
