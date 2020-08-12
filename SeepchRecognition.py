from pydub import AudioSegment
from pydub.utils import make_chunks
import speech_recognition as sr
import json


text_file = open("transcript.txt","w")
# recognize speech using Google Cloud Speech
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""../cbd00b2d3e72.json"""
with open(GOOGLE_CLOUD_SPEECH_CREDENTIALS) as f:
    d = f.read()

current_time_h = 0;
current_time_m = 0;
current_time_s = 0;
end_time_h = 0;
end_time_m = 0;
wnd_time_s = 0;
    
path = ""


myaudio = AudioSegment.from_file("Eri_Pres.wav" , "wav") 
chunk_length_ms = 30000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

#Export all of the individual chunks as wav files

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
    try:
        text_file.write("{}:{}:{}----{}:{}:{}\n".format(current_time_h,current_time_m,current_time_s,
                                          end_time_h,end_time_m,end_time_s))
        text_file.write(r.recognize_google_cloud(chunk, credentials_json=d))
        text_file.write('\n')
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
    current_time_s = end_time_s
    current_time_m = end_time_m
    current_time_h = end_time_h




text_file.close()
