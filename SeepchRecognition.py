from pydub import AudioSegment
from pydub.utils import make_chunks
import speech_recognition as sr
import json
import os

################################## replace with your files
audio_file="20200810_meeting.wav" #to be translated file
path = "20200810_meeting"  # new folds to put all chunks
##################################

if not os.path.exists(path):
    os.makedirs(path)


text_file = open("transcript.txt","w") #the results file

# recognize speech using Google Cloud Speech
###################################replace with your files
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""cbd00b2d3e72.json"""
##################################

with open(GOOGLE_CLOUD_SPEECH_CREDENTIALS) as f:
    d = f.read()

current_time_h = 0;
current_time_m = 0;
current_time_s = 0;
end_time_h = 0;
end_time_m = 0;
wnd_time_s = 0;
    


myaudio = AudioSegment.from_file(audio_file , "wav") 
chunk_length_ms = 30000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

#Export all of the individual chunks as wav files
for i, chunk in enumerate(chunks):
    chunk_name = os.path.join(path,"chunk{0}.wav".format(i))
    print ("exporting", chunk_name)
    chunk.export(path+chunk_name, format="wav")
    

chunks=[ i for i in os.listdir(path) if i.endswith(".wav")]   


for i, chunk in enumerate(chunks):
    print(i)
    if(current_time_s>=60):
        end_time_s = 30;
        end_time_m = current_time_m + 1
        if(current_time_m >= 60):
            end_time_m = 0;
            end_time_h = 1;
    else:
        end_time_s =current_time_s+30 #when current second is 0
        if(end_time_s == 60):
            end_time_m = end_time_m+1;
            end_time_s = 0;
    r = sr.Recognizer()
    with sr.AudioFile(os.path.join(path,chunk)) as source:
        audio = r.record(source)
    try:
        text_file.write("{}:{}:{}----{}:{}:{}\n".format(current_time_h,current_time_m,current_time_s,
                                          end_time_h,end_time_m,end_time_s))
        text_file.write(r.recognize_google_cloud(audio, credentials_json=d))
        text_file.write('\n')
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
    current_time_s = end_time_s
    current_time_m = end_time_m
    current_time_h = end_time_h




text_file.close()
