import numpy as np
import matplotlib.pyplot as plt
import random
from astropy.table import Table

d1=Table.read(r'/home/anjitha/kids/Training Tables/Training_KiDS_DR4_x_Equatorial_36_gaap9_cleaned.hdf5')

################################################################################################
################CODE to subselect sample in histogram based on neigbouring heights##############
################Made by PJ for Anjitha's galaxy photo-z ML checks of the training data##########
################################################################################################



data_org=d1

data_x = data_org['Z'] # np.random.normal(loc=0, scale=4, size=700)
kids_id_x = data_org['KiDS_ID']

# Combine both KiDS_ID and Z into tuples
data_pairs = list(zip(kids_id_x, data_x))

# Compute histogram
print('-------------------If you want to change something these are the only parameters to be changed---')
counts_x, bins = np.histogram(data_x, bins=81)

#model4:
iterations =60 #3
threshold_init =3 #10 #initial threshold
threshold_step =5 #3 #reduction is threshold

print('-----------------Remember if you change thing the IDS selected will change even if random state is same---')
#
data = data_x.copy()
counts = counts_x.copy()
smoothed_counts = counts_x.copy()

random_state = 42  #important to generate same KiDS_ID everytime
random.seed(random_state)

plt.figure(figsize=(12, 6)) 
plt.hist(data,bins=bins, edgecolor='black',alpha=0.6, label='Original Histogram')

#The main code which took the most part to develop this
for iteration in range(iterations):
    threshold = threshold_init-iteration*threshold_step  
    subsample_data_pairs = []
    for i in range(1, len(counts) - 1):
        bin_id = np.where((data > bins[i]) & (data <= bins[i+1]))[0]
        if ((counts[i] > counts[i-1]+threshold) & (counts[i] > counts[i+1]+threshold)) or (counts[i] > counts[i-1]+2*threshold) or (counts[i] > counts[i+1]+2*threshold): 
            smoothed_counts[i] = min([(counts[i - 1] + counts[i + 1]) / 2,counts[i]])
        selected_pairs = random.sample([data_pairs[j] for j in bin_id], k=smoothed_counts[i])
        subsample_data_pairs.extend(selected_pairs)


    # Convert the subsampled data pairs to arrays
    subsample_data_pairs = np.array(subsample_data_pairs)
    data_pairs = subsample_data_pairs.copy()
    # Separate the KiDS_ID and Z values
    subsample_kids_ids = subsample_data_pairs[:, 0]  # First column is KiDS_ID
    subsample_data = subsample_data_pairs[:, 1]  # Second column is Z
        
    subsample_data = np.array(subsample_data)
    data = subsample_data.copy()
    counts = smoothed_counts.copy()
    print(f'For {iteration+1} subsample data = {len(subsample_kids_ids)} whereas unique IDs are {len(np.unique(subsample_kids_ids))}')
    plt.hist(subsample_data,bins=bins,  alpha=0.5, label=f'Smoothed Histogram {iteration+1}')
plt.hist(subsample_data,bins=bins,histtype='step', label='Final subsample z',color='k')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram Smoothing')
plt.legend()
#plt.show()
plt.close()

print('------------------The KiDS subsample IDS are:---------------------')
print(subsample_kids_ids)
print('------------------The KiDS subsample z are:---------------------')
print(subsample_data)
print('--------Now you can just save these IDs to select from abive HDF file :)------')
print(f'Sample remaining is {len(subsample_data)*100/len(data_org)} %')

len(subsample_kids_ids)


# Convert the KiDS_IDs to the same type for filtering 
subsample_kids_ids = subsample_kids_ids.astype(data_org['KiDS_ID'].dtype)

# Select rows from the original data that match the subsampled KiDS_IDs
selected_data = data_org[np.isin(data_org['KiDS_ID'], subsample_kids_ids)]

data=selected_data

