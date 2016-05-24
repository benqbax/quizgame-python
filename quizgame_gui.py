# Skapad av: Ben Forsrup CMETE1
# Programmeringsteknik DD1315
# 2016-05-17
# Reviderad 2016-05-23

import tkinter as tk
import os
from tkinter import messagebox
import operator
from tabulate import tabulate
import csv

# Olika fonts som använts i programmet
TITLE_FONT = ("Helvetica", 18, "bold")
QUESTION_FONT = ("Helvetica", 14, "bold")
MENUOPTION_FONT = ("Helvetica", 10, "bold")


# en del strukturella idéer togs från
# http://stackoverflow.com/questions/24885827/python-tkinter-how-can-i-ensure-only-one-child-window-is-created-onclick-and-no

class Question(object):
    """
    Frågeklass. Har tre parametrar
    """

    def __init__(self, question, answers, right):
        """
        Skapar en ny fråga
        :param question: Frågan - sträng
        :param answers: 3 alternativ - lista med stränger
        :param right: rätt svar till frågan - sträng
        :return:
        """

        if not isinstance(question, str):
            raise TypeError
            # om frågan inte är en sträng sätts den till nedan
            self.question = "A question"

        else:
            self.question = question

        if not isinstance(answers, list):
            raise TypeError
            # om answers inte är en lista sätts den till nedan
            self.answers = ["1", "2", "3"]
        else:
            self.answers = answers

        if not any(alt == right for alt in answers):
            raise TypeError
            # om right är ej rätt så sätts de till första av alten
            self.right = answers[0]

        else:
            self.right = right

    def get_question(self):
        """
        :return: Returnerar frågan i form av en sträng
        """
        return self.question

    def get_answers(self):
        """
        :return: Returnerar en lista av alternativen
        """
        return [self.answers[0], self.answers[1], self.answers[2]]

    def get_right(self):
        """
        :return: Returnerar det rätta svaret
        """
        return self.right

    def __getitem__(self, key):
        """
        Ser till att man kan en attribut av frågeobjektet.
        :param key: Keyn, så du kan skriva question[0] exempelvis - int
        :return: Beroende på key returneras frågan, alten eller rätt svar
        """
        if key == 0:
            return self.question
        elif key == 1:
            return self.answers
        elif key == 2:
            return self.right
        else:
            raise IndexError


