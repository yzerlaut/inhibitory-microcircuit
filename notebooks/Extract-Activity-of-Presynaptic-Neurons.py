# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import sys, os
sys.path.append('./microns_phase3_nda')


import datajoint as dj
# start mysql database with: "mysql -u root"
# username: "user"
# password ""
# maybe need: GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost';
from microns_phase3 import nda, utils
import numpy as np
import matplotlib.pyplot as plt

# %%
from caveclient import CAVEclient
client = CAVEclient('minnie65_public')
matched_df = client.materialize.query_table('coregistration_manual_v4')

# %%
pre_coreg_BCs = np.load('data/functional/pre_coreg_BCs.npy', allow_pickle=True).item()
pre_coreg_MCs = np.load('data/functional/pre_coreg_MCs.npy', allow_pickle=True).item()

# %%
nMax = 100000

for pre_coreg in [pre_coreg_BCs, pre_coreg_MCs]:
    
    for post in list(pre_coreg.keys()):
        
        unit_keys = []
        for pre in pre_coreg[post][:nMax]:
            
            entry = matched_df[matched_df['pt_root_id']==pre]
            unit_key = entry[['session', 'scan_idx', 'unit_id']].to_dict(orient='records')[0]
            unit_keys.append(unit_key)
    
            # cellular data
            cFile = os.path.join('data', 'functional', 'cells', '%s.npy' % pre)
            cell_data = dict(\
                    session = unit_key['session'],
                    scan_idx = unit_key['scan_idx'],
                    spike_trace = (nda.Activity & unit_key).fetch1('trace'),
                    calcium_trace = (nda.ScanUnit * nda.Fluorescence & unit_key).fetch1('trace')
            )
            np.save(cFile, cell_data)
            
            # session data
            sFile = os.path.join('data', 'functional', 'sessions', 'session_%i-scan_idx_%i.npy' % (unit_key['session'], unit_key['scan_idx']))
            if not os.path.isfile(sFile):
                session_data = dict(\
                    movie = (nda.Stimulus & unit_key).fetch1('movie'),
                    nframes = (nda.Scan & unit_key).fetch1('nframes'),
                    fps = (nda.Scan & unit_key).fetch1('fps'),
                    pupil_radius = (nda.ManualPupil & unit_key).fetch1('pupil_maj_r'),
                    treadmill = (nda.Treadmill & unit_key).fetch1('treadmill_velocity'))
                np.save(sFile, session_data)



# %%
for unit_key in unit_keys[:1]:
    
    nframes, fps = (nda.Scan & unit_key).fetch1('nframes', 'fps')  # fetch # frames and fps
    time_axis = np.arange(nframes)/ fps # create time axis (seconds)
    spike_trace = (nda.Activity & unit_key).fetch1('trace') # fetch spike trace
    calcium_trace = (nda.ScanUnit * nda.Fluorescence & unit_key).fetch1('trace') # fetch calcium fluorescence trace
    pupil_radius = (nda.ManualPupil & unit_key).fetch1('pupil_maj_r') # fetch manually segmented pupil trace 
    treadmill = (nda.Treadmill & unit_key).fetch1('treadmill_velocity') # fetch treadmill speed
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8), sharex=True)
    ax1.plot(time_axis, calcium_trace, color='g', alpha=0.3, label='calcium trace')
    ax1.plot(time_axis, spike_trace, color='k', label='spike trace')
    ax2.plot(time_axis, pupil_radius, color='k')
    ax3.plot(time_axis, treadmill, color='k')
    ax3.set_xlim(3000, 4000) 
    ax1.set_ylabel('response magnitude')
    ax1.legend()
    ax2.set_ylabel('pupil radius')
    ax3.set_ylabel('treadmill speed')
    fig.suptitle(f'session: {unit_key["session"]}, scan_idx: {unit_key["scan_idx"]}, unit_id: {unit_key["unit_id"]}', fontsize=22);
    [ax.spines['right'].set_visible(False) for ax in [ax1, ax2, ax3]];
    [ax.spines['top'].set_visible(False) for ax in [ax1, ax2, ax3]];

# %%
