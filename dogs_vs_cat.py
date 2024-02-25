# -*- coding: utf-8 -*-
"""Dogs vs cat

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1994xvestdDRt2zNnyU2lbnYzdgAZpZFU
"""

!wget --no-check-certificate https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip

import zipfile

local_zip = './cats_and_dogs_filtered.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall()

zip_ref.close()

import os

base_dir = 'cats_and_dogs_filtered'

print("Contents of base directory:")
print(os.listdir(base_dir))

print("\nContents of train directory:")
print(os.listdir(f'{base_dir}/train'))

print("\nContents of validation directory:")
print(os.listdir(f'{base_dir}/validation'))

import os

train_dir = os.path.join(base_dir,'train')
validation_dir= os.path.join(base_dir,'validation')

train_cats_dir = os.path.join(train_dir,'cats')
train_dogs_dir = os.path.join(train_dir, 'dogs')

validation_cats_dir = os.path.join(validation_dir,'cats')
validation_dogs_dir = os.path.join(validation_dir, 'dogs')

train_cat_fnames= os.listdir( train_cats_dir)
train_dog_fnames= os.listdir( train_dogs_dir)

print(train_cat_fnames[:10])
print(train_dog_fnames[:10])

print("total training cat images:",len(os.listdir( train_cats_dir)))
print("total training dogs images:", len(os.listdir( train_dogs_dir)))

print("total validation cats images", len(os.listdir( validation_cats_dir)))
print("total validation dogs images", len(os.listdir(validation_dogs_dir)))

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib.image as mping
import matplotlib.pyplot as plt

nrows = 4
ncols = 4

pic_index = 0

fig = plt.gcf()
fig.set_size_inches(ncols*4, nrows*4)
pic_index=0

next_cat_pix =[os.path.join(train_cats_dir,fname)
               for fname in train_cat_fnames[ pic_index-8:pic_index]]

next_dog_pix = [os.path.join(train_dogs_dir,fname)
                 for fname in train_dog_fnames[ pic_index-8:pic_index]]

for i, image_path in enumerate(next_cat_pix+next_dog_pix):
  sp=plt.subplot(nrows,ncols,i+1)
  sp.axix('off')

  img=mping.imread(img_path)
  plt.imshow(img)

plt.show()

import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16,(3,3), activation= 'relu', input_shape = (150,150,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32,(3,3),activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512,activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.summary()

from tensorflow.keras.optimizers import RMSprop

model.compile(optimizer=RMSprop(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator( rescale = 1.0/255.)
test_datagen = ImageDataGenerator( rescale  = 1.0/255.)

train_generator = train_datagen.flow_from_directory(train_dir,batch_size=20,class_mode='binary',
                                                    target_size=(150,150))

validation_generator = test_datagen.flow_from_directory(validation_dir,batch_size=20,class_mode='binary',
                                                        target_size=(150,150))

history =model.fit(
    train_generator,
    epochs=15,
    validation_data= validation_generator,
    verbose=2
)

import numpy as np
from google.colab import files
from tensorflow.keras.utils import load_img, img_to_array
uploaded =files.upload()
for fn in uploaded.keys():
  path = '/content/'+fn
  img =load_img(path,target_size =(150,150))
  x= img_to_array(img)
  x/= 255
  x= np.expand_dims(x,axis=0)
  images=np.vstack([x])
  classes = model.predict(images,batch_size=10)
  print(classes[0])

  if classes[0]>0.5:
    print(fn+"is a dog ")
  else :
    print(fn+ "is a cat")

