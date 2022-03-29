**BeMyVision**

Image Captioning system using CNN LSTM

**Introduction**

Image processing is a growing subject of study. Images come in a variety of file formats and represent a variety of things, including places, persons, scientific, astrological, and other topics. An image is made up of a series of pixels that are arranged in rows and columns. These photos
are taken, processed, and saved for a variety of purposes. It is simple for ordinary individuals to identify and interpret generic images, but it is more challenging for the blind and physically disabled. Unfortunately, such needy people have no prior method or interface through which to
communicate with the rest of the world. People who are blind or visually impaired are sometimes neglected by society, so there is always a need to assist them, Mrunmayee Patil et al[1]. Recent computer vision research has produced excellent achievements in autonomously
describing images using natural language. To create a multilingual captioning system, most of these systems are generated in a single language, requiring using numerous language-specific models. We suggest a fairly basic way for creating a single uniform model across multiple
platforms artificial intelligence used to govern the language. It is a cost-effective and efficient approach for visually impaired people to hear text graphics in their own languages. Text-to-speech conversion is a technique that scans and reads any language letters and numbers in an image, then translates it into any desired language and outputs the translated text as audio.

**Prerequisites**

    Python 3
    Jupyter Notebook
    Tensorflow (tensorflow.org/install/)
    Keras (pypi.org/project/keras/)
    NumPy (scipy.org/install/)
    OpenCV (scipy.org/install/)
    Pandas (scipy.org/install/)
    Matplotlib (scipy.org/install/)
    
**Dataset**

    Dataset name:
      Flicker 8k [6] (https://www.kaggle.com/ming666/flicker8k-dataset)
    Dataset size:
      o 1 GB
      o A total of 8092 images in JPEG format with different shapes and sizes. Of which 6000
      of them will be used for training, 1000 for testing and 1000 for development.  
      
**Usage**

You can train the model on your local system using Jupyter Notebook or you can use Kaggle or google colab.
Download the dataset on your system or upload it on your google drive (if using colab. Change the path from the code where needed.
Train the model and save it in your system in HDF5 format.
Load the trained model and perform evaluations.
