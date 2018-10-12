#!/usr/bin/env python2
from bitcoinrpc.authproxy import AuthServiceProxy
from os.path import expanduser
import os, sys, time

if len(sys.argv) > 3:
    print "Usage: findmindiff.py (BLOCKFROM) (BLOCKTO)"
    exit(1)


class BlockInfo:
    def __init__(self, block_num, diff, time):
        self.block_num = block_num
        self.diff = diff
        self.time = time

    def __str__(self):
        return "{}: diff={}, time={}".format(self.block_num, self.diff, self.time)


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

statsFileName = "stats_mindiff{}-{}.csv".format(block_from, block_to)
statsFile = open(filePath + statsFileName, "w+")

print "\nloading blocks {}-{}...\n".format(block_from, block_to)

totalBlocks = block_to - block_from + 1
onePercent = max(int(round(totalBlocks / 100)), 1)
tenPercent = max(int(round(totalBlocks / 10)), 1)
num_blocks = 0

min_diff = None
min_diff_blocks = []

last_block_time = None

start_time = time.time()
last_update_time = start_time

statsFile.write("blockHeight,blockTimeDelta,difficulty\n")

for block_height in xrange(block_from, block_to + 1):  # +1 so inclusive
    if num_blocks > 0 and num_blocks % onePercent == 0:
        sys.stdout.write(".")
        sys.stdout.flush()
    if num_blocks > 0 and num_blocks % tenPercent == 0:
        current_time = time.time()
        elapsed = int(current_time - last_update_time)
        print " +{:02d}:{:02d}:{:02d}".format(elapsed // 3600, (elapsed % 3600 // 60), elapsed % 60)
        last_update_time = current_time

    block = None
    for attempt in xrange(1, 3):  # 2 tries
        try:
            block = api.getblock("{}".format(block_height), 2)
            break
        except Exception as e:
            # Create a new proxy as we may not be able to send more requests without a new connection
            api = AuthServiceProxy("http://username:password@127.0.0.1:8232")

    if block is None:
        print "Skipping block {}\n".format(block_height)
        continue

    diff = block["difficulty"]
    block_time = block["time"]

    block_time_elapsed = 0
    if last_block_time is not None:
        block_time_elapsed = block_time - last_block_time

    if min_diff is None or diff < min_diff:
        min_diff = diff
        min_diff_blocks = [BlockInfo(block_height, diff, block_time_elapsed)]
    elif diff == min_diff:
        min_diff_blocks.append(BlockInfo(block_height, diff, block_time_elapsed))

    statsFile.write("{},{},{}\n".format(block_height, block_time_elapsed, diff))

    last_block_time = block_time

    num_blocks += 1

statsFile.flush()
statsFile.close()

elapsed = int(time.time() - start_time)
elapsed_time_str = "{:02d}:{:02d}:{:02d}".format(elapsed // 3600, (elapsed % 3600 // 60), elapsed % 60)

print "\n{} blocks written to {} in {}\n".format(num_blocks, filePath + statsFileName, elapsed_time_str)

print "Min diff = {}, Number of blocks = {}".format(min_diff, len(min_diff_blocks))
for block_info in min_diff_blocks:
    print block_info
