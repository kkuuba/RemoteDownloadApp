from __future__ import unicode_literals
import youtube_dl
import datetime
import threading
import requests
import re

threads = []  # all threads list
tasks_list = []  # all tasks list


def start_received_request_action(data):
    """
    Main function which extract task type and start proper action. Then return response.

    :param data:
    :return: response string
    """
    if data["action"] == "check_status":
        dictionary = get_status_of_all_tasks()
        if dictionary:
            return get_status_of_all_tasks()
        else:
            return {"response": "no task in process"}
    elif data["action"] == "download_request":
        tasks_list.append(Task(data))
        return tasks_list[-1].response
    else:
        return {"response": "invalid request action data"}


def get_status_of_all_tasks():
    """
    Function which get information about all actual processed tasks.

    :return: dictionary containing information about all actual processed tasks
    """
    response = dict()
    for task in tasks_list:
        response.update(task.get_task_data())

    return response


class Task(object):
    def __init__(self, data):
        """
        Create task download object. This automatically starts downloading file in new thread.

        :param data: received dict with all task data
        """

        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # time when task was started
        self.link = ""
        self.filename = ""
        self.status = '0.0'
        self.finish = False  # flag which determinate if task is done
        self.download_dir = "/"
        self.extension = ""
        self.rcv_data = data
        self.response = ""

        self._extract_task_info_from_rcvdata()
        threads.append(threading.Thread(target=self.start_download_task, args=()))
        # ^^define new thread and write this object to threads table

        i = len(threads)
        threads[i - 1].daemon = True
        threads[i - 1].start()
        self.response = {"response": "download task started"}

    def get_task_data(self):
        """
        Give information about filename, start time and download status of task object.

        :return: json object with all information about task object
        """
        data = {self.filename: {"extension": self.extension,
                                "download_dir": self.download_dir, "status": self.status,
                                "start_time": self.start_time}}

        return data

    def _extract_task_info_from_rcvdata(self):

        self.link = self.rcv_data["link"]
        self.filename = self.rcv_data["filename"]
        self.extension = self.rcv_data["extension"]
        self.download_dir = self.rcv_data["download_dir"]

    def _check_task_type(self):
        """
        Verify if it's youtube task or regular file download task.

        :return: True or False
        """
        if re.match(r'\w+:..((www.youtube.)|(youtu.be.)).+', self.link):

            return True
        else:
            return False

    def _download_youtube_mp3(self):
        """
        Download youtube mp3 file.

        :return: None
        """
        ydl_opts = {
            # values to set yt_dl library
            'format': 'bestaudio/best',
            'extractaudio': True,  # value determinate parametrs of ydl library
            'audioformat': "mp3",
            'outtmpl': self.download_dir + '%(title)s.mp3',
            'noplaylist': True,
            'nooverwrites': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:  # create mp3 file

            ydl.download([self.link])
        # TO DO make status counter in this section
        self.status = 100  # set status value to 100 %
        self.finish = True

    def _download_regular_file(self):
        """
        Download regular file.

        :return: None
        """
        filename = self.filename + '.' + self.extension

        with open(self.download_dir + filename, 'wb') as f:  # create file with properer extension

            print(filename)
            print(self.link)

            response = requests.get(self.link, stream=True)  # get response from link which contain size of file
            total = response.headers.get('content-length')

            if total is None:  # no header no stream started
                f.write(response.content)

            else:
                downloaded = 0
                total = int(total)

                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    progress = (downloaded / total) * 100

                    self.status = "%.2f" % progress  # update percent value od downloaded file

    def start_download_task(self):
        """
        Check download task type and start downloading via proper interface.

        :return: None
        """
        if self._check_task_type():
            self._download_youtube_mp3()
        else:
            self._download_regular_file()
            self.finish = True