class MainApplication(tk.Frame):
    def __init__(self, master, listOfQuestions):
        """
        Skapar nytt frame.
        :param master: tkinter objektet
        :param listOfQuestions: listan på frågor
        :return:
        """

        # avsedd för testande
        if not isinstance(listOfQuestions, list):
            raise TypeError

        if not any(isinstance(question, Question) for question in listOfQuestions):
            raise TypeError
        else:
            self.listOfQuestions = listOfQuestions

        # ------Skapar olika element--------#
        self.master = master
        self.frame = tk.Frame(self.master)
        self.welcome = tk.Label(self.frame, text="Welcome to my game!", width=53, bd=40, font=TITLE_FONT)
        self.play = tk.Button(self.frame, text="Play Game", width=40, command=self.play_window, pady=5,
                               font=MENUOPTION_FONT)
        self.highscore = tk.Button(self.frame, text="Highscore", width=40, command=self.highscore_window, pady=5,
                                   font=MENUOPTION_FONT)
        self.quit = tk.Button(self.frame, text="Close game", width=40, command=self.quit_game, pady=5,
                              font=MENUOPTION_FONT)
        self.space1 = tk.Label(self.frame, text="", width=53)
        self.space2 = tk.Label(self.frame, text="", width=53)
        self.space3 = tk.Label(self.frame, text="", width=53)

        # -------Packeterar elementen------#
        # self.space1,2,3 används för att skapa lite utrymme mellan knapparna.
        self.welcome.pack()
        self.play.pack()
        self.space2.pack()
        self.highscore.pack()
        self.space3.pack()
        self.quit.pack()
        self.frame.pack()

        # Denna metod hittades
        # http://stackoverflow.com/questions/24885827/python-tkinter-how-can-i-ensure-only-one-child-window-is-created-onclick-and-no.
        # Jag har däremot perfaktat den lite mer...
        self.underWindow = None

    def play_window(self):
        """
        Här skapas nya Game objekt, det vill säga, nya frames(i mitt fall toplevel).
        Denna anropas varje gång man trycker på Spela spelet knappen.
        Här använder jag en checker för att kolla om den nya framen är skapad. Det fungerar såhär:
        I klassen finns en instansvariabel som heter self.underWindow, den är satt till None.
        När toplevel framen skapas sätts den så blir self.underWindow = den framen. Det vill säga, ej tom.
        Men i toplevelframen finns en instansvariabel som heter self.checker, som är satt till False.
        Om man väljer att avsluta programmet anropas self.avsluta() och därmed sätts self.checker = True.
        Om detta händer sätts self.underWindow=None igen och ett nytt objekt skapas.
        :return:
        """
        if not self.underWindow:
            self.underWindow = Game(self.master, self.listOfQuestions)
        if self.underWindow.checker:
            self.underWindow = None
            self.underWindow = Game(self.master, self.listOfQuestions)

    def highscore_window(self):
        """
        Här skapas nya Highscore objekt, det vill säga, nya frames(i mitt fall toplevel).
        Denna anropas varje gång man trycker på Se Highscore knappen.
        Här använder jag en checker för att kolla om den nya framen är skapad. Det fungerar såhär:
        I klassen finns en instansvariabel som heter self.underWindow, den är satt till None.
        När toplevel framen skapas sätts den så blir self.underWindow = den framen. Det vill säga, ej tom.
        Men i toplevelframen finns en instansvariabel som heter self.checker, som är satt till False.
        Om man väljer att avsluta programmet anropas self.avsluta() och därmed sätts self.checker = True.
        Om detta händer sätts self.underWindow=None igen och ett nytt objekt skapas.
        :return:
        """
        if not self.underWindow:
            self.underWindow = Highscore(self.master, self.listOfQuestions)
        if self.underWindow.checker:
            self.underWindow = None
            self.underWindow = Highscore(self.master, self.listOfQuestions)

    def quit_game(self):
        """
        Avslutar hela spelet
        :return:
        """

        if not self.underWindow:
            self.master.destroy()

        elif self.underWindow.checker:
            self.underWindow = None
            self.master.destroy()


