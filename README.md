# Hybrid-z

**Hybrid-z** is a deep learning package designed for photometric redshift estimation using 4-band imaging data combined with 9-band photometric magnitudes. This hybrid model combines convolutional neural networks and fully connected layers for redshift predictions.

---

## Requirements

- Python 3.7 or later  
- TensorFlow 2.19.0  
- NumPy 2.1.3  
- Pandas 2.2.3  
- Astropy 7.0.1  
- scikit-learn 1.6.1  
- Matplotlib 3.10.0  

Install dependencies with:

```bash
pip install tensorflow==2.19.0 numpy==2.1.3 pandas==2.2.3 astropy==7.0.1 scikit-learn==1.6.1 matplotlib==3.10.0
```
## 📄 Input Data Format

**Hybrid-z** requires input data in the form of a **FITS (Flexible Image Transport System)** file containing both **image cutouts** and associated **photometric and spectroscopic measurements**. The FITS file must be structured with the following columns:

### 🖼️ Image Column  
- **Column Name:** As specified via the `--image_column` argument (e.g., `image`)
- **Data Type:** 2D NumPy-compatible arrays (image cutouts)
- **Description:** Pixel data for each source, typically centered on the object of interest. Images are cropped to a square size set by the `--crop_size` parameter (e.g., 25×25 pixels).

### 📏 Photometric Magnitude Columns  
- **Column Names:** As specified via the `--mag_columns` argument  
  *(e.g., `umag`, `gmag`, `rmag`, `imag`, `Zmag`, `Ymag`, `Jmag`, `Hmag`, `KSmag`)*  
- **Data Type:** Float  
- **Description:** Apparent magnitudes for each source in multiple photometric bands.

### 📊 Spectroscopic Redshift Column  
- **Column Name:** As specified via the `--z_column` argument (e.g., `Zspec`)  
- **Data Type:** Float  
- **Description:** Spectroscopic redshift value for each source, used as the ground truth for training and validation.

### 🌐 Additional Metadata Columns *(Optional)*  
- **Column Names:** As specified via the `--additional_columns` argument  
  *(e.g., `RA`, `DEC`)*  
- **Data Type:** Float or string  
- **Description:** Additional parameters to be preserved in the final output prediction table, such as right ascension and declination.

---

### 📑 Example FITS Table Structure

| image       | umag  | gmag  | rmag  | imag  | Zmag  | Ymag  | Jmag  | Hmag  | KSmag | Zspec | RA       | DEC      |
|:------------|:------|:------|:------|:------|:------|:------|:------|:------|:------|:------|:-----------|:-----------|
| (2D array)  | 22.41 | 21.63 | 20.75 | 20.10 | 19.80 | 19.60 | 19.50 | 19.40 | 19.35 | 0.755 | 150.116321 | 2.20583   |
| ...         | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...       | ...       |

---

**Note:**  
- All photometric magnitudes should be pre-calibrated and corrected for extinction if necessary.
- Image data should be pre-aligned and centered on the target source.


## Usage Example:

```bash
python model.py --input_file data.fits --output_dir ./output --image_column image --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag --z_column Zspec --additional_columns RA DEC --crop_size 25 --batch_size 32 --epochs 5
```
After training, **Hybrid-z** generates the following deliverables in the specified `output_dir`:

- **Model Weights**  
  `model_weights.weights.h5`  
  Saved trained model weights for future inference or fine-tuning.

---

## Diagnostic Plots

- **Redshift Distribution Histogram**  
  `redshift_distribution.png`  
  Histograms of the spectroscopic redshift distribution for the training, validation, and test datasets.

- **Training History Plots**
  - `huber_loss_curve.png`  
    Training and validation Huber loss as a function of epochs.
  
  - `mae_curve.png`  
    Training and validation Mean Absolute Error (MAE) per epoch.

---

## Final Prediction Table

- **FITS file**  
  `result_test.fits`  
  Contains the model’s predictions and associated metadata for the test sample, including:

  - Original additional columns (e.g., `RA`, `DEC`)  
  - Photometric magnitudes (as specified in `--mag_columns`)  
  - Spectroscopic redshift values (`Z_spec`)  
  - Predicted photometric redshift values (`Z_phot`)  
  - Residuals between predicted and true redshifts:
    - `dz` = Δz = Z_phot - Z_spec
    - `normalized_dz` = Δz / (1 + Z_spec)

---

These outputs provide both quantitative and qualitative insights into the model’s performance and support further scientific analysis, visualization, and validation.
