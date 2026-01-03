Output
======

After training, **Hybrid-z** generates the following output in the specified ``output_dir``:

Model Weights
-------------

``model_weights.weights.h5``  
Saved trained model weights for future testing.

Redshift Distribution Histogram
-------------------------------

``redshift_distribution.png``  
Histograms of the spectroscopic redshift distribution for the training, validation, and test datasets.

Training History Plots
----------------------

- ``huber_loss_curve.png``  
  Training and validation Huber loss as a function of epochs.

- ``mae_curve.png``  
  Training and validation Mean Absolute Error (MAE) per epoch.

Final Prediction Table
----------------------

``result_test.fits``  
Contains the model’s predictions and associated metadata for the test sample, including:

- Original additional columns (e.g., ``RA``, ``DEC``)
- Photometric magnitudes (as specified in ``--mag_columns``)
- Spectroscopic redshift values (``Z_spec``)
- Predicted photometric redshift values (``Z_phot``)
- Residuals between predicted and true redshifts:
  
  - ``dz`` = Δz = Z_phot - Z_spec
  - ``normalized_dz`` = Δz / (1 + Z_spec)

How to Use the Pre-Trained Model
================================

To use the saved model weights for photometric redshift prediction, run the ``test.py`` script with the required arguments. Example usage:

.. code-block:: bash

   python test.py --input_file data.fits \
       --image_column image \
       --crop_size 25 \
       --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag \
       --additional_columns RA DEC \
       --weights_path ./model_weights.weights.h5 \
       --output_dir ./predictions

The output table will be saved in the ``predictions`` directory.

**Note:** The ``crop_size`` parameter must match the image crop size used during model training.