class Game(tk.Toplevel):
    def __init__(self, master, qList):
        """
        Skapar ett nytt fönster, alltså en toplevel med parent widget master som är huvudmenyn.
        :param master: Parent widget, dvs huvudmenyn
        :param qList: Listan på frågor
        :return:
        """
        # Istället för att göra som vanligt, alltså typ self.master = master,
        # self.frame = tk.Frame(self.master), använder vi denna metod.
        # Detta gör att varje topclass blir ett egen window och inte endast en frame
        # som ett window.
        tk.Toplevel.__init__(self, master)
        # sätter upp frame för gui

        self.qList = qList
        self.title("Quiz Game")
        self.geometry("400x290")

        self.resizable(width=tk.FALSE, height=tk.FALSE)
        # Här skapar jag en frame så att jag kan cleara skärmen enkelt
        self.frame = tk.Frame(self)
        self.frame.pack()
        # ------------------------------
        self.l1 = tk.Label(self.frame, text="You are about to play the game!", bd=20, font=QUESTION_FONT)
        self.name = tk.Label(self.frame, text="Name", font=MENUOPTION_FONT)
        self.nameEntry = tk.Entry(self.frame, bd=1)
        self.space2 = tk.Label(self.frame, text="")
        self.space2.pack()
        self.space3 = tk.Label(self.frame, text="")
        self.space3.pack()
        self.l1.pack()
        self.name.pack()
        self.nameEntry.pack()
        self.space = tk.Label(self.frame, text="")
        self.space.pack()
        self.playButton = tk.Button(self.frame, text="Play", command=self.check_name_entry, font=MENUOPTION_FONT)
        self.playButton.pack()

        self.checker = False

        # taget från http://stackoverflow.com/questions/4643007/intercept-tkinter-exit-command
        self.wm_protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        """
        Avslutar framet. Samt sätter checker till True, vilket gör att man kan öppna spelet igen om man vill.
        :return:
        """
        self.checker = True
        self.destroy()

    def check_name_entry(self):
        """
        Kollar det man skriver in i self.nameEntry. Här anropas checkname funktionen.
        Om namnet ej godkäns ges ett felmeddelande
        Annars så spelas spelet med namnet som parameter, samt så anropas self.clear_screen().
        :return:
        """
        name = self.nameEntry.get()

        # if checkname(theName, "names.txt"):
        #   messagebox.showerror("Oh no!", "Please enter a new name",
        #                       parent=self)

        if check_name(name) == 0:
            messagebox.showerror("Oh no!", "Please use normal characters",
                                 parent=self)
        elif check_name(name) == 1:
            messagebox.showerror("Oh no!", "Name too short",
                                 parent=self)
        elif check_name(name) == 2:
            messagebox.showerror("Oh no!", "Name too long",
                                 parent=self)
        elif check_name(name) == 3:
            self.clear_screen()
            self.play_game(name)

    def clear_screen(self):
        """
        Denna funktion tar bort widgetsarna från denna frame.
        Det gör att jag kan placera nya labels o buttons etc på en ren skärm
        utan att behöva skapa en ny frame.
        :return:
        """
        self.frame.destroy()

    def play_game(self, name):
        """
        Här körs själva spelet.
        Hur algoritmen ser hur skiljer sig lite gentemot hur betygB versionen såg ut.
        Detta är för att knappar fungerar inte riktigt som inputs.
        En input kan stanna upp en for loop och vänta på användarens
        input, men de gör inte buttons.
        Alltså måste man bygga en egen forloop som byter fråga och alternativ.
        Detta har jag då gjort med hjälp av en extra funktion som jag kallar check_answer.
        I dess docstring förklarar jag mer vad den gör, men
        egentligen är det så att i denna funktion skapas endast den första frågan och dess alternativ.
        Därefter sätts nya värden
        efter man har tryckt på en knapp. När man trycker på en knapp anropas check_answer.
        :param name: Namnet på spelaren
        :return:
        """
        self.queCounter = 0
        question = "{}. {}".format(self.queCounter + 1, self.qList[self.queCounter].get_question())
        self.userName = name
        self.text = tk.StringVar()
        self.questionText = tk.Label(self, textvariable=self.text, bd=40, wraplength=390)

        self.text.set(question)

        self.buttonFrame = tk.Frame(self)

        self.spaceDivider1 = tk.Label(self, text=" ")
        self.spaceDivider2 = tk.Label(self, text=" ")
        self.spaceDivider3 = tk.Label(self, text=" ")

        # Question Alternative Buttons
        self.alt1 = tk.Button(self.buttonFrame, width=30, text=self.qList[self.queCounter].get_answers()[0],
                              command=lambda: self.check_answer(1))
        self.alt2 = tk.Button(self.buttonFrame, width=30, text=self.qList[self.queCounter].get_answers()[1],
                              command=lambda: self.check_answer(2))
        self.alt3 = tk.Button(self.buttonFrame, width=30, text=self.qList[self.queCounter].get_answers()[2],
                              command=lambda: self.check_answer(3))

        self.questionText.pack()
        self.buttonFrame.pack()
        self.spaceDivider1.pack()
        self.alt1.pack(side=tk.TOP)
        self.spaceDivider2.pack()
        self.alt2.pack(side=tk.TOP)
        self.spaceDivider3.pack()
        self.alt3.pack(side=tk.TOP)

        self.listOfRightWrong = []
        self.numOfRights = 0

    def check_answer(self, selector):
        """
        Denna funktion har då i uppgift att kolla om du har svarat rätt på frågan(första if och else satserna)
        samt oberoende av detta svar ställa nästa fråga.
        Den har även i uppgift att kolla om man har svarat på alla frågor(andra ifsatsen).
        Har man det så anropas clear_screen, samt så förstörs även frågelabeln och knappalternativen.
        Om dessa inte uppfylls så ställs en ny fråga
        Alltså anrop till set_new_question()
        :param selector: Id:et på svaret man gav
        :return:
        """
        self.queCounter += 1

        if self.right_or_wrong(self.qList[self.queCounter - 1], selector):
            self.listOfRightWrong.append([self.queCounter, "R"])
            self.numOfRights += 1

        else:
            self.listOfRightWrong.append([self.queCounter, "F"])

        # Kolla att man har svarat på alla frågor
        if self.queCounter >= len(self.qList):
            self.finished_game()

        else:
            self.set_new_question()

    def set_new_question(self):
        """
        När denna metod kallas sätts labeln till en ny fråga samt knapparna ändras..
        :return:
        """
        newQuestion = "{}. {}".format(self.queCounter + 1, self.qList[self.queCounter].get_question())
        self.text.set(newQuestion)
        self.alt1.config(text=self.qList[self.queCounter].get_answers()[0])
        self.alt2.config(text=self.qList[self.queCounter].get_answers()[1])
        self.alt3.config(text=self.qList[self.queCounter].get_answers()[2])

    def finished_game(self):
        """
        Kallas om man har svarat på alla frågor. Clearar skärmen, visar scoren man har fått samt visas
        en knapp som tar en tillbaka till statistikmenyn.
        :return:
        """
        self.clear_screen()
        self.buttonFrame.destroy()
        self.questionText.destroy()
        new_name = create_name_file(self.userName, "userscores")

        finishedGameText = "Good job {}! You got {} correct answers out of {} questions".format(new_name,
                                                                                                self.numOfRights,
                                                                                                len(self.qList))

        self.finishLabel = tk.Label(self, text=finishedGameText)
        self.finishLabel.pack()
        self.toQuit = tk.Button(self, text="Go back to the main menu", command=self.close)
        self.toQuit.pack()

        save(self.numOfRights, new_name, self.listOfRightWrong, "userscores")

    @staticmethod
    def right_or_wrong(question, answer):
        """
        Kollar om man har svarat rätt eller fel.
        :param question: Frågan som ställs
        :param answer: Det rätta svaret
        :return: True eller False om man har svarat rätt respektive fel.
        """
        if answer == 1:
            answer = question.answers[0]
        elif answer == 2:
            answer = question.answers[1]

        elif answer == 3:
            answer = question.answers[2]

        if question.right == answer:
            return True
        else:
            return False


