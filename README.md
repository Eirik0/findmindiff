## Find Min Diff

This program outputs a csv file with information about each transaction in the Zcash blockchain.

The columns are as follows:

* blockHeight - The height of the block containing the transaction
* blockTimeDelta - The time elsapsed between blocks
* difficulty - The difficulty of the block

Additionally, it will print a list of all blocks which have minimal difficulty over a given range.

# Requirements

pip install python-bitcoinrpc

# Usage

Start a Zcash daemon and the execute the following command

python findmindiff.py (BLOCKFROM) (BLOCKTO)

# Example

python findmindiff.py 290000

    loading blocks 290000-304932...

    .......... +00:00:03
    .......... +00:00:04
    .......... +00:00:03
    .......... +00:00:04
    .......... +00:00:03
    .......... +00:00:05
    .......... +00:00:03
    .......... +00:00:03
    .......... +00:00:03
    .......... +00:00:04

    14933 blocks written to /home/eirik/zcash_stats/stats_mindiff290000-304932.csv in 00:00:39

    Min diff = 1, Number of blocks = 180

    299188: diff=1, time=3351
    299189: diff=1, time=1104
    299202: diff=1, time=14581
    ... And so on ...

# Notes

There are two optional parameters BLOCKFROM and BLOCKTO. The default for
BLOCKFROM is 0 and the default for BLOCKTO is the current height of the
blockchain.
