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

QUERY_ID = 4518440  # query id for getting burners https://dune.com/queries/4518440


block_number = 24586698  # modify this to snapshot at a specific block number
burn_address = "0xdead696969dead696969dead696969dead696969"
token_address = "0x956e1a6b5ff341e38c4e277a03e661a8801806f6"  # $DWL


def getBurners():
    """FUNCTION TO EXPORT BURNERS TO CSV"""
    try:

        query = QueryBase(
            name="getBurners",
            query_id=QUERY_ID,
            params=[
                QueryParameter.number_type(name="block_number", value=block_number),
                QueryParameter.text_type(
                    name="burn_address",
                    value=burn_address,
                ),
                QueryParameter.text_type(name="token_address", value=token_address),
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

        df.to_csv(f"DWL_Burners_snapshot.csv", index=False)

        print("Burners exported to csv")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    getBurners()
