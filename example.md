## Usage Example

```bash
python model.py --input_file data.fits --output_dir ./output --image_column image  --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag  --z_column Zspec --additional_columns RA DEC --crop_size 25 --batch_size 32 --epochs 5

## Outputs

After training, **Hybrid-z** generates the following deliverables in the specified `output_dir`:

## Model Artifacts
- **Model Weights**  
  `model_weights.weights.h5`  
  Saved trained model weights for future inference or fine-tuning.

---

## 📊 Diagnostic Plots

- **Redshift Distribution Histogram**  
  `redshift_distribution.png`  
  Histograms of the spectroscopic redshift distribution for the training, validation, and test datasets.

- **Training History Plots**
  - `huber_loss_curve.png`  
    Training and validation Huber loss as a function of epochs.
  
  - `mae_curve.png`  
    Training and validation Mean Absolute Error (MAE) per epoch.

---

### 📁 Final Prediction Table

- **FITS file**  
  `result_test.fits`  
  Contains the model’s predictions and associated metadata for the test sample, including:

  - Original additional columns (e.g., `RA`, `DEC`)  
  - Photometric magnitudes (as specified in `--mag_columns`)  
  - Spectroscopic redshift values (`Z_spec`)  
  - Predicted photometric redshift values (`Z_phot`)  
  - Residuals between predicted and true redshifts:
    - `dz` = Δz = exp(Z_phot) - exp(Z_spec)
    - `normalized_dz` = Δz / (1 + exp(Z_spec))

---

These outputs provide both quantitative and qualitative insights into the model’s performance and support further scientific analysis, visualization, and validation.

