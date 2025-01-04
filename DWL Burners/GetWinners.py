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

    # convert from uint256 --> dec
    df["total_burned_dwl"] = df["total_burned"] / Decimal(1e18)

    # get guaranteed winners list // since the total amount of $DWL < 100 --> no randomiztion between those
    guaranteed_winners = df[df["total_burned_dwl"] == 1]["sender_address"].tolist()

    # get non-guaranteed winners list
    raffle_pool = df[df["total_burned_dwl"] != 1]

    weights = (
        raffle_pool["total_burned_dwl"] / raffle_pool["total_burned_dwl"].sum()
    )  # normalize chance to win

    raffle_winners_index = np.random.choice(  # raffle
        raffle_pool.index,
        size=min(num_winners, len(raffle_pool)),
        replace=False,
        p=weights,
    )
    raffle_winners = raffle_pool.loc[raffle_winners_index, "sender_address"].tolist()

    final_winners = pd.DataFrame(
        {
            "sender_address": guaranteed_winners + raffle_winners,
            "win_type": ["guaranteed"] * len(guaranteed_winners)
            + ["raffle"] * len(raffle_winners),
        }
    )

    output_file = "winners.csv"
    final_winners.to_csv(output_file, index=False)

    print(f"Raffle completed. {num_winners} winners saved to {output_file}.")
    return output_file


if __name__ == "__main__":
    raffle_for_burners(num_winners=100)
