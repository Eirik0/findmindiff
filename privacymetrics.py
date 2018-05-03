#!/usr/bin/env python2
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from os.path import expanduser
import os, sys, time
# The following import is from authproxy,py
try:
    import http.client as httplib
except ImportError:
    import httplib

class CachedTx:
    def __init__(self, tx):
        self.isCoinBase = len(tx["vin"]) == 1 and "coinbase" in tx["vin"][0]
        self.values = []

if len(sys.argv) > 3:
    print "Usage: privacymetrics.py (BLOCKFROM) (BLOCKTO)"
    exit(1)

# have a local running instance of zcashd
api = AuthServiceProxy("http://username:password@127.0.0.1:8232")

chainHeight = api.getblockcount()
block_from = int(sys.argv[1]) if len(sys.argv) > 1 else 0
block_to = int(sys.argv[2]) if len(sys.argv) > 2 else chainHeight
block_from = min(max(0, block_from), chainHeight)
block_to = min(max(block_to, block_from), chainHeight)

filePath = expanduser("~") + "/zcash_stats/"
if not os.path.exists(filePath):
    os.makedirs(filePath)

statsFileName = "stats{}-{}.csv".format(block_from, block_to)
statsFile = open(filePath + statsFileName, "w+")

errorFileName = "stats{}-{}_errors.txt".format(block_from, block_to)
errorFile = open(filePath + errorFileName, "w+")

print "\nloading blocks {}-{}...\n".format(block_from, block_to)

totalBlocks = block_to - block_from + 1
onePercent = max(int(round(totalBlocks / 100)), 1)
tenPercent = max(int(round(totalBlocks / 10)), 1)
numBlocks = 0
numTxs = 0
numErrors = 0

cachedTxs = dict()

start_time = time.time()
last_update_time = start_time
lastNumErrors = 0
lastNumTxs = 0

statsFile.write("blockHeight,blockTime,txId,isCoinBase,numVIn,totalVIn,numVOut,totalVOut,numJS,totalJSIn,totalJSOut,isSpendingCoinBase\n")

for blockHeight in xrange(block_from, block_to + 1): # +1 so inclusive
    if numBlocks > 0 and numBlocks % onePercent == 0:
        sys.stdout.write(".")
        sys.stdout.flush()
    if numBlocks > 0 and numBlocks % tenPercent == 0:
        current_time = time.time()
        elapsed = int(current_time - last_update_time)
        print " +{:02d}:{:02d}:{:02d} ({} txs, {} errors)".format(elapsed // 3600, (elapsed % 3600 // 60), elapsed % 60, numTxs - lastNumTxs, numErrors - lastNumErrors)
        last_update_time = current_time
        lastNumTxs = numTxs
        lastNumErrors = numErrors

    block = None
    for attempt in xrange(1, 3): # 2 tries
        try:
            block = api.getblock("{}".format(blockHeight), 2)
            break
        except Exception as e:
            numErrors += 1
            errorFile.write("Error when loading block {} - {}: {}\n".format(blockHeight, type(e), e.message))
            # Create a new proxy as we may not be able to send more requests without a new connection
            api = AuthServiceProxy("http://username:password@127.0.0.1:8232")

    if block is None:
        errorFile.write("Skipping block {}\n".format(blockHeight))
        continue   

    blockTime = block["time"]
    for tx in block["tx"]:
        txid = tx["txid"]
        
        cachedTx = CachedTx(tx)
        cachedTxs[txid] = cachedTx

        totalVIn = 0
        isSpendingCoinBase = False

        if not cachedTx.isCoinBase:
            for vin in tx["vin"]:
                prevHash = vin["txid"]
                prevN = vin["vout"]
                if cachedTxs.has_key(prevHash):
                    prevTx = cachedTxs[prevHash]
                    totalVIn += prevTx.values[prevN]
                    isSpendingCoinBase |= prevTx.isCoinBase
                else:
                    try:
                        prevTx = api.getrawtransaction(prevHash, 1)
                    except JSONRPCException as e:
                        numErrors += 1
                        errorFile.write("Error when loading prevout {} for transaction {}: {}\n".format(prevHash, txid, e))
                        continue
                    totalVIn += prevTx["vout"][prevN]["value"]
                    isSpendingCoinBase |= len(prevTx["vin"]) == 1 and "coinbase" in prevTx["vin"][0]

        totalVOut = 0
        for vout in tx["vout"]:
            value = vout["value"]
            cachedTx.values.append(value)
            totalVOut += value

        totalJSIn = 0
        totalJSOut = 0
        for js in tx["vjoinsplit"]:
            totalJSIn += js["vpub_new"]
            totalJSOut += js["vpub_old"]

        formatVIn = "{0:.8f}".format(totalVIn)
        formatVOut = "{0:.8f}".format(totalVOut)
        formatJSIn = "{0:.8f}".format(totalJSIn)
        formatJSOut = "{0:.8f}".format(totalJSOut)
        formatCoinBase = "T" if cachedTx.isCoinBase else "F"
        formatSpendingCoinBase = "T" if isSpendingCoinBase else "F"

        statsFile.write("{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                blockHeight, blockTime, txid, formatCoinBase,
                len(tx["vin"]), formatVIn, len(tx["vout"]), formatVOut, 
                len(tx["vjoinsplit"]), formatJSIn, formatJSOut,
                formatSpendingCoinBase))

        numTxs += 1
    
    numBlocks += 1

statsFile.flush()
statsFile.close()

elapsed = int(time.time() - start_time)
elapsed_time_str = "{:02d}:{:02d}:{:02d}".format(elapsed // 3600, (elapsed % 3600 // 60), elapsed % 60)
print "\n{} transactions written to {} in {}".format(numTxs, filePath + statsFileName, elapsed_time_str)
if numErrors > 0:
    print "{} errors written to {}".format(numErrors, filePath + errorFileName)
else:
    errorFile.write("No errors\n")
    print "with no errors"

errorFile.flush()
errorFile.close()