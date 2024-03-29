from pydoc import describe
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.applications.xception import Xception
from keras.models import load_model
from pickle import load
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from gramformer import Gramformer
import argparse

## ap = argparse.ArgumentParser()
# ap.add_argument('-i', '--image', required=True, help="Image Path")#args = vars(ap.parse_args())
# img_path = args['image']
# img_path = '/content/drive/MyDrive/ML/Flicker8k_Dataset/111537222_07e56d5a30.jpg'

def extract_features(filename, model):
        try:
            image = Image.open(filename)
            
        except:
            print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
        image = image.resize((299,299))
        image = np.array(image)
        # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3]
        image = np.expand_dims(image, axis=0)
        image = image/127.5
        image = image - 1.0
        feature = model.predict(image)
        return feature

def word_for_id(integer, tokenizer):
 for word, index in tokenizer.word_index.items():
     if index == integer:
         return word
 return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo,sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    return in_text

def caption(imgpath):
    #path = 'Flicker8k_Dataset/111537222_07e56d5a30.jpg'
    max_length = 32
    tokenizer = load(open("/home/saba/FYP/tokenizer.p","rb"))
    model = load_model('/home/saba/FYP/model_15.h5')
    xception_model = Xception(include_top=False, pooling="avg")

    photo = extract_features(imgpath, xception_model)
    # gf = Gramformer(models = 1, use_gpu=False)
    description = generate_desc(model, tokenizer, photo, max_length)
    new_desc= description.split("start")
    # res = gf.correct(new_desc)
    new_desc=' '.join(new_desc)
    str2=new_desc.split("end")
    str2="".join(str2)
    # print(description)
    # plt.imshow(img)
    return str2


