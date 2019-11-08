from tasks import task_tab
from tasks import zadanie


def check_tasks():
    for i in range(len(task_tab)):  # function check if all tasks all finish and retunr flag

        if not task_tab[i].finish:
            return False

    return True


def task_parser(dane):
    # if dane == "open_gate\n":

    if dane == "status\n":  # status block

        feedback = ""

        for i in range(len(task_tab)):

            if check_tasks():  # if all tasks done delete all objecs from tab

                del task_tab[i]

            else:

                feedback = feedback + task_tab[i].show_tasks()  # show every task info

        if feedback == "":
            return 'Currently no tasks in process\n'  # give feedback
        else:
            return feedback

    else:  # download block

        try:

            linia = dane.split("**")  # split data from string
            task_tab.append(zadanie(linia[0], linia[1]))  # create new task
            return "Task started\n"

        except:

            return 'bad format of task\nEnter task:\n'  # feedback
