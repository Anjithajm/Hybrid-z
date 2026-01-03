.. Hybrid-z documentation master file, created for Read the Docs

.. image:: https://github.com/user-attachments/assets/b18c2440-0219-4c43-aabd-a007ad7b0860
   :alt: Hybrid-z
   :align: center
   :width: 800px

Hybrid-z
=========

**Hybrid-z** is a deep learning package made for photometric redshift estimation using 4-band imaging data combined with 9-band photometric magnitudes. This hybrid model combines convolutional neural networks and fully connected layers for predicting redshifts of galaxies/quasars.

For a detailed description of the methodology, please refer to the following publication and cite it if you use it:  
`A&A 2025 <https://www.aanda.org/articles/aa/full_html/2025/06/aa53576-24/aa53576-24.html>`_.

---

Requirements
------------

- Python 3.7 or later  
- TensorFlow 2.19.0  
- NumPy 2.1.3  
- Pandas 2.2.3  
- Astropy 7.0.1  
- scikit-learn 1.6.1  
- Matplotlib 3.10.0  

Install dependencies with:

.. code-block:: bash

    pip install tensorflow==2.19.0 numpy==2.1.3 pandas==2.2.3 astropy==7.0.1 scikit-learn==1.6.1 matplotlib==3.10.0

---

Input Data Format
-----------------

**Hybrid-z** requires input data in the form of a **FITS or HDF5** file containing both **image cutouts** and associated **photometric and spectroscopic measurements**.  

### Image Column

- **Column Name:** As specified via the `--image_column` argument (e.g., `image`)  
- **Data Type:** NumPy-compatible arrays (image pixel values)  
- **Shape:** (N_objects, cutout_size, cutout_size, 4)  
- **Description:** Pixel data for each source, typically centered on the object of interest. Images are cropped to a square size set by the `--crop_size` parameter.

### Photometric Magnitude Columns

- **Column Names:** As specified via the `--mag_columns` argument  
  *(e.g., `umag`, `gmag`, `rmag`, `imag`, `Zmag`, `Ymag`, `Jmag`, `Hmag`, `KSmag`)*  
- **Data Type:** Float  
- **Description:** Apparent magnitudes for each source in multiple photometric bands.

### Spectroscopic Redshift Column

- **Column Name:** As specified via the `--z_column` argument (e.g., `Zspec`)  
- **Data Type:** Float  
- **Description:** Spectroscopic redshift value for each source, used as the ground truth for training, validation, and testing.

### Additional Columns *(Optional)*

- **Column Names:** As specified via the `--additional_columns` argument *(e.g., `RA`, `DEC`)*  
- **Data Type:** Float or string  
- **Description:** Additional columns to be saved in the final output prediction table.

---

Example FITS Table Structure
----------------------------

+------------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-----------+-----------+
| image      | umag  | gmag  | rmag  | imag  | Zmag  | Ymag  | Jmag  | Hmag  | KSmag | Zspec | RA        | DEC       |
+============+=======+=======+=======+=======+=======+=======+=======+=======+=======+=======+===========+===========+
| (numpy array) | 22.41 | 21.63 | 20.75 | 20.10 | 19.80 | 19.60 | 19.50 | 19.40 | 19.35 | 0.755 | 150.116321 | 2.20583 |
+------------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-----------+-----------+
| ...        | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...       | ...       |
+------------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-----------+-----------+

**Note:** All photometric magnitudes should not contain any NaN values.

---

Usage Example
-------------

To train the model:

.. code-block:: bash

    python model.py --input_file data.fits --output_dir ./output --image_column image \
        --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag \
        --z_column Zspec --additional_columns RA DEC \
        --crop_size 25 --batch_size 32 --epochs 5

**Cutout size calculation**:

- **cutout size (arcsec):** 8  
- **Pixel scale:** 0.2 arcsec/pixel  
- **cutout size in pixels:** cutout_size_arcsec / pixel_scale = 40 × 40 pixels

Early stopping is used to terminate training if validation loss does not improve.

---

Output
------

After training, **Hybrid-z** generates:

- **Model Weights**: `model_weights.weights.h5`  
- **Redshift Distribution Histogram**: `redshift_distribution.png`  
- **Training History Plots**:  
  - `huber_loss_curve.png`  
  - `mae_curve.png`  
- **Final Prediction Table**: `result_test.fits`  

The table contains:

- Original additional columns (RA, DEC)  
- Photometric magnitudes  
- Spectroscopic redshift (`Z_spec`)  
- Predicted photometric redshift (`Z_phot`)  
- Residuals (`dz` = Z_phot - Z_spec, `normalized_dz` = Δz / (1 + Z_spec))

---

Using Pre-trained Model Weights
-------------------------------

To use saved weights for prediction:

.. code-block:: bash

    python test.py --input_file data.fits --image_column image --crop_size 25 \
        --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag \
        --additional_columns RA DEC \
        --weights_path ./model_weights.weights.h5 \
        --output_dir ./predictions

**Note:** The `crop_size` must match the training crop size.

---

Acknowledgements
----------------

This work is supported by the Polish National Science Center through grants:  

- 2020/38/E/ST9/00395  
- 2018/31/G/ST9/03388
