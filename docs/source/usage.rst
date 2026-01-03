Usage
=====

.. _usage:

Installation
------------

To use Hybrid-z, first make sure you have installed the required dependencies:

.. code-block:: bash

    pip install tensorflow==2.19.0 numpy==2.1.3 pandas==2.2.3 astropy==7.0.1 scikit-learn==1.6.1 matplotlib==3.10.0

Training the model
------------------

To train the Hybrid-z model, run the following command:

.. code-block:: bash

    python model.py --input_file data.fits --output_dir ./output \
        --image_column image \
        --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag \
        --z_column Zspec \
        --additional_columns RA DEC \
        --crop_size 25 --batch_size 32 --epochs 5

- ``crop_size``: image size in pixels for the model  
- ``epochs``: number of training epochs (early stopping will terminate if validation loss stops improving)

Testing / Using pre-trained weights
-----------------------------------

Once the model is trained or if you have pre-trained weights, you can run predictions:

.. code-block:: bash

    python test.py --input_file data.fits \
        --image_column image \
        --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag \
        --additional_columns RA DEC \
        --weights_path ./model_weights.weights.h5 \
        --crop_size 25 \
        --output_dir ./predictions

This will save the predicted redshifts and associated metadata in the specified output directory.

