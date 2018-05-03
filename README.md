## Privacy Metrics

This program outputs a csv file with information about each transaction in the
Zcash blockchain.

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

python privacymetrics.py 0 1000

    loading blocks 0-1000...

    .......... +00:00:00 (100 txs, 0 errors)
    .......... +00:00:00 (100 txs, 0 errors)
    .......... +00:00:00 (100 txs, 0 errors)
    .......... +00:00:00 (102 txs, 0 errors)
    .......... +00:00:00 (145 txs, 0 errors)
    .......... +00:00:01 (355 txs, 0 errors)
    .......... +00:00:02 (421 txs, 0 errors)
    .......... +00:00:01 (304 txs, 0 errors)
    .......... +00:00:02 (491 txs, 0 errors)
    .......... +00:00:02 (638 txs, 0 errors)

    2758 transactions written to /home/eirik/zcash_stats/stats0-1000.csv in 00:00:13
    0 errors written to /home/eirik/zcash_stats/stats0-1000_errors.txt

python privacymetrics.py 316900

    loading blocks 316900-316928...

    .. +00:00:37 (55 txs, 0 errors)
    .. +00:00:20 (13 txs, 0 errors)
    .. +00:00:04 (22 txs, 0 errors)
    .. +00:03:24 (31 txs, 0 errors)
    .. +00:00:11 (48 txs, 0 errors)
    .. +00:00:01 (26 txs, 0 errors)
    .. +00:01:13 (22 txs, 0 errors)
    .. +00:00:02 (23 txs, 0 errors)
    .. +00:00:01 (13 txs, 0 errors)
    .. +00:00:10 (71 txs, 0 errors)
    .. +00:00:01 (9 txs, 0 errors)
    .. +00:01:19 (15 txs, 0 errors)
    .. +00:00:02 (33 txs, 0 errors)
    .. +00:00:11 (30 txs, 0 errors)

    418 transactions written to /home/eirik/zcash_stats/stats316900-316928.csv in 00:07:43
    0 errors written to /home/eirik/zcash_stats/stats316900-316928_errors.txt


python privacymetrics.py 

    loading blocks 0-316566...

    .......... +00:17:06 (183378 txs, 0 errors)
    .......... +00:16:46 (126591 txs, 0 errors)
    .......... +00:16:25 (155691 txs, 0 errors)
    .......... +00:23:04 (211800 txs, 0 errors)
    .......... +00:21:43 (262748 txs, 0 errors)
    .......... +00:24:44 (301184 txs, 0 errors)
    .......... +00:26:21 (344080 txs, 0 errors)
    .......... +00:51:59 (563301 txs, 2 errors)
    .......... +00:58:12 (472586 txs, 1 errors)
    .......... +01:34:22 (341515 txs, 2 errors)

    2962940 transactions written to /home/user/zcash_stats/stats0-316566.csv in 05:50:46
    5 errors written to /home/user/zcash_stats/stats0-316566_errors.txt

# Notes

There are two optional parameters BLOCKFROM and BLOCKTO. The default for
BLOCKFROM is 0 and the default for BLOCKTO is the current height of the
blockchain

The program will print to the console based on it's progress though the 
blockchain. It will print the time elapsed, the number of transactions
written, and the number of errors encountered for each ~1/10th of the
requested range of blocks. When the program has finished processing it 
will print the number of transactions processed, the location of the
output file, the total time elapsed, and a message regarding whether or
not there were any errors.

The program is designed to be able to recover from some errors. If there is
an error when making the a call for a raw transaction, the 'totalVIn' for that
transaction will not be correct. If there is an error when calling for a block. 
The program will open a new connection and try to make the call again. If 
there is only one error for a given block, assuming the program did not crash, 
then the program will have recovered and successfully loaded the block.