class Highscore(tk.Toplevel):
    def __init__(self, master, listOfQuestions):
        """
        Skapar ett nytt fönster, alltså en toplevel med parent widget master som är huvudmenyn.
        :param master: Själva parent widgeten, dvs huvudmenyn.
        :param listOfQuestions: Listan på frågor
        :return:
        """
        # Istället för att göra som vanligt, alltså typ self.master = master,
        # self.frame = tk.Frame(self.master), använder vi denna metod.
        #  Detta gör att varje topclass blir ett egen window och inte endast en frame
        # som ett window.
        tk.Toplevel.__init__(self, master)
        self.geometry("500x500+40+40")
        self.configure(background="white")
        self.title("Quizgame")
        self.listOfQuestions = listOfQuestions
        self.resizable(width=tk.FALSE, height=tk.FALSE)
        # hanterar hur man stänger fönstret
        self.checker = False
        # taget från http://stackoverflow.com/questions/4643007/intercept-tkinter-exit-command
        self.wm_protocol("WM_DELETE_WINDOW", self.close_full)

        # Skapar en frame för att kunna cleara skärmen enkelt
        self.frame = tk.Frame(self)
        self.frame.configure(background="white")

        self.frame.pack()
        # taget från http://stackoverflow.com/questions/4241036/how-do-i-center-a-frame-within-a-frame-in-tkinter
        self.frame.place(in_=self, anchor="c", relx=.5, rely=.5)
        # -------------------------------------------------------------
        self.highscore = tk.Button(self.frame, text="Highscore", width=20, font=MENUOPTION_FONT,
                                   command=lambda: self.clear_widget(1))
        self.stats = tk.Button(self.frame, text="Stats for each question", width=20, font=MENUOPTION_FONT,
                               command=lambda: self.clear_widget(2))
        self.avs = tk.Button(self.frame, text="Back to main menu", command=self.close_full, font=MENUOPTION_FONT)

        self.space = tk.Label(self.frame, text="", bg="white")
        self.space1 = tk.Label(self.frame, text="", bg="white")

        self.highscore.pack()
        self.space.pack()
        self.stats.pack()
        self.space1.pack()
        self.avs.pack()

    def clear_widget(self, checker):
        """
        Denna funktion tar bort allt på skärmen efter man har gjort ett visst val.
        När jag får upp menyn med visa highscore och visa statistik,
        beroende på vad jag väljer kommer olika saker clearas, samt anropas.
        Så om jag väljer Se highscore, då clearas hela framet och self.show_highscore() anropas
        Om jag väljer Se Statistik, då clears hela framet och self.show_stats() anropas.
        :param checker:
        :return:
        """
        if checker == 1:
            self.frame.destroy()
            self.show_highscore(self.calc_highscore("userscores"))
        elif checker == 2:
            self.frame.destroy()
            self.show_stats(self.calc_stats("userscores"))

    def show_stats(self, statList):
        """
        Metod för att visa statistiken, väldigt lik den versionen i fragesport_betygB.py.
        Den enda skillnaden är hur det visas, alltså i en textbox.
        :param statList: statList med statistik
        :return:
        """
        self.highscore = tk.Text(self, height=25)
        newStatList = self.calc_procentage(statList, "userscores")
        headers = ["Question", "Procentage", "Num of rights"]

        self.highscore.insert(tk.INSERT, tabulate(newStatList, headers, tablefmt="grid"))

        save_stats(statList=newStatList, file="statistics.csv")

        self.highscore.config(state=tk.DISABLED)
        self.highscore.pack()
        self.back = tk.Button(self, text="Back to main menu", command=self.close_half, font=MENUOPTION_FONT)
        self.back.pack()

    def calc_stats(self, directory):
        """
        Läser in filerna och skapar statistik.
        :param directory: Mappen där filerna är
        :return: en hiList med statistik
        """
        highscoreList = []
        hiList = {}

        # lite felhantering
        try:
            os.path.exists(directory)
            checker = True
        except FileNotFoundError:
            raise FileNotFoundError

        if checker:
            for filename in os.listdir(directory):
                thefile = os.path.join(directory, filename)
                with open(thefile, "r") as reader:
                    next(reader)
                    nameandscore = reader.readlines()
                for rad in nameandscore:
                    alter = rad.split("/")
                    highscoreList.append([alter[0].strip(), alter[1].strip()])

        for counter, element in enumerate(highscoreList, 1):
            if counter > len(self.listOfQuestions):
                break
            else:
                hiList[counter] = highscoreList.count([str(counter), "R"])
        return hiList

    @staticmethod
    def calc_procentage(dictOfStats, directory):

        procentList = []
        for key, value in dictOfStats.items():
            length = len(os.listdir(directory))
            procent = format(value * 100 / length, '.2f')
            procentList.append([key, procent, value])
        return procentList

    def show_highscore(self, highscore):
        """
        Metod för att visa highscore
        :param highscore: Lista av highscore
        :return:
        """
        self.highscore1 = tk.Text(self, width=200, height=25, padx=40)

        headers = ["Place", "Name", "Score"]

        newHighscore = []
        for place, rad in enumerate(highscore):
            newHighscore.append([place + 1, highscore[place][0], highscore[place][1]])
            if place >= 9:
                break

        self.highscore1.insert(tk.INSERT, tabulate(newHighscore, headers, tablefmt="grid"))
        self.highscore1.config(state=tk.DISABLED)
        self.highscore1.pack()
        self.tillbaka = tk.Button(self, text="Tillbaka till huvudmenyn", command=self.close_half, font=MENUOPTION_FONT)
        self.tillbaka.pack()

    @staticmethod
    def calc_highscore(directory):
        """
        Läser in filerna och skapar highscore.
        :param directory: Mappen där filerna ligger
        :return: En highscorelista
        """
         # Koden nedan körs bara om mappen finns
        try:
            os.path.exists(directory)
            checker = True
        except FileNotFoundError:
            raise FileNotFoundError

        highscoreList = {}
        # Credit för os.listdir och os.path.join till
        #  http://stackoverflow.com/questions/18262293/python-open-every-file-in-a-folder
        if checker:
            for filename in os.listdir(directory):
                thefile = os.path.join(directory, filename)
                with open(thefile, "r") as reader:
                    nameandscore = reader.readlines()
                    nameandscore = [nameandscore[0].strip()]
                for rad in nameandscore:
                    alter = rad.split("/")
                    highscoreList[alter[0]] = int(alter[1])

        highscore = sorted(highscoreList.items(), key=operator.itemgetter(1), reverse=True)
        return highscore

    def close_half(self):
        """
        Avslutar endast det halvt, alltså går tillbaka till statistikmenyn.
        :return:
        """
        self.checker = True
        self.underWindow = Highscore(self.master, self.listOfQuestions)
        self.destroy()

    def close_full(self):
        """
        Avslutar helt och hållet, sätter checker till True så att
        man kan öppna nya toplevels.
        :return:
        """
        self.checker = True
        self.destroy()


