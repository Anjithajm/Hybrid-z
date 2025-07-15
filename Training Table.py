from astropy.table import Table
from astropy.io import fits
import numpy as np
import pandas as pd
import random
import os

qso=Table.read(r'/home/anjitha/quasars/inputdata/DR4_ QSO_compil_with_DESI_EDR_Jan21.csv')

magnitude_columns = ['MAG_GAAP_u', 'MAG_GAAP_g', 'MAG_GAAP_r', 'MAG_GAAP_i', 'MAG_GAAP_Z', 'MAG_GAAP_Y', 'MAG_GAAP_J', 'MAG_GAAP_H', 'MAG_GAAP_Ks']
magnitudes = np.array([qso[col] for col in magnitude_columns]).T  # Convert to NumPy array and transpose

# Check for NaN values in the magnitude columns
nan_mask = np.isnan(magnitudes).any(axis=1)

# Apply the mask to filter out rows with NaN values
data_filtered = qso[~nan_mask]
qso=data_filtered
len(qso)

from astropy.table import Table


cols = [
    "ID",
    "MAG_AUTO_CALIB", "MAGERR_AUTO",
    "RAJ2000", "DECJ2000",
    "A_WORLD", "B_WORLD",
    "FLUX_RADIUS", "CLASS_STAR",
    "SG2DPHOT", "KIDS_TILE",
    "MAG_GAAP_u", "MAGERR_GAAP_u",
    "MAG_GAAP_g", "MAGERR_GAAP_g",
    "MAG_GAAP_r", "MAGERR_GAAP_r",
    "MAG_GAAP_i", "MAGERR_GAAP_i",
    "MAG_GAAP_Z", "MAGERR_GAAP_Z",
    "MAG_GAAP_Y", "MAGERR_GAAP_Y",
    "MAG_GAAP_J", "MAGERR_GAAP_J",
    "MAG_GAAP_H", "MAGERR_GAAP_H",
    "MAG_GAAP_Ks", "MAGERR_GAAP_Ks",
    "SG_FLAG", "MASK",
    "Z", "ZERR", "ZWARN"
]

# 3. Slice out those columns into a new Table
data1 = qso[cols]

# 4. (Optional) verify
print(data1.colnames)
data1.info()

def sanitize_table(data1):
    for col in data1.colnames:
        if data1[col].dtype.kind == 'b':  # Boolean type
            data1[col] = data1[col].astype(int)
        elif data1[col].dtype.kind == 'S':  # Byte strings
            data1[col] = data1[col].astype(str)
    return data1

# Sanitize the table to ensure compatibility
data_sanitized = sanitize_table(data1)



data1 = Table()
data1['ID'] = qso['ID']
data1['RAJ2000'] = qso['RAJ2000']
data1['DECJ2000'] = qso['DECJ2000']
data1['Zspec'] = qso['Zspec']
#data1['QSO_PHOTO']=qso['QSO_PHOTO_1']
#data1['Z_PHOTO_QSO']=qso['Z_PHOTO_QSO_1']
#data1['Z_PHOTO_STDDEV_QSO']=qso['Z_PHOTO_STDDEV_QSO_1']
data1['Z_B'] = qso['Z_B']

data1['MASK']=qso['MASK']
data1['CLASS_STAR']=qso['CLASS_STAR']
data1['SG2DPHOT']=qso['SG2DPHOT']

data1['MAG_GAAP_u']=qso['MAG_GAAP_u']
data1['MAGERR_GAAP_u']=qso['MAGERR_GAAP_u']
data1['FLAG_GAAP_u']=qso['FLAG_GAAP_u']

data1['MAG_GAAP_g']=qso['MAG_GAAP_g']
data1['MAGERR_GAAP_g']=qso['MAGERR_GAAP_g']
data1['FLAG_GAAP_g']=qso['FLAG_GAAP_g']

data1['MAG_GAAP_r']=qso['MAG_GAAP_r']
data1['MAGERR_GAAP_r']=qso['MAGERR_GAAP_r']
data1['FLAG_GAAP_r']=qso['FLAG_GAAP_r']

