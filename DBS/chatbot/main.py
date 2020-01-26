import nltk 
from nltk import word_tokenize,sent_tokenize
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy 
import tflearn 
import tensorflow 
import json
import random 
import pickle
import boto3 
import speech_recognition as sr
from pygame import mixer

#Load into the json file 
with open("intents.json") as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?" ]
words = sorted(list(set(words))) # reomve duplicated elements 

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate (docs_x):

    bag = []
    wrds = [stemmer.stem(w.lower()) for w in doc]

    # counting which word exists 
    for w in words:
        if w in wrds :
            bag.append(1)
        else :
            bag.append(0)

    output_row = out_empty[:]
    output_row [labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training) 
output = numpy.array(output)

# Deep learning , predicting which tag and then gives the corresponsing response 
tensorflow.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8) # hiddent layer , 8 neurons
net = tflearn.fully_connected(net, 8) # hiddent layer , 8 neurons
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch = 1000, batch_size = 8, show_metric = True)



def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se :
                bag[i] = (1)

    return numpy.array(bag)


# Chatting with the bot function
def chat():
    print ("Start talking with the bot (type quit to stop) !")
    counter = 0 
    while True:

        inp = input ("You: ")
        if inp.lower() == "quit":
            break 

        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        print(responses)

        speak = reaction(++counter, responses)
        mixer.init()
        mixer.music.load(speak)
        mixer.music.play()


# Speech Recognition
def speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("You:")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
       # print("You said : {}".format(text))
        return str(text)
    except:
        print("Sorry could not recognize what you said")


# converting the text into a voice
def reaction(counter, responses):

    polly_client = boto3.Session(aws_access_key_id = 'AKIAJ6PM3AW4NEMBQPOA' , 
            aws_secret_access_key = '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' ,
            region_name = 'ap-southeast-1').client('polly')
    reaction = polly_client.synthesize_speech(VoiceId = 'Joanna', OutputFormat ='mp3', Text = random.choice(responses))


    speak = 'responses' + str(counter) + '.mp3'
    file = open(speak, 'wb')
    file.write(reaction['AudioStream'].read())
    file.close  

    return speak

chat()
 