def read_files(file):
    """
    Läser in filen med frågor. Delar sedan upp inputen till frågor, alternativ och rätta svar. Sedan läggs
    dessa in i en lista av frågeobjekt.
    :param file: Filen med frågor
    :return: En lista av instanser av klassen Question.
    """

    # Lite felhantering
    try:
        with open(file, "r"):
            checker = True
    except:
        raise FileNotFoundError

    if checker:
        with open(file, "r") as t1:
            next(t1)  # Ser till att vi kan läsa titeln till dokumentet, alltså där jag förklarar formatet
            data = t1.readlines()

        questionList = []

        for rad in data:
            alter = rad.split("/")

            questionList.append(
                Question(str(alter[0].strip()), [str(alter[1].strip()), str(alter[2]).strip(), str(alter[3]).strip()],
                         str(alter[4]).strip()))
        return questionList


def save(result, name, rightOrWrong, directory):
    """
    Sparar highscore och namn i en ny fil med spelarens namn som filnamn
    :param result: Antalet rätt spelaren fick
    :param name: Spelarens namn
    :param rightOrWrong: Lista på svar som man har svarat rätt eller fel på
    :param directory: Där filen ska sparas
    :return:
    """

    try:
        os.path.exists(directory)
        checker = True
    except:
        raise FileNotFoundError

    if checker:

        # fileName = os.path.join(directory, name + ".txt")
        fileName = directory + "/" + name + ".txt"

        file = open(fileName, "w")

        file.write(name + "/" + str(result) + "\n")
        for result in rightOrWrong:
            file.write(str(result[0]) + "/" + str(result[1]) + "\n")

        file.close()


