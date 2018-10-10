#!/usr/bin/env python2
from bitcoinrpc.authproxy import AuthServiceProxy
import sys
import time

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

print "\nloading blocks {}-{}...\n".format(block_from, block_to)

totalBlocks = block_to - block_from + 1
onePercent = max(int(round(totalBlocks / 100)), 1)
tenPercent = max(int(round(totalBlocks / 10)), 1)
numBlocks = 0

start_time = time.time()
last_update_time = start_time

min_diff = None
min_diff_blocks = []

last_block_time = None

for block_height in xrange(block_from, block_to + 1):  # +1 so inclusive
    if numBlocks > 0 and numBlocks % onePercent == 0:
        sys.stdout.write(".")
        sys.stdout.flush()
    if numBlocks > 0 and numBlocks % tenPercent == 0:
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

    block_time_elapsed = None
    if last_block_time is not None:
        block_time_elapsed = block_time - last_block_time

    if min_diff is None or diff < min_diff:
        min_diff = diff
        min_diff_blocks = [BlockInfo(block_height, diff, block_time_elapsed)]
    elif diff == min_diff:
        min_diff_blocks.append(BlockInfo(block_height, diff, block_time_elapsed))
    
    last_block_time = block_time

    numBlocks += 1

elapsed = int(time.time() - start_time)
elapsed_time_str = "{:02d}:{:02d}:{:02d}".format(elapsed // 3600, (elapsed % 3600 // 60), elapsed % 60)

print "\nFinished in {}".format(elapsed_time_str)

print "Min diff = {}".format(min_diff)
for block_info in min_diff_blocks:
    print block_info
