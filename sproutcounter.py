#!/usr/bin/env python2
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import *
import sys

if len(sys.argv) != 3:
    print "Usage: sproutcounter.py BLOCKFROM BLOCKTO"
    exit(1)

# have a local running instance of zcashd
api = AuthServiceProxy("http://username:password@127.0.0.1:8232")

count_joinsplits = 0
count_shielded_tx = 0
block_from = int(sys.argv[1])
block_to = int(sys.argv[2]) + 1  # +1 so inclusive
sum_vpub_old = Decimal(0)
sum_vpub_new = Decimal(0)

for i in xrange(block_from, block_to):
    blockhash = api.getblockhash(i)
    block = api.getblock(blockhash)
    for txid in block["tx"]:
        tx = api.getrawtransaction(txid,1)
        if len(tx["vjoinsplit"]) is 0:
            continue
        for js in tx["vjoinsplit"]:
            sum_vpub_old += js["vpub_old"]
            sum_vpub_new += js["vpub_new"]

n = sum_vpub_old - sum_vpub_new
print "aggregate value entering sprout circuit     = %.8f" % (sum_vpub_old)
print "aggregate value leaving sprout circuit      = %.8f" % (sum_vpub_new)
print "net shielded value change in sprout circuit = %.8f" % (n)

