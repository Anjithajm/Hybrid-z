Input Data Format
=================

Hybrid-z requires input data in the form of a **FITS or HDF5** file containing both **image cutouts** and associated **photometric and spectroscopic measurements**. The FITS file must be structured with the following columns:

Image Column
------------

- **Column Name:** As specified via the ``--image_column`` argument (e.g., ``image``)
- **Data Type:** NumPy-compatible arrays (image pixel values)
- **Shape:** (N_objects, cutout_size, cutout_size, 4) — here, 4 is the number of bands
- **Description:** Pixel data for each source, typically centered on the object of interest. Images are cropped to a square size set by the ``--crop_size`` parameter (e.g., 25×25 pixels)

Photometric Magnitude Columns
-----------------------------

- **Column Names:** As specified via the ``--mag_columns`` argument  
  (e.g., ``umag``, ``gmag``, ``rmag``, ``imag``, ``Zmag``, ``Ymag``, ``Jmag``, ``Hmag``, ``KSmag``)
- **Data Type:** Float
- **Description:** Apparent magnitudes for each source in multiple photometric bands

Spectroscopic Redshift Column
-----------------------------

- **Column Name:** As specified via the ``--z_column`` argument (e.g., ``Zspec``)
- **Data Type:** Float
- **Description:** Spectroscopic redshift value for each source, used as the ground truth for training, validation, and testing

Additional Columns *(Optional)*
-------------------------------

- **Column Names:** As specified via the ``--additional_columns`` argument (e.g., ``RA``, ``DEC``)
- **Data Type:** Float or string
- **Description:** Additional columns to be saved in the final output prediction table

Example FITS Table Structure
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 5 5 5 5 5 5 5 5 5 5 10 10

   * - image
     - umag
     - gmag
     - rmag
     - imag
     - Zmag
     - Ymag
     - Jmag
     - Hmag
     - KSmag
     - Zspec
     - RA
     - DEC
   * - (numpy array)
     - 22.41
     - 21.63
     - 20.75
     - 20.10
     - 19.80
     - 19.60
     - 19.50
     - 19.40
     - 19.35
     - 0.755
     - 150.116321
     - 2.20583
   * - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...

.. note::

   All photometric magnitudes should not contain any NaN values.

Usage Example
=============

This section explains how to train the model.

.. code-block:: bash

   python model.py --input_file data.fits --output_dir ./output \
       --image_column image \
       --mag_columns umag gmag rmag imag Zmag Ymag Jmag Hmag KSmag \
       --z_column Zspec \
       --additional_columns RA DEC \
       --crop_size 25 --batch_size 32 --epochs 5

The ``crop_size`` is the desired image size for the model training (in pixels). To compute the cutout size in pixels:

- **cutout size_arcsec** = 8 arcseconds
- **Pixel scale** = 0.2 arcseconds per pixel

.. math::

   \text{cutout\_size\_pixels} = \frac{\text{cutout\_size\_arcsec}}{\text{pixel\_scale}}

**Final cutout size:** 40 × 40 pixels

An early stopping criterion is employed, allowing the number of training epochs to be set to a relatively high value (e.g., ``--epochs 200``). The training process will automatically terminate if no improvement in the validation loss is observed for a predefined number of consecutive epochs.

You can download the ``data.fits`` file for a test run.
