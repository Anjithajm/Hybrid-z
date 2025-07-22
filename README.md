
<p align="center">
<img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/9b0240a3-d31f-4b17-9465-8d1ac6d34e11" />
</p>



**Hybrid-z** is a deep learning package made for photometric redshift estimation using 4-band imaging data combined with 9-band photometric magnitudes. This hybrid model combines convolutional neural networks and fully connected layers for predicting redshifts of galaxies/quasars.

For a detailed description of the methodology, please refer to the following publication and cite it if you use: https://www.aanda.org/articles/aa/full_html/2025/06/aa53576-24/aa53576-24.html

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
##  Input Data Format

**Hybrid-z** requires input data in the form of a **FITS or hdf5** file containing both **image cutouts** and associated **photometric and spectroscopic measurements**. The FITS file must be structured with the following columns:

###  Image Column  
- **Column Name:** As specified via the `--image_column` argument (e.g., `image`)
- **Data Type:** NumPy-compatible arrays (image pixel values)
- **Shape:** (N_objects, cutout_size, cutout_size, 4). Here, 4 is number of bands.
- **Description:** Pixel data for each source, typically centered on the object of interest. Images are cropped to a square size set by the `--crop_size` parameter (e.g., 25×25 pixels).

###  Photometric Magnitude Columns  
- **Column Names:** As specified via the `--mag_columns` argument  
  *(e.g., `umag`, `gmag`, `rmag`, `imag`, `Zmag`, `Ymag`, `Jmag`, `Hmag`, `KSmag`)*  
- **Data Type:** Float  
- **Description:** Apparent magnitudes for each source in multiple photometric bands.

###  Spectroscopic Redshift Column  
- **Column Name:** As specified via the `--z_column` argument (e.g., `Zspec`)  
- **Data Type:** Float  
- **Description:** Spectroscopic redshift value for each source, used as the ground truth for training, validation, and testing.

###  Additional Columns *(Optional)*  
- **Column Names:** As specified via the `--additional_columns` argument  
  *(e.g., `RA`, `DEC`)*  
- **Data Type:** Float or string  
- **Description:** Additional columns to be saved in the final output prediction table.

---

### 📑 Example FITS Table Structure

| image       | umag  | gmag  | rmag  | imag  | Zmag  | Ymag  | Jmag  | Hmag  | KSmag | Zspec | RA       | DEC      |
|:------------|:------|:------|:------|:------|:------|:------|:------|:------|:------|:------|:-----------|:-----------|
| (numpy array)  | 22.41 | 21.63 | 20.75 | 20.10 | 19.80 | 19.60 | 19.50 | 19.40 | 19.35 | 0.755 | 150.116321 | 2.20583   |
| ...         | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...       | ...       |

---

**Note:**  
- All photometric magnitudes should not contain any NaN values.

---
## Usage Example:
This section explains how to train the model. 

```bash
python model.py --input_file data.fits --output_dir ./output --image_column image --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag --z_column Zspec --additional_columns RA DEC --crop_size 25 --batch_size 32 --epochs 5
```
`crop_size` is the desired image size for the model training. It is in pixel units.
To compute the cutout size in pixel units:

- **cutout size_arcsec** = 8 arcseconds  
- **Pixel scale** = 0.2 arcseconds per pixel  

The number of pixels along one dimension is given by:
cutout_size_pixels = cutout_size_arcsec / pixel_scale

**Final cutout size**: **40 × 40 pixels**

An early stopping criterion is employed, allowing the number of training epochs to be set to a relatively high value (e.g., `--epochs 200`). The training process will automatically terminate if no improvement in the validation loss is observed for a predefined number of consecutive epochs. 

You can download the `data.fits` file for a test run 

---

## Output
After training, **Hybrid-z** generates the following output in the specified `output_dir`:

- **Model Weights**  
  `model_weights.weights.h5`  
  Saved trained model weights for future testing.


- **Redshift Distribution Histogram**  
  `redshift_distribution.png`  
  Histograms of the spectroscopic redshift distribution for the training, validation, and test datasets.

- **Training History Plots**
  - `huber_loss_curve.png`  
    Training and validation Huber loss as a function of epochs.
  
  - `mae_curve.png`  
    Training and validation Mean Absolute Error (MAE) per epoch.

- **Final Prediction Table**
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
## How to use the pre-trained model weights?
To use the saved model weights for photometric redshift prediction, run the `test.py` script with the required arguments. Example usage is:
```bash
python test.py --input_file data.fits --image_column image --crop_size 25 --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag --additional_columns RA DEC --weights_path /model_weights.weights.h5 --output_dir ./predictions
```
The output table will be saved in the `predictions` directory

**Note:** The `crop_size` parameter must match the image crop size used during model training.

## Acknowledgements
This work is supported by the Polish National Science Center through grants no.
2020/38/E/ST9/00395, and 2018/31/G/ST9/03388. I also acknowledge the Center for Theoretical Physics in Warsaw, Poland.
