## Find Min Diff

This program will examine the blockchain and output a list of all blocks which
have minimal difficulty over a given range.

# Requirements

pip install python-bitcoinrpc

# Usage

Start a Zcash daemon and the execute the following command

python findmindiff.py (BLOCKFROM) (BLOCKTO)

# Example

python findmindiff.py 0 1000

    loading blocks 290000-303587...

    .......... +00:00:07
    .......... +00:00:08
    .......... +00:00:07
    .......... +00:00:08
    .......... +00:00:07
    .......... +00:00:09
    .......... +00:00:07
    .......... +00:00:07
    .......... +00:00:07
    .......... +00:00:07

    Finished in 00:01:18
    Min diff = 1
    299188: diff=1, time=3351
    299189: diff=1, time=1104
    299202: diff=1, time=14581
    ... And so on ...

# Notes

There are two optional parameters BLOCKFROM and BLOCKTO. The default for
BLOCKFROM is 0 and the default for BLOCKTO is the current height of the
blockchain
