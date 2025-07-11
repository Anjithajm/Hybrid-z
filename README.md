# Hybrid-z
It is a deep learning package for the photometric redshift estimation from 4-band images and 9-band magnitudes.
# Requirements

Python 3.7 or later
TensorFlow 2.19.0
NumPy 2.1.3
Pandas 2.2.3
Astropy 7.0.1
scikit-learn 1.6.1
Matplotlib 3.10.0

# To run the script 
python model.py --input_file ./data/data.fits --output_dir ./output --image_column image --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag --z_column Zspec --additional_columns RA DEC --crop_size 25 --batch_size 32 --epochs 5
