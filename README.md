# Requirements

pip install python-bitcoinrpc

# Usage

python privacymetrics.py BLOCKFROM BLOCKTO

# Example

python privacymetrics.py 396 433

    aggregate value entering sprout circuit     = 10.71830000
    aggregate value leaving sprout circuit      = 0.27450000
    net shielded value change in sprout circuit = 10.44380000

python privacymetrics.py 1 241964

    aggregate value entering sprout circuit     = 3634697.72584490
    aggregate value leaving sprout circuit      = 3510258.15050241
    net shielded value change in sprout circuit = 124439.57534249

python privacymetrics.py 241965 256819
    aggregate value entering sprout circuit     = 220706.44213950
    aggregate value leaving sprout circuit      = 215666.57193453
    net shielded value change in sprout circuit = 5039.87020497

# Notes

The value entering and leaving the sprout circuit is not a count of
unique coins entering and leaving because the same ZEC can be
shielded and unshielded multiple times.

For example, if you have 1000 ZEC and shield and unshield, the value
entering the sprout circuit will increase by 1000, and the value
leaving the sprout circuit will decrease by 1000.

If you were to shield and unshield 5 times, the value entering the
sprout circuit would increasea by 5000, and the value leaving the
sprout circuit would also increase by 5000.

