from __future__ \
import unicode_literals
import youtube_dl
import datetime
import threading
import requests


directory_path = '/home/pi/files/'


task_tab = []
threads = []


class zadanie:
    def __init__(self, link, filename):

        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # time when task was started
        self.link = link # link to file which is downloaded
        self.filename = filename # name of file in proccess
        self.status = '0.0' # amount of downloaded size in percents
        self.finish = False # flag which determiates if task is done or not

        threads.append(threading.Thread(target=self.download, args=())) # define new thread and write this object to threads table
        i = len(threads) # get lenght of threads tab
        threads[i - 1].daemon = True  # Daemonize thread
        threads[i - 1].start() # starting this thread

    def show_tasks(self):
        # function which return info about object(task)
        info = str(self.filename) + "------------------------------------------------\n" + str(
            self.start_time) + "  " + str(self.status) + " % \n" + "------------------------------------------------\n"

        return info

    def download(self):
        # ---------------------------------
        filename = self.filename.rstrip()
        link = self.link
        list = link.split('.') # trying to extract extension from link
        n = len(list)
        exten = list[n - 1]
        exten = exten.rstrip()
        exten = exten[:3]
        # ------------------------------------------------------
        if list[1] == 'youtube' or list[0] == 'https://youtu': # determinates if file is youtube file or usually file

            ydl_opts = {

                'format': 'bestaudio/best',
                'extractaudio': True, # value determinate parametrs of ydl library
                'audioformat': "mp3",
                'outtmpl': '/home/pi/files/Music/%(title)s.mp3',
                'noplaylist': True,
                'nooverwrites': True,
            }



            with youtube_dl.YoutubeDL(ydl_opts) as ydl:# this starting downloading mp3 file


                ydl.download([link])# maybe this starti it , this above create file


            self.status = 100 # write paramters
            self.finish = True

        else:

            filename = filename + '.' + exten # add extesnion to name of file

            with open(directory_path + filename, 'wb') as f: # create file

                print(filename)
                print(link)

                response = requests.get(link, stream=True) #get response from link
                total = response.headers.get('content-length')

                if total is None: #no header no stream
                    f.write(response.content)

                else:
                    # download file block
                    downloaded = 0
                    total = int(total)

                    for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                        downloaded += len(data)
                        f.write(data)
                        prog = (downloaded / total) * 100

                        self.status = "%.2f" % prog # updateing status parametr

            self.finish = True
