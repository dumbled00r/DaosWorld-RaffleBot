import csv

import pandas as pd
from dune_client.client import DuneClient
from dune_client.models import (
    CreateTableResult,
    DeleteTableResult,
    DuneError,
    ExecutionResponse,
    ExecutionState,
    ExecutionStatusResponse,
    InsertTableResult,
)
from dune_client.query import QueryBase
from dune_client.types import QueryParameter

DUNE_API_KEY = "DUNE_API_KEY_HERE"

dune = DuneClient(api_key=DUNE_API_KEY)

QUERY_ID = 4481695  # my query

dict_ca = {
    "AR": "0x3e43cB385A6925986e7ea0f0dcdAEc06673d4e10",
    "AiSTR": "0x20ef84969f6d81Ff74AE4591c331858b20AD82CD",
    "ALCH": "0x2b0772BEa2757624287ffc7feB92D03aeAE6F12D",
}

lp_address = {
    "AiSTR": "0x197ecb5c176aD4f6e77894913a94c5145416f148",
    "AR": "0x3fdD9A4b3CA4a99e3dfE931e3973C2aC37B45BE9",
    "ALCH": "0xF5677B22454dEe978b2Eb908d6a17923F5658a79",
}


def getHolders(token_name, ca):
    """RUN THIS FUNCTION TO EXPORT HOLDERS TO CSV"""
    try:
        query = QueryBase(
            name="testquery",
            query_id=QUERY_ID,
            params=[
                QueryParameter.text_type(
                    name="chain",
                    value="base",
                ),
                QueryParameter.text_type(
                    name="Contract",
                    value=ca,
                ),
            ],
        )
        job_id = dune.execute_query(query).execution_id
        # status = dune.get_execution_status(job_id)
        # # get the result

        results = dune.get_execution_results(job_id)
        while results.state != ExecutionState.COMPLETED:
            results = dune.get_execution_results(job_id)

        # print(result)
        df = pd.DataFrame(results.result.rows)
        lstToHold = ["address", "holding_balance", "rk"]
        lstDrop = list(set(df.columns) - set(lstToHold))
        df.drop(lstDrop, axis=1, inplace=True)
        # remove the LP address row from the dataframe
        df = df[~df["address"].str.contains(lp_address[token_name])]

        df.to_csv(f"{token_name}.csv", index=False)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    for token, contract_address in dict_ca.items():
        getHolders(token, contract_address)
        print(f"Exported {token} holders to {token}.csv")

    # remove
