# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy as np

# %%
pre_coreg_BCs = np.load('data/functional/pre_coreg_BCs.npy', allow_pickle=True).item()

def process(pre, post):

    cell = np.load('data/functional/cells/%i.npy' % post, allow_pickle=True).item()
    print(cell)
    session = np.load('data/functional/sessions/session_%i-scan_idx_%i.npy' %\
                                                 (cell['session'], cell['scan_idx']), allow_pickle=True).item()
    
    return cell, session

pre = list(pre_coreg_BCs.keys())[0]
post = pre_coreg_BCs[pre][0]
cell, session = process(pre, post)

# %%
cell

# %%
