cat > docs/source/installation.rst << 'EOF'
Installation
============

Prerequisites
-------------
- Python 3.8 or higher
- CUDA-capable GPU (optional, for faster training)

Install from repository
-----------------------

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/Anjithajm/Hybrid-z.git
   cd Hybrid-z

2. Install dependencies:

.. code-block:: bash

   pip install -r requirements.txt

3. Install the package in development mode:

.. code-block:: bash

   pip install -e .

Dependencies
------------

The main dependencies are:

* TensorFlow >= 2.10
* NumPy >= 1.21
* Pandas >= 1.3
* Astropy >= 5.0
* scikit-learn >= 1.0
* Matplotlib >= 3.5
* Seaborn >= 0.11

All dependencies are listed in ``requirements.txt``.

Verification
------------

To verify the installation, run:

.. code-block:: python

   import hybrid_z
   print(hybrid_z.__version__)
EOF
