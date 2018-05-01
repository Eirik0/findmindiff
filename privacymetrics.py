#!/usr/bin/env python2
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from os.path import expanduser
import sys, os

if len(sys.argv) != 3:
    print "Usage: privacymetrics.py BLOCKFROM BLOCKTO"
    exit(1)

# have a local running instance of zcashd
api = AuthServiceProxy("http://username:password@127.0.0.1:8232")

block_from = int(sys.argv[1])
block_to = int(sys.argv[2])

filePath = expanduser("~") + "/zcash_stats/"
fileName = "stats{}-{}.csv".format(block_from, block_to)
if not os.path.exists(filePath):
    os.makedirs(filePath)
statsFile = open(filePath + fileName, "w+")

statsFile.write("blockHeight,blockTime,txId,isCoinBase,numVIn,totalVIn,numVOut,totalVOut,numJS,totalJSIn,totalJSOut,isSpendingCoinBase,type\n")

totalBlocks = block_to - block_from + 1
onePercent = int(totalBlocks / 100)
tenPercent = int(totalBlocks / 10)
numBlocks = 1
numTxs = 0

for blockHeight in xrange(block_from, block_to + 1): # +1 so inclusive
    if (numBlocks % onePercent) == 0:
        sys.stdout.write(".")
        sys.stdout.flush()
    if (numBlocks % tenPercent) == 0:
        print ""

    block = api.getblock("{}".format(blockHeight), 2)
    blockTime = block["time"]
    for tx in block["tx"]:
        txid = tx["txid"]
        isCoinBase = len(tx["vin"]) == 1 and "coinbase" in tx["vin"][0]

        totalVIn = 0
        isSpendingCoinBase = False
        if not isCoinBase:
            for vin in tx["vin"]:
                prevHash = vin["txid"]
                prevN = vin["vout"]
                try:
                    prevTx = api.getrawtransaction(prevHash, 1)
                except JSONRPCException as e:
                    print "When loading prevout {}, txid {}: {}\n".format(prevHash, txid, e)
                    continue
                totalVIn += prevTx["vout"][prevN]["value"]
                isSpendingCoinBase |= len(prevTx["vin"]) == 1 and "coinbase" in prevTx["vin"][0]

        totalVOut = 0
        for vout in tx["vout"]:
            totalVOut += vout["value"]

        totalJSIn = 0
        totalJSOut = 0
        for js in tx["vjoinsplit"]:
            totalJSIn += js["vpub_new"]
            totalJSOut += js["vpub_old"]

        txType = "tz"
        if len(tx["vjoinsplit"]) == 0:
            txType = "tt"
        elif len(tx["vin"]) == 0 and len(tx["vout"]) == 0:
            txType = "tz"
        elif totalJSIn > 0:
            txType = "zt"

        formatVIn = "{0:f}".format(totalVIn)
        formatVOut = "{0:f}".format(totalVOut)
        formatJSIn = "{0:f}".format(totalJSIn)
        formatJSOut = "{0:f}".format(totalJSOut)

        statsFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                blockHeight,blockTime,txid,isCoinBase,
                len(tx["vin"]), formatVIn, len(tx["vout"]), formatVOut, 
                len(tx["vjoinsplit"]), formatJSIn, formatJSOut,
                isSpendingCoinBase, txType))

        numTxs += 1
    
    numBlocks += 1

statsFile.flush()
statsFile.close()

print "{} transactions written to {}".format(numTxs, filePath + fileName)