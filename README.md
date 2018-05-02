## Privacy Metrics

This program outputs a csv file with information about each transaction
in the Zcash blockchain.

The columns are as follows:

* blockHeight - The height of the block containing the transaction
* blockTime - The time the block was mined
* txId - The ID of the transaction
* isCoinBase - 'T' if the transaction is a coinbase transaction
* numVIn - The number of vin for the transaction
* totalVIn - The sum of the values referenced by the vins
* numVOut - The number of vout for the transaction
* totalVOut - The sum of the values of the vouts
* numJS - The number of joinsplits for the transaction
* totalJSIn - The sum of the shielded input amount
* totalJSOut - The sum of the shielded output amounts
* isSpendingCoinBase - 'T' if the vins reference a coinbase transaction

# Requirements

pip install python-bitcoinrpc

# Usage

Start a Zcash daemon and the execute the following command

python privacymetrics.py (BLOCKFROM) (BLOCKTO)

# Examples

python privacymetrics.py 0 100

    loading blocks 0-100...

    ..........+00:00:00
    ..........+00:00:00
    ..........+00:00:00
    ..........+00:00:00
    ..........+00:00:00
    ..........+00:00:00
    ..........+00:00:00
    ..........+00:00:00
    ..........+00:00:00
    ..........+00:00:00
    .
    101 transactions written to /home/user/zcash_stats/stats0-100.csv in 00:00:00


python privacymetrics.py 316000

    loading blocks 316000-316343...

    ...........+00:07:29
    ...........+00:02:02
    ............+00:01:54
    ...........+00:03:26
    ...........+00:03:07
    ............+00:07:47
    ...........+00:05:23
    ...........+00:02:35
    ............+00:04:01
    ...........+00:08:13
    .
    4448 transactions written to /home/user/zcash_stats/stats316000-316343.csv in 00:47:13

python privacymetrics.py

    loading blocks 0-316332...

    ..........+00:17:42
    ..........+00:16:47
    ..........+00:17:04
    ..........+00:24:47
    ..........+00:24:39
    ..........+00:25:29

...

# Notes

The program will print to the console based on it's progress though
the blockchain. It will print the time elapsed for each ~1/10th of 
the requested range of blocks. When the program has finished processing
it will print the number of transactions processed, the location of the
output file, and the total time elapsed.

