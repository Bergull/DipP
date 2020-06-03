from flask import Flask, redirect, url_for, request, render_template, jsonify, make_response

#from skimage import io
from io import BytesIO
import urllib.request

print("Loading packages")
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.applications.inception_resnet_v2 import preprocess_input
datagen = ImageDataGenerator(preprocessing_function = preprocess_input)

import numpy as np
#np.set_printoptions(suppress=True)
#model = load_model('K:\DP\WD\softmax_model_view.h5')

#ZRUSIT absolutni adresovani ve finalu
import os
os.chdir("K:/DP/webapp")
print("Loading model")
#model = load_model('K:/DP/WD/plan_no_weighting.h5')
model = load_model("model-53-0.9073.hdf5")
print("Model loaded")
import json
with open('dict.json', 'r') as jsfile:
    loaded = json.load(jsfile)
    #inverted the dictionary so that labels are keys
    class_names = {v: k for k, v in loaded.items()}




def predict_for_image(img):
    imaget = image.load_img(img, target_size=(256, 256))
    #print(type(img))
    imaget = image.img_to_array(imaget)
    imaget = np.expand_dims(imaget, axis=0)
    imaget = datagen.standardize(imaget) 
    #print(imaget)
    classes = model.predict_classes(imaget)      
    #return str(inverted_names.get(classes[0]))
    predicted_class = str(class_names.get(classes[0]))
    predicted_probs = model.predict_proba(imaget).tolist()[0]
    #print(predicted_probs)
    #print(class_names)
    #print(inverted_names)
    dictionary = {}
    for label in class_names:
        #print(class_names.get(label))
        #print(predicted_probs[label])
        class_name = class_names.get(label)
        dictionary.update({class_name : predicted_probs[label]})
        
    #dictionary = dict(zip(inverted_names, predicted_probs))
    #print("dictionary")
    #print(dict(zip(inverted_names, predicted_probs)))
    #print(dictionary)      
    return dictionary


UPLOAD_FOLDER = './files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
   return render_template("createoffer.html")

@app.route('/success/')
def success(label):
   return label

from db import init_db, db_session
from models.OfferModel import OfferModel
from models.ImagesModel import ImagesModel
from io import BytesIO
from werkzeug.utils import secure_filename

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
@app.route('/listings/')
def listings():
    offersList = []
    init_db()
    #imgresult = Imagesmod.query.first()
    #imgresult.image
    #imgretrieved = image.load_img(BytesIO(imgresult.image))
    #get all ads
    results = OfferModel.query.all()
    #for each ad get all images belonging to it and add as List
    for result in results:
        imagesList = db_session.query(ImagesModel).join(OfferModel).filter(OfferModel.id == result.id)
        result.imagesList = list(imagesList)
        offersList.append(result)
    print(offersList)
    return render_template("listings.html", offersList = offersList)

@app.route('/receive/', methods = ['POST'])
def receive():
    print("receive triggered")
    if request.method == 'POST':
        #import pprint
        #str = pprint.pformat(request.environ, depth=5)
        #print(str)
        
        files = request.files.to_dict()
        #print(files)
        #print(type(files))
        #print(len(files))
        predictionDict = {}
        predClass = {}
        THRESHOLD = 0.9
        for img in files:
            print(type(files[img]))
            print(files[img].filename)
            print("test for predict")
            print()
            predictiontest = predict_for_image(files[img])
            #print(predictiontest)
            
        # check jestli ma file povolenej extension pro kazdej file filename, kdyz jo tak ho ulozit se secure_filename a ulozit do db
            # if(allowed_file(files[img].filename)):
            #     filename = secure_filename(files[img].filename)
            #     print(filename)
            #     files[img].stream.seek(0)
            #     files[img].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            
            predictionDict.update({ img : predictiontest})
            predictedClasses = []
            #in case of multiclass
            for pred in predictiontest:
                if(predictiontest[pred] >= THRESHOLD):
                    print(predictiontest[pred])
                    predictedClasses.append(pred)
                    print(predictedClasses)
                    
                    
                else:
                    print("else triggered")
                    #predClass.update({ img : None})
            predClass.update( {img : predictedClasses})
            print(predClass)
            print("predictiondict")
            print(predictionDict)
        
        #return redirect(url_for('success', label = classes))
        #data = { 'predicted_class' : predicted_class, "predicted_probs" : predicted_probs,  "cnames" : inverted_names}
        #print(predictionDict)
        
        
        
        data = {'message': 'lenght of files' + str(len(files)), 'code': 'SUCCESS', 'predictions' : predictionDict, 
                'predClasses' : predClass}
        return make_response(jsonify(data), 201)
        
@app.route('/submit/')
def submit():
    return render_template("submit.html")    
    
