import pickle
from sklearn.preprocessing import MultiLabelBinarizer
import cv2
import numpy as np
import io
import base64
from PIL import Image
from keras.preprocessing.image import img_to_array
model_file = open('cnn_model(1).pkl', 'rb')
saved_classifier_model = pickle.load(model_file)

def convert_image(image_data):
    default_image_size = tuple((256, 256))
    image_size = 0
    try:
        image = Image.open(image_data)
        print(image)
        if image is not None :
            image = image.resize(default_image_size, Image.ANTIALIAS)   
            image_array = img_to_array(image)
            return np.expand_dims(image_array, axis=0), None
        else :
            return None, "Error loading image file"
    except Exception as e:
        return None, str(e)

def convert_image_to_array(image_dir):
        default_image_size = tuple((256, 256))
        image_size = 0
        try:
            image = cv2.imread(image_dir)
            if image is not None :
                image = cv2.resize(image, default_image_size)   
                return img_to_array(image)
            else :
                return np.array([])
        except Exception as e:
            print(f"Error : {e}")
            return None
class image:   
    # def predictclass(self,url):
    #     #header, image_data = url.split(';base64,')
    #     image_array= convert_image_to_array(url)
    #     print("loading model")
    #     print(image_array)
    #     # model_file = open('cnn_model(1).pkl', 'rb')
    #     # saved_classifier_model = pickle.load(model_file)
    #     # model_file = cnn_model.pkl"
    #     # saved_classifier_model = pickle.load(open(model_file,'rb'))
    #     prediction = saved_classifier_model.predict(image_array) 
    #     print("prediction is complete")
    #     label_binarizer = pickle.load(open('label_transform.pkl','rb'))
    #     print( label_binarizer.inverse_transform(prediction[0]))
    #     return "sucess" 
        
        #print(model)
    def predict(self,url):
        imar = convert_image_to_array(url)
        npimagelist = np.array([imar], dtype=np.float16) / 225.0
        label_binarizer=['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust',
 'Apple___healthy', 'Blueberry___healthy',
 'Cherry_(including_sour)___Powdery_mildew',
 'Cherry_(including_sour)___healthy',
 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
 'Corn_(maize)___healthy', 'Grape___Black_rot',
 'Grape___Esca_(Black_Measles)',
 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
 'Peach___healthy' ,'Pepper,_bell___Bacterial_spot',
 'Pepper,_bell___healthy' ,'Potato___Early_blight' ,'Potato___Late_blight',
 'Potato___healthy' ,'Raspberry___healthy' ,'Soybean___healthy',
 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch',
 'Strawberry___healthy' ,'Tomato___Bacterial_spot' ,'Tomato___Early_blight',
 'Tomato___Late_blight' ,'Tomato___Leaf_Mold' ,'Tomato___Septoria_leaf_spot',
 'Tomato___Spider_mites Two-spotted_spider_mite' ,'Tomato___Target_Spot',
 'Tomato___Tomato_Yellow_Leaf_Curl_Virus' ,'Tomato___Tomato_mosaic_virus',
 'Tomato___healthy']
        PREDICTEDCLASSES2 = saved_classifier_model.predict_classes(npimagelist) 
        #label=pickle.load(open('label_transform.pkl','rb'))
        #print(label.inverse_transform(PREDICTEDCLASSES2[0]))
        res= label_binarizer[int(PREDICTEDCLASSES2)]
        print(res)
        return str(res)

    
                   

    
