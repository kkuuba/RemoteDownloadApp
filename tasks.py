from __future__ import unicode_literals
import youtube_dl
import datetime
import threading
import requests
import re
threads = []


class Task:
    def __init__(self, link, filename, extension, download_dir):
        """
        Create task download object. This automatically starts downloading file in new thread.

        :param link: link to target file
        :param filename: name of file we want ot save in remote device
        :param download_dir: path to directory where target file will be saved
        """
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # time when task was started
        self.link = link  # link to file which is downloaded
        self.filename = filename  # name of file in process
        self.status = '0.0'  # amount of downloaded size in percents
        self.finish = False  # flag which determinate if task is done
        self.download_dir = download_dir
        self.extension = extension

        threads.append(threading.Thread(target=self.start_download_task, args=()))
        # ^^define new thread and write this object to threads table

        i = len(threads)  # get length of threads tab
        threads[i - 1].daemon = True  # Demonize thread
        threads[i - 1].start()  # starting this thread

    def show_task(self):
        """
        Give information about filename, start time and download status of task object.

        :return: string containing actual progress of task object
        """
        info = str(self.filename) + "------------------------------------------------\n" + str(
            self.start_time) + "  " + str(self.status) + " % \n" + "------------------------------------------------\n"

        return info

    def check_task_type(self):
        """
        Verify if it's youtube task or regular file download task.

        :return: True or False
        """
        if re.match(r'\w+:..((www.youtube.)|(youtu.be.)).+', self.link):

            return True
        else:
            return False

    def download_youtube_mp3(self):
        """
        Download youtube mp3 file.

        :return: None
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,  # value determinate parametrs of ydl library
            'audioformat': "mp3",
            'outtmpl': self.download_dir + '%(title)s.mp3',
            'noplaylist': True,
            'nooverwrites': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:  # this starting downloading mp3 file

            ydl.download([self.link])  # maybe this starti it , this above create file

        self.status = 100  # write paramters
        self.finish = True

    def download_regular_file(self):
        """
        Download regular file.

        :return: None
        """
        filename = self.filename + '.' + self.extension  # add extesnion to name of file

        with open(self.download_dir + filename, 'wb') as f:  # create file

            print(filename)
            print(self.link)

            response = requests.get(self.link, stream=True)  # get response from link
            total = response.headers.get('content-length')

            if total is None:  # no header no stream
                f.write(response.content)

            else:
                # download file block
                downloaded = 0
                total = int(total)

                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    prog = (downloaded / total) * 100

                    self.status = "%.2f" % prog  # updateing status parametr

    def start_download_task(self):
        """
        Check download task type and start downloading via proper interface.

        :return: None
        """
        if self.check_task_type():
            self.download_youtube_mp3()
        else:
            self.download_regular_file()
            self.finish = True
