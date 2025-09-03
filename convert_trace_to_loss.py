import os
import numpy as np

MTU=1500
INTERVAL_MS=1000/60
OUTPUT_DIR = "pktloss"

def convert(fpath, fname):
    fout = os.path.splitext(fname)[0] + ".pktloss"
    with open(os.path.join(fpath, fname), 'r') as fin, open(os.path.join(OUTPUT_DIR, fout), 'w') as fout:
        # write the code to Read the bandwidth and loss rate in the format of "2.50Mbps 48.0ms 0.67"
        for line in fin.readlines():
            # Split the line into parts
            parts = line.strip().split()
            bandwidth = float(parts[0].replace("Mbps", ""))
            delay = float(parts[1].replace("ms", ""))
            loss_rate = float(parts[2])
            
            num_pkts = np.round(bandwidth * 1000 * INTERVAL_MS / MTU / 8)
            num_loss = np.round(num_pkts * loss_rate)
            num_recv = num_pkts - num_loss
            outstr = "0 " * int(num_recv) + "1 " * int(num_loss)
            fout.write(outstr)


for fname in os.listdir("traces"):
    if fname.endswith(".log"):
        convert("traces", fname)