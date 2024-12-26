from decimal import Decimal

import numpy as np
import pandas as pd


def raffle(
    ar_file="AR.csv", alch_file="ALCH.csv", aistr_file="AISTR.csv", num_winners=100
):

    ar_df = pd.read_csv(ar_file)
    alch_df = pd.read_csv(alch_file)
    aistr_df = pd.read_csv(aistr_file)

    merged_df = ar_df.merge(
        alch_df, on="address", how="outer", suffixes=("_AR", "_ALCH")
    )
    # preprocess
    merged_df = merged_df.merge(aistr_df, on="address", how="outer")
    merged_df = merged_df.fillna(0)

    merged_df["holding_balance_AR"] = (
        merged_df["holding_balance_AR"].astype(str).apply(Decimal)
    )
    merged_df["holding_balance_ALCH"] = (
        merged_df["holding_balance_ALCH"].astype(str).apply(Decimal)
    )
    merged_df["holding_balance"] = (
        merged_df["holding_balance"].astype(str).apply(Decimal)
    )

    # total token holdings
    merged_df["total_holdings"] = (
        merged_df["holding_balance_AR"]
        + merged_df["holding_balance_ALCH"]
        + merged_df["holding_balance"]
    )

    weights = merged_df["total_holdings"]

    # normalize weights
    weights = weights / weights.sum()

    winners_index = np.random.choice(
        merged_df.index, size=num_winners, replace=False, p=weights
    )
    winning_addresses = merged_df.loc[winners_index, "address"].tolist()

    winners_df = merged_df[merged_df["address"].isin(winning_addresses)]
    winners_df.drop(
        [
            "holding_balance_AR",
            "holding_balance_ALCH",
            "holding_balance",
            "rk_AR",
            "rk_ALCH",
            "rk",
        ],
        axis=1,
        inplace=True,
    )
    return winners_df.to_csv("winners.csv", index=False)


raffle()