data1['MAG_GAAP_i']=qso['MAG_GAAP_i']
data1['MAGERR_GAAP_i']=qso['MAGERR_GAAP_i']
data1['FLAG_GAAP_i']=qso['FLAG_GAAP_i']

data1['MAG_GAAP_Z']=qso['MAG_GAAP_Z']
data1['MAGERR_GAAP_Z']=qso['MAGERR_GAAP_Z']
data1['FLAG_GAAP_Z']=qso['FLAG_GAAP_Z']

data1['MAG_GAAP_Y']=qso['MAG_GAAP_Y']
data1['MAGERR_GAAP_Y']=qso['MAGERR_GAAP_Y']
data1['FLAG_GAAP_Y']=qso['FLAG_GAAP_Y']

data1['MAG_GAAP_J']=qso['MAG_GAAP_J']
data1['MAGERR_GAAP_J']=qso['MAGERR_GAAP_J']
data1['FLAG_GAAP_J']=qso['FLAG_GAAP_J']

data1['MAG_GAAP_H']=qso['MAG_GAAP_H']
data1['MAGERR_GAAP_H']=qso['MAGERR_GAAP_H']
data1['FLAG_GAAP_H']=qso['FLAG_GAAP_H']

data1['MAG_GAAP_Ks']=qso['MAG_GAAP_Ks']
data1['MAGERR_GAAP_Ks']=qso['MAGERR_GAAP_Ks']
data1['FLAG_GAAP_Ks']=qso['FLAG_GAAP_Ks']

data1['COLOUR_GAAP_u_g']=qso['COLOUR_GAAP_u_g']
data1['COLOUR_GAAP_g_r']=qso['COLOUR_GAAP_g_r']
data1['COLOUR_GAAP_r_i']=qso['COLOUR_GAAP_r_i']
data1['COLOUR_GAAP_i_Z']=qso['COLOUR_GAAP_i_Z']
data1['COLOUR_GAAP_Z_Y']=qso['COLOUR_GAAP_Z_Y']
data1['COLOUR_GAAP_Y_J']=qso['COLOUR_GAAP_Y_J']
data1['COLOUR_GAAP_J_H']=qso['COLOUR_GAAP_J_H']
data1['COLOUR_GAAP_H_Ks']=qso['COLOUR_GAAP_H_Ks']

data1['source']=qso['source']

sample_size = len(data1)
rn_id = random.sample(range(0, len(data1)), sample_size)
data = data1[rn_id] 
size = len(data)

IMS = np.zeros((size,36,36,4))
band=['u','r','i','g']


idx=[]
for i, id in enumerate(data['RAJ2000']):
    file_path = os.path.join("home/anjitha/quasars/final/cutout/", band[0]+'band', 'z'+band[0]+'_galaxy_'+str(data['RAJ2000'][i])+"_"+str(data['DECJ2000'][i])+".fits")
    file_p = os.path.isfile(file_path)
    print(file_path)
    print(file_p)
    if file_p:
        u_shape = np.shape(fits.getdata(file_path))
        r_shape = np.shape(fits.getdata(file_path))
        i_shape = np.shape(fits.getdata(file_path))
        g_shape = np.shape(fits.getdata(file_path))
        if (u_shape == (36,36)) & (r_shape == (36,36)) & (i_shape == (36,36)) & (g_shape == (36,36)):
            IMS[i,:,:,0] = fits.getdata(file_path)
            IMS[i,:,:,1] = fits.getdata(file_path)
            IMS[i,:,:,2] = fits.getdata(file_path)
            IMS[i,:,:,3] = fits.getdata(file_path)
            idx.append(i)
idx = np.array(idx)
idx
new_data_o=data[idx]

new_data_o.write(r'/home/anjitha/quasars/Training Tables/Training_KiDS_DR4_.hdf5', path='\ground', append=True, serialize_meta=True)