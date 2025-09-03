import gilbert_elliot_model
import numpy as np
import os
import multiprocessing as mp
from tqdm import tqdm
import sys

pbar = tqdm (smoothing=0, ncols=80)

def process_file(fname):
    """
    Process a single file: fit the Gilbert-Elliot model.
    """
    sys.stdout = open('a.out','a')
    sys.stderr = open('a.err','a')
    obs = np.loadtxt(os.path.join("pktloss", fname), dtype=int)
    p, r, k, n, model = gilbert_elliot_model.fit_hmm(
        obs, init_params={'k': 1, 'h': 0}
    )
    category = fname.split("-")[0]
    return category, fname, p, r

def pbar_update (result):
    pbar.update ()
    with open("gilbert-regression.csv", "a") as f:
        category, fname, p, r = result
        f.write(f"{fname},{category},{p},{r}\n")
    

if __name__ == '__main__':
    pool = mp.Pool(processes=mp.cpu_count())
    fnames = [
        fname for fname in os.listdir("pktloss") if fname.endswith(".pktloss")
    ]
    
    with open("gilbert-regression.csv", "a") as f:
        f.write(f"\n")
        
    pbar.reset (total=len (fnames))
    for fname in fnames:
        pool.apply_async(process_file, args=(fname,), callback=pbar_update)

    pool.close ()
    pool.join ()
    pbar.close ()
    