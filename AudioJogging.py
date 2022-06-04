from pydub import AudioSegment
import os
import pandas as pd

y= 0
var=0
x= 0
mix=0
time = 0
d = {}
key = 0

#df = pd.read_excel("D:\Testaudio\Jogplan.xlsx")

#df = pd.DataFrame(df)
#print(df)

# Variable for running
name=str(input("For who->"))
cw=int(input("Warmup minute->"))
rt=int(input("Run time minute->"))
sq=int(input("How many sequence->"))

file_list = os.listdir("D:/Testaudio/"+name)
print("D:/Testaudio/"+name+"/"+str(file_list[y]))

# Set sequence if necessary, the key is reused later
for i in range(sq):
    key= key+1

    cr= int(input("run second->"))
    cb= int(input("Break second->"))
    d ["cr"+str(key)]= cr
    d ["cb"+str(key)]= cb

print (d)
# all the audio necessary
countdown= AudioSegment.from_mp3("D:/Testaudio/Sound/Countdown.mp3")
complete= AudioSegment.from_mp3("D:/Testaudio/Sound/complete.mp3")
bellsound= AudioSegment.from_mp3("D:/Testaudio/Sound/BellSound.mp3")
Countmin = AudioSegment.from_mp3("D:/Testaudio/Sound/Shrek_Jog.mp3")
Countmin = Countmin.apply_gain(+20.5)
countdown =countdown[10000:21000]
bellsound = bellsound[106000:107500]
bellsound = bellsound.apply_gain(+20.5)
#Skip warmup
time = (cw)*60000

#loop all the Playlist audio
while x -(60*2) < (cw + rt)*60 :
    try:
        song= AudioSegment.from_mp3("D:/Testaudio/"+name+"/"+str(file_list[y]))
        mix = mix + song
        x= len(mix)/1000
        print(x-500)
        print((cw + rt)*60)
        y= y+1
    except :
        y= 0
        print("Loop")

# End the Warmup
mix = mix.overlay(countdown, position= time-10000, gain_during_overlay=-10)
mix = mix.overlay(complete, position=(cw + rt)*60000 , gain_during_overlay=-10)

#loop all the audio bite for the running sequence
while time < (cw + rt)*60000 :
    try:
        timestart=time
        runmin =1
        timestart2 =time
        var=var+1
        print("cr"+str(var))
        mix = mix.overlay(countdown, position= (time + d["cr"+str(var)]*1000) -10000, gain_during_overlay=-10)
        time =(time + d["cr"+str(var)]*1000)
        
        # Extra loop for the bell every minute during run time
        while timestart  < time  : 
                if runmin % 6 == 0 :
                    print(timestart)
                    mix = mix.overlay(Countmin, position= timestart, gain_during_overlay=-10)
                    timestart = timestart + 60000
                    runmin = 2

                else:
                    mix = mix.overlay(bellsound, position= timestart )
                    timestart = timestart + 60000
                    runmin = runmin+1
                    print("good-"+str(runmin))


        print("cb"+str(var))
        mix = mix.overlay(countdown, position= (time + d["cb"+str(var)]*1000) -10000, gain_during_overlay=-10)
        time =(time + d["cb"+str(var)]*1000)
    except : 
        var = 0
        print("Loop")


file_handle = mix.export("D:/Testaudio/"+name+"_Jog.mp3", format="mp3")