def save_stats(statList, file):
    """
    Sparar statistiken i en csv fil
    :param statlist: Listan med statistik!
    :param file: Filen där statistiken ska sparas
    :return:
    """

    with open(file, 'w', newline="") as statFile:
        statFileWriter = csv.writer(statFile, delimiter=';')
        statFileWriter.writerows([["Question", "Procent", "Num of right"]])
        statFileWriter.writerows(statList)


def create_name_file(name, directory):
    # fileName = os.path.join(directory, name + ".txt")
    fileName = directory + "/" + name + ".txt"
    saveName = name

    n = 1
    while os.path.exists(fileName):

        # används för testning
        if name == "testuser":
            fileName = os.path.join(directory, ("%s(%i).txt" % (name, 1)))
            break

        saveName = ("%s(%i)" % (name, n))

        fileName = os.path.join(directory, ("%s(%i).txt" % (name, n)))
        n += 1

    try:
        open(fileName, 'w').close()
    except:
        raise FileNotFoundError

    return saveName


def check_name(name):
    """
    Kollar att namnet är ok
    :param name: Detta är den variabel man kollar, om den finns i listan av namn eller inte
    :param file: Filen som ska checkas
    :return: True om den finns i listan, False om den inte finns i listan
    """
    # Kod som används för testande
    if not name.isalpha():
        return 0
    elif not len(name) > 2:
        return 1
    elif len(name) >= 9:
        return 2
    else:
        return 3


def main():
    """
    Här anropas nästan alla andra metoder. Först läser jag in frågorna, sen skapar jag ett nytt tkinterobjekt.
    :return:
    """
    # Läser in frågorna och sedan läggs de in i questionsvariabeln i form av en lista
    fileName = os.path.join("QuestionFolder", "fragor2.txt")
    questions = read_files(fileName)

    root = tk.Tk()
    root.title("My quizgame")
    root.geometry("400x290")
    root.resizable(width=tk.FALSE, height=tk.FALSE)

    app = MainApplication(root, questions)
    root.mainloop()


if __name__ == '__main__':
    main()
