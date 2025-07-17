#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import numpy as np
import pandas as pd
import tensorflow as tf
from astropy.table import Table
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from tensorflow.keras import layers, Model
from tensorflow.keras.layers import (Input, Conv2D, AveragePooling2D, MaxPooling2D, Flatten,
                                     Dense, Dropout, BatchNormalization, concatenate)
from tensorflow.keras.losses import Huber
import tensorflow.keras.backend as K

# ---------- Utility Functions ----------

def central_crop(image, target_size):
    start = (image.shape[0] - target_size) // 2
    end = start + target_size
    return image[start:end, start:end, :]

def R2(y_true, y_pred):
    SS_res = K.sum(K.square(y_true - y_pred))
    SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
    return (1 - SS_res / (SS_tot + K.epsilon()))


def inception_module(x, filters):
    tower_1 = Conv2D(filters=filters[0], kernel_size=(1, 1), padding='same', activation='relu',
                     kernel_initializer='he_normal')(x)
    tower_2 = Conv2D(filters=filters[1], kernel_size=(1, 1), padding='same', activation='relu',
                     kernel_initializer='he_normal')(x)
    tower_2 = Conv2D(filters=filters[2], kernel_size=(3, 3), padding='same', activation='relu',
                     kernel_initializer='he_normal')(tower_2)
    tower_3 = Conv2D(filters=filters[3], kernel_size=(1, 1), padding='same', activation='relu',
                     kernel_initializer='he_normal')(x)
    tower_3 = Conv2D(filters=filters[4], kernel_size=(5, 5), padding='same', activation='relu',
                     kernel_initializer='he_normal')(tower_3)
    tower_4 = MaxPooling2D(pool_size=(2, 2), strides=(1, 1), padding='same')(x)
    tower_4 = Conv2D(filters=filters[5], kernel_size=(1, 1), padding='same', activation='relu',
                     kernel_initializer='he_normal')(tower_4)
    return concatenate([tower_1, tower_2, tower_3, tower_4], axis=-1)

# ---------- Main Workflow ----------

def main(args):
    os.makedirs(args.output_dir, exist_ok=True)

    print("Reading data...")
    data = Table.read(args.input_file)
    images = np.array(data[args.image_column].reshape((-1, 36, 36, 4)))
    mag = np.vstack([np.array(data[col]) for col in args.mag_columns]).T

    additional_columns = data[args.additional_columns]
    add_col = np.vstack([additional_columns[field] for field in additional_columns.colnames]).T

    print("Cropping images...")
    images_cropped = np.array([central_crop(img, args.crop_size) for img in images])

    print("Normalizing images...")
    low_p, high_p = 2, 98
    images_norm = np.zeros_like(images_cropped)
    for i in range(images_cropped.shape[0]):
        X_low = np.percentile(images_cropped[i], low_p, axis=(0, 1), keepdims=True)
        X_high = np.percentile(images_cropped[i], high_p, axis=(0, 1), keepdims=True)
        images_norm[i] = (images_cropped[i] - X_low) / (X_high - X_low + 1e-8)
        images_norm[i] = np.clip(images_norm[i], 0, 1)

    print("Splitting data...")
    
    scaler = StandardScaler()
    mag_pre = scaler.fit_transform(mag)
    
    
    print("Building model...")
    cnn_input = Input(shape=(args.crop_size, args.crop_size, 4))
    x = Conv2D(64, (7, 7), padding='same', activation='relu', kernel_initializer='he_normal')(cnn_input)
    x = AveragePooling2D(pool_size=(3, 3), padding='same')(x)
    x = Conv2D(64, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(x)
    x = Conv2D(192, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(x)
    x = AveragePooling2D(pool_size=(3, 3), strides=(2, 2), padding='same')(x)
    x = inception_module(x, filters=[64, 96, 128, 16, 32, 32]) 
    x = inception_module(x, filters=[64, 96, 128, 16, 32, 32]) 
    x = inception_module(x, filters=[128, 128, 192, 32, 96, 64])
    x = inception_module(x, filters=[128, 128, 192, 32, 96, 64])
    cnn_output = Flatten()(x)

    onn_input = Input(shape=(len(args.mag_columns),))
    y = Dense(512, activation='relu', kernel_initializer='he_normal')(onn_input)
    y = Dense(256, activation='relu', kernel_initializer='he_normal')(y)
    y = BatchNormalization()(y)
    y = Dropout(0.2)(y)
    y = Dense(128, activation='relu', kernel_initializer='he_normal')(y)
    y = Dense(64, activation='relu', kernel_initializer='he_normal')(y)

    merged = concatenate([cnn_output, y])
    z = Dense(1024, activation='relu')(merged)
    output = Dense(1, activation='linear')(z)

    model = Model(inputs=[cnn_input, onn_input], outputs=output)

    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(1e-3, decay_steps=10000, decay_rate=0.9)
    optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
    model.compile(optimizer=optimizer, loss=Huber(delta=0.0001), metrics=['mae', R2])


    
    model.load_weights(args.weights_path)
    print(f"Model weights loaded from {args.weights_path}")

    
    predictions = model.predict([images_norm, mag_pre])

    print("Saving predictions...")
    output_table = Table()
    for i, col in enumerate(args.additional_columns):
        output_table[col] = add_col[:, i]
    for i, col in enumerate(args.mag_columns):
        output_table[col] = mag[:, i]
    output_table['Z_phot'] = predictions.flatten()
    output_table.write(os.path.join(args.output_dir, "result_test.fits"), format='fits', overwrite=True)

    print("Workflow completed.")

# ---------- Argument Parsing ----------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Photometric Redshift Estimator (Deep Learning)")
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--image_column", required=True)
    parser.add_argument("--mag_columns", nargs='+', required=True)
    parser.add_argument("--additional_columns", nargs='+', default=['RAJ2000', 'DECJ2000'])
    parser.add_argument("--crop_size", type=int, default=36)
    parser.add_argument("--weights_path", required=True)
    args = parser.parse_args()
    main(args)
