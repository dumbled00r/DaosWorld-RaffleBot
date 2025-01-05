from decimal import Decimal

import numpy as np
import pandas as pd


def raffle_for_burners(snapshot_file="DWL_Burners_snapshot.csv", num_winners=100):
    """
    Conducts a raffle for token burners based on the snapshot file.

    Args:
        snapshot_file (str): Path to the DWL_Burners_snapshot.csv file.
        num_winners (int): Number of winners to select from the raffle pool.

    Returns:
        csv file with the winners.
    """
    df = pd.read_csv(snapshot_file)
    df["total_burned"] = df["total_burned"].astype(str).apply(Decimal)
    df["total_burned_dwl"] = df["total_burned"] / Decimal(1e18)

    # get guaranteed winners list // burners with at least 1 DWL
    guaranteed_winners = df[df["total_burned_dwl"] >= 1]["sender_address"].tolist()

    # get non-guaranteed list
    raffle_pool = df[df["total_burned_dwl"] < 1]

    raffle_winners = []
    for _, row in raffle_pool.iterrows():
        if np.random.random() <= float(row["total_burned_dwl"]):
            raffle_winners.append(row["sender_address"])

    final_winners = list(set(guaranteed_winners + raffle_winners))

    remaining_pool = set(df["sender_address"]) - set(final_winners)
    while len(final_winners) < num_winners and remaining_pool:
        final_winners.append(remaining_pool.pop())

    final_winners = final_winners[:num_winners]
    final_winners_df = pd.DataFrame(
        {
            "sender_address": final_winners,
            "total_burned_dwl": [
                df.loc[df["sender_address"] == addr, "total_burned_dwl"].values[0]
                for addr in final_winners
            ],
            "win_type": [
                "guaranteed" if addr in guaranteed_winners else "raffle"
                for addr in final_winners
            ],
        }
    )

    output_file = "winners.csv"
    final_winners_df.to_csv(output_file, index=False)
    print(f"Raffle completed. Winners saved to {output_file}.")
    return output_file


if __name__ == "__main__":
    raffle_for_burners(num_winners=100)
