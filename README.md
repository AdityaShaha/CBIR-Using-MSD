# CBIR-Using-MSD
The project is an attempt to implement the paper Content Based Image Retrieval using Micro structure Descriptors by Guang-Hai Liu et all. in Python

## Micro Structure Descriptors

Microstructures can be defined in **two phases**
- In the pre-attentive stage, primitive features such as colors and orientation are extracted effortlessly and registered in special modules of feature maps
- In the attentive stage, focal attention is required to recombine the separate features to form
objects

## Algorithm :

- Covert RGB color space to HSV color space for detecting the micro-structure features.
- In the HSV color space, quantize the color image into 72 colors and detect the edge orientation
- The micro-structures are defined in the edge orientation image, and the MSD is built based on the underlying colors in micro-structures
- The MSD is used to represent the image features for image retrieval

## Dataset used for testing the algorithm

Dataset used for testing the algorithm is Corel-10k dataset. Corel-10k dataset  contains 100 categories,and there are 10,000 images from diverse contents such as sunset, beach, flower, building, car, horses, mountains, fish, food, door, etc. Each category contains 100 images of size 192×128 or 128×192 in the JPEG format.  Corel-5K dataset consists of the first 5000 images, and Corel-10K dataset consists of the 10,000 images. The dataset can be downloaded from [Corel-10k](http://www.ci.gxnu.edu.cn/cbir/Dataset.aspx)