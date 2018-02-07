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

## Repository Structure
- 215.jpg : It is an image from `Corel-10k dataset` used for visualization of the histogram in `Image Retieval based on Micro Structure Description.ipynb`<br/>
- Image Retieval based on Micro Structure Description.ipynb : It is a Jupyter notebook used for the explaination of code for extracting microstructure descriptors from the input image `215.jpg`.</br>
- Image Retieval based on Micro Structure Description - Retrieval Phase.ipynb : It is a Jupyter notebook used for the explaination of code for retrieval of image from the MongoDB database.</br>
- MSD.py : The python code is responsible for extracting the features from the images and seeding it into the MongoDB database.</br>
- Retrieval.py : The python code is responsible for retrieving the similar images from the database by taking the number(e.g. `13.jpg`) from the database.</br>
- `dump>test_database`: The folder contains the actual dump of the seeded images in the database which can be directly restored in the local database for checking the results.The 72 bin feature-vector for each image was extracted.

## Restoring the mongodump
- Open the terminal in Linux or Command Line in windows
- For windows make sure that mongo is in the environment variables. if not follow this [tutorial]('https://docs.mongodb.com/tutorials/install-mongodb-on-windows/')
- In the repository directory type
```
cd dump
cd test_database
mongorestore --db database_name .
```
## Dataset used for testing the algorithm

Dataset used for testing the algorithm is Corel-10k dataset. Corel-10k dataset  contains 100 categories,and there are 10,000 images from diverse contents such as sunset, beach, flower, building, car, horses, mountains, fish, food, door, etc. Each category contains 100 images of size 192×128 or 128×192 in the JPEG format.  Corel-5K dataset consists of the first 5000 images, and Corel-10K dataset consists of the 10,000 images. The dataset can be downloaded from [Corel-10k](http://www.ci.gxnu.edu.cn/cbir/Dataset.aspx)