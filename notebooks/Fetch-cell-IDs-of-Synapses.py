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
from caveclient import CAVEclient
client = CAVEclient('minnie65_public')

# %%
client.materialize.get_tables()

# %%
coreg = client.materialize.query_table('coregistration_manual_v4')

# %%
coreg

# %%
v1types = client.materialize.query_table('allen_v1_column_types_slanted_ref')

# %%
BCs = v1types[v1types['cell_type']=='BC']
len(BCs)

# %%
MCs = v1types[v1types['cell_type']=='MC']
len(MCs)

# %%
MCs_pre = {}

for i in range(len(MCs)):

    MCs_pre[str(MCs['pt_root_id'].values[i])] = []
    
    input_syn_df = client.materialize.synapse_query(post_ids=MCs['pt_root_id'].values[i])

    for j in range(len(input_syn_df['pre_pt_root_id'])):
        
        cond = input_syn_df['pre_pt_root_id'].values[j]==coreg['pt_root_id']

        if np.sum(cond)==1:

            MCs_pre[str(MCs['pt_root_id'].values[i])].append(\
                            input_syn_df['pre_pt_root_id'].values[j])
            
    print('cell %i' % (1+i), ' nsyn = %i ' % len(MCs_pre[str(MCs['pt_root_id'].values[i])]))


# %%
np.save('data/pre_coreg_MCs.npy', MCs_pre)

# %%
BCs_pre = {}

for i in range(len(BCs)):

    BCs_pre[str(BCs['pt_root_id'].values[i])] = []
    
    input_syn_df = client.materialize.synapse_query(post_ids=BCs['pt_root_id'].values[i])

    for j in range(len(input_syn_df['pre_pt_root_id'])):
        
        cond = input_syn_df['pre_pt_root_id'].values[j]==coreg['pt_root_id']

        if np.sum(cond)==1:

            BCs_pre[str(BCs['pt_root_id'].values[i])].append(\
                            input_syn_df['pre_pt_root_id'].values[j])
            
    print('cell %i' % (1+i), ' nsyn = %i ' % len(BCs_pre[str(BCs['pt_root_id'].values[i])]))
np.save('data/pre_coreg_BCs.npy', BCs_pre)