@app.route('/postoffer/', methods = ["POST"])
def post_offer():
    print("Post offer triggered")
    if request.method == 'POST':
        #dict for better manipulation?
        files = request.files.to_dict()
        #print(request.form["adresa"])
        address = request.form["address"]
        name = request.form["name"]
        print("address")
        print(address)
        print("name")
        print(name)
        init_db()
        offer = OfferModel(name = name, email = address)
        db_session.add(offer)
        db_session.flush()
        #result = OfferModel.query.filter(OfferModel.name == name).first()
        resultID = offer.id
        db_session.commit()
        predictions = batch_predict(list(files.values()))
        print("pred 0")
        print(predictions[0])
        predictedClasses = pred_classes(predictions, 0.9)
        print(predictedClasses)
        finalClasspredDict = {}
        finalProbsDict = {}
        for i,file in enumerate(files):
            print(file)
            print(files[file].filename)
            #print(vars(file))
            if(allowed_file(files[file].filename)):
                fileobj = files[file]
                filename = secure_filename(fileobj.filename)
                finalClasspredDict.update({ file : predictedClasses[i]})
                finalProbsDict.update({ file : predictions[i]})
                
                #print(filename)
                fileobj.stream.seek(0)
                fileobj.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if (len(predictedClasses[i])>0):
                    imgobj = ImagesModel(predictedClasses[i][0], resultID, filename)
                else:
                    imgobj = ImagesModel("", resultID, filename)    
                db_session.add(imgobj)
                db_session.commit()
        print(finalProbsDict)
        print(finalClasspredDict)        
    #return render_template("listings.html")
        data = {"cool" : "cool", "predClasses" : finalClasspredDict, "predprobs" : finalProbsDict, "redirect" : resultID }
        return make_response(jsonify(data), 201)
#hodit sem ziskany predikce, pro ne predikovat classy na zaklade thresholdu, vratit list nebo dict ziskanejch class
def pred_classes(pred_probs, threshold):
    print("pred_classes debug")
    predictedClassesDict = []
    for pred in pred_probs:
        individualPredClass = []
        for label in pred:
            if(pred[label] >= threshold):
                #print(predictiontest[pred])
                individualPredClass.append(label)
                #print(predictedClasses)
            
            
        #else:
            #print("else triggered")
            #predClass.update({ img : None})
        predictedClassesDict.append(individualPredClass)
    # finalDict = {}
    # for i,file in enumerate(files):
    #     finalDict.update({ file : predictedClassesDict[i]})
    # print(finalDict)
    print(predictedClassesDict)
    return predictedClassesDict    


def batch_predict(files):
    #print(files)
    print("batch predict debugs")
    print(files[0])
    type(files[0])
    print("file len in batch")
    print(len(files))
    batch = np.zeros((len(files), 256, 256, 3))
    #batch.astype(np.float64)
    #print(batch)
    print(batch[0])
    for i, img in enumerate(files):
        loadedimg = image.load_img(img, target_size=(256, 256))
        batch[i,] = loadedimg
    batch = datagen.standardize(batch) 
    
    predictions = model.predict_proba(batch, batch_size=32) #.tolist()[0]
    finalPreds = []
    ## udelat nice looking list of prediction dictionaries to make working with it easier later. need np float 64 pro json
    for prediction in predictions:
        #print(prediction)
        preddictionary = {}
        #for json serialization
        #f64pred = prediction.astype(np.float64)
        print("pred dtype")
        print(prediction.dtype) 
        for label in class_names:
        #print(class_names.get(label))
        #print(predicted_probs[label])
            class_name = class_names.get(label)
            preddictionary.update({class_name : prediction[label].astype(np.float64)})
        finalPreds.append(preddictionary)
       
    return finalPreds
    # filenamedict = {}
    # for file in files:
    #     for pred in finalPreds:
    #         file_name = file.filename
    #         filenamedict.upadte({file_name : pred})
    # return filenamedict    


from flask import send_from_directory
@app.route('/files/<path:filename>')
def download_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route("/offer/<offerID>")
def offer(offerID):
    offersList = []
    init_db()
    #imgresult = Imagesmod.query.first()
    #imgresult.image
    #imgretrieved = image.load_img(BytesIO(imgresult.image))
    #get all ads
    result = OfferModel.query.filter(OfferModel.id == offerID).first()
    #for each ad get all images belonging to it and add as List
    imageList = list(db_session.query(ImagesModel).join(OfferModel).filter(OfferModel.id == result.id)) 
    result.imageList = imageList
    return render_template("offer.html",  result = result)


@app.route("/createoffer/")
def createoffer():
    return render_template("createoffer.html")  


#vypnout debug pred deploys, use_reloader false pro notebook a ide, nacist model odtud ve finalni verzi
if __name__ == '__main__':
   #model = load_model('K:/DP/WD/plan_no_weighting.h5')
   app.run(debug = True, use_reloader = False)

