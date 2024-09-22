import os
import threading
import time
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox

from tkinter import ttk
from ttkthemes import themed_tk as tk


from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
#Return a list of themes
root.get_themes() 
#sets an available theme
root.set_theme("radiance")


statusbar = ttk.Label(root,text='welcome to melody',relief=SUNKEN,anchor=W,font = 'Times 10 italic')
statusbar.pack(side=BOTTOM ,fill=X)

#menubar
menubar = Menu(root)
root.config(menu=menubar)

#submenu

submenu = Menu(menubar,tearoff=0)

playlist = []


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index=0
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    index += 1


menubar.add_cascade(label='File',menu=submenu)
submenu.add_command(label='open',command=browse_file)
submenu.add_command(label='Exit',command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About melody','this music player is build using python')

submenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='HELP',menu=submenu)
submenu.add_cascade(label='About us',command = about_us)


mixer.init()

root.title('Melody')
root.iconbitmap(r'images/melody.ico')


leftframe = Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addbtn = ttk.Button(leftframe,text="+ Add",command=browse_file)
addbtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delbtn = ttk.Button(leftframe,text= ' -Del',command=del_song)
delbtn.pack(side=LEFT)


rightframe = Frame(root)
rightframe.pack(pady=30)


topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe,text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe,text = 'current time : --:--',relief = GROOVE)
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splittext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused

    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs = divmod(current_time,60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            currenttimelabel['text'] = "current time"+'-'+timeformat
            time.sleep(1)
            current_time+=1

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "playing music"+'-'+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('file not found','melody could not find')

def stop_music():
    mixer.music.stop()
    statusbar['text'] = 'Music stopped'


paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "music paused"

def rewind_music():
    play_music()
    statusbar['text'] = "music reviend"


def set_vol(val):
    volumn = float(val) /100
    mixer.music.set_volume(volumn)

    muted = FALSE

    def mute_music():
        global muted
        if muted:
            mixer.music.set_volumn(0.7)
            volumnBtn.configure(image=volumnphoto)
            scale.set(70)
            muted = FALSE
        else:
            mixer.music.set_volumn(0)
            volumnBtn.configure(image=mutephoto)
            scale.set(0)
            muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=30,padx=30)

playphoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe,image=playphoto,command=play_music)
playBtn.grid(row=0,column=0,padx=10)


stopphoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe,image=stopphoto,command=stop_music)
stopBtn.grid(row=0,column=1,padx=10)


pausephoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe,image=pausephoto,command=pause_music)
pauseBtn.grid(row=0,column=2,padx=10)


#bottom frame for volumn ,revind,mute etc

bottomframe = Frame(rightframe)
bottomframe.pack()

rewindphoto = PhotoImage(file='images/mute.png')
rewindBtn = ttk.Button(bottomframe,image=rewindphoto,command=rewind_music)
rewindBtn.grid(row=0,column=0)



mutephoto = PhotoImage(file='images/mute.png')
volumnphoto = PhotoImage(file='images/volume.png')
volumnBtn = ttk.Button(bottomframe,image=volumnphoto,command=play_music)
volumnBtn.grid(row=0,column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


            


            

    


























    





















