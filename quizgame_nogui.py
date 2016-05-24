# Skapad av: Ben Forsrup CMETE1
# Programmeringsteknik DD1315
# 2016-05-17
# Reviderad 2016-05-23

import sys
import os
import operator
from tabulate import tabulate
import csv


class Color:
    """
    Class that is used for changing colour amongst other things on texts
    Solution taken from
    # http://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
    """
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


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


class Game(object):
    """
    Spelklassen. Här spelas hela spelet.
    """

    def __init__(self, listOfQuestions):
        """
        Skapar ett nytt Gameobjekt
        :param listOfQuestions: en lista på de frågor som ska ställas - lista
        :return:
        """

        # avsedd för testande
        if not isinstance(listOfQuestions, list):
            raise TypeError

        if not any(isinstance(question, Question) for question in listOfQuestions):
            raise TypeError
        else:
            self.listOfQuestions = listOfQuestions

    def mainmenu(self):
        """
        Anropar print_menu() och input_choice().
        Beroende på vad man väljer anropas play_game() eller stat_choice().
        Man kan även avsluta spelet.
        :return:
        """

        print_menu()
        choice = self.input_choice()
        if choice == 1:
            self.play_game()
        elif choice == 2:
            self.stat_choice()
        elif choice == 3:
            print("You wish to exit")
            sys.exit(0)

        self.mainmenu()

    def input_choice(self):
        """
        Läser in vilket alternativ spelaren väljer, i antingen huvudmenyn, spelet eller highscore/stats menyn.
        Om svaret ej fyller chosen()s krav, så måste man skriva igen
        :return: Det valda alternativet( 1, 2 eller 3)
        """
        type_again = False

        while not type_again:
            try:
                choice = int(input("\nSelect either (1) or (2) or (3) \nAnswer: "))
                if not self.chosen(choice):
                    print("Incorrect input, try again")
                else:
                    return choice
            except ValueError:
                print("Incorrect! input, try again")

    @staticmethod
    def chosen(choice):
        """
        Kollar att valet är ok. La till denna funktion så att man kan testa
        :param choice: inputen - sträng
        :return: True om inputen är knäpp, annars False
        """
        if choice is not 1 and choice is not 2 and choice is not 3:

            return False
        else:
            return True

    def stat_choice(self):
        """
        Först printas ett par alternativ, om man vill se highscore eller statistik.
        Sedan gör användaren ett val, här anropas input_choice().
        Om användaren väljer 1 så anropas show_Highscore(), vilket printar Highscoren.
        Om användaren väljer 2 så anropas show_Stats(), vilket printar statistiken.
        Om användaren väljer 3 så anropas inget, men metoden fortsätter köra
        och därmed tas man tillbaka till huvudmenyn.
        :return:
        """

        print("\t\tStatistics\n")
        print("1. See Highscore")
        print("2. See statistics per question")
        print("3. Go back to main menu")

        choice = self.input_choice()
        print()
        if choice == 1:
            print("\t\tTop 10 - Highscore\n")
            self.print_highscore(self.calc_highscore("userscores"))

        elif choice == 2:
            print("\t\tStats per question\n")
            self.print_stats(self.calc_stats("userscores"))

        elif choice == 3:
            print()
            self.mainmenu()
        self.stat_choice()

    @staticmethod
    def calc_highscore(directory):
        """
        Kalkylerar highscoren, det vill säga personerna med de bästa resultaten
        :param directory: Platsen där filerna ligger
        :return: highscoren, alltså en lista med de bästa resultaten
        """

        # Koden nedan körs bara om mappen finns
        try:
            os.path.exists(directory)
            checker = True
        except FileNotFoundError:
            raise FileNotFoundError

        highscorelist = {}
        if checker:
            # Credit för
            # os.listdir och os.path.join till
            #  http://stackoverflow.com/questions/18262293/python-open-every-file-in-a-folder
            for filename in os.listdir(directory):
                thefile = os.path.join(directory, filename)
                with open(thefile, "r") as reader:
                    nameAndScore = reader.readlines()
                    # Tar endast ut första raden, alltså name/score
                    nameAndScore = [nameAndScore[0].strip()]
                for rad in nameAndScore:
                    alter = rad.split("/")
                    highscorelist[alter[0]] = int(alter[1])

            highscore = sorted(highscorelist.items(), key=operator.itemgetter(1), reverse=True)
            return highscore

    @staticmethod
    def print_highscore(highscore):
        """
        Printar ut highscoren
        :param highscore: En highscore lista från calc_highscore
        :return:
        """

        headers = ["Place", "Name", "Score"]

        newHighscore = []
        for place, rad in enumerate(highscore):
            newHighscore.append([place + 1, highscore[place][0], highscore[place][1]])
            if place >= 9:
                break
        print(tabulate(newHighscore, headers, tablefmt="grid"))

        print()
        input("Please enter any key to go back\n")

    def calc_stats(self, directory):
        """
        Kalkylerar statistiken per fråga. Det vill säga hur många procent som har svarat rätt på frågan.
        :param directory: Den map vi ska hämta saker från
        :return: En statistiklista
        """
        lista = {}
        hiscoreListaStat = []

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
                    stats = reader.readlines()
                for rad in stats:
                    alter = rad.split("/")
                    hiscoreListaStat.append([alter[0].strip(), alter[1].strip()])

            for counter, element in enumerate(hiscoreListaStat, 1):
                if counter > len(self.listOfQuestions):
                    break
                else:
                    lista[counter] = hiscoreListaStat.count([str(counter), "R"])

        return lista

    @staticmethod
    def calc_procentage(dictOfStats, directory):
        # lägg till
        try:
            os.path.exists(directory)
            checker = True
        except FileNotFoundError:
            raise FileNotFoundError

        if checker:

            procentList = []
            for key, value in dictOfStats.items():
                length = len(os.listdir(directory))
                procent = format(value * 100 / length, '.2f')
                procentList.append([key, procent, value])
        return procentList

    def print_stats(self, statlist):
        """
        Printar statistiken
        :param statlist: Lista av statistiken
        :return:
        """
        newStatList = self.calc_procentage(statlist, "userscores")
        headers = ["Question", "Procentage correct[%]", "Number of right"]

        save_stats(statList=newStatList, file="statistics.csv")

        print(tabulate(newStatList, headers, tablefmt="grid"))
        print()
        input("Please enter any key to go back\n")

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

        if question.get_right() == answer:
            return True
        else:
            return False

    def play_game(self):
        """
        Här körs spelet.
        :return:
        """
        print("You wish to play the game")

        name = str(input("Please enter your name(max 10 characters):\nSvar: "))
        while True:
            if check_name(name) == 0:
                name = str(input("\nPlease use normal characters. \nSvar: "))
            elif check_name(name) == 1:
                name = str(input("\nName too short. \nSvar:"))
            elif check_name(name) == 2:
                name = str(input("\nName too long. \nSvar:"))
            elif check_name(name) == 3:
                break

        listOfRightAndWrong = []
        numRight = 0
        for counter, question in enumerate(self.listOfQuestions, 1):
            # printar frågor
            queText = "{}. {}".format(counter, question.get_question())
            print(Color.BOLD + queText + Color.END)

            # printar ut alternativ
            for count, answers in enumerate(question.get_answers(), 1):
                answer = "      {}.    {}".format(count, answers)
                print(answer)
            if self.right_or_wrong(question, self.input_choice()):
                listOfRightAndWrong.append([counter, "R"])
                numRight += 1
            else:
                listOfRightAndWrong.append([counter, "F"])
        new_name = create_name_file(name, "userscores")
        finishedGame = "Good job {}! You got {} correct answers out of {} questions".format(new_name, numRight, len(self.listOfQuestions))
        print(finishedGame)
        save(numRight, new_name, listOfRightAndWrong, "userscores")


def save_stats(statList, file):
    """
    Sparar statistiken i en csv fil
    :param statList: Listan med statistik!
    :param file: Filen med statistiken
    :return:
    """

    with open(file, 'w', newline="") as statFile:
        statFileWriter = csv.writer(statFile, delimiter=';')
        statFileWriter.writerows([["Question", "Procent", "Number of right"]])
        statFileWriter.writerows(statList)


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

        for row in data:
            alter = row.split("/")

            questionList.append(
                Question(str(alter[0].strip()), [str(alter[1].strip()), str(alter[2]).strip(), str(alter[3]).strip()],
                         str(alter[4]).strip()))
        return questionList


def create_name_file(name, directory):
    """
    Skapar en fil med användarens namn. Ifall namnet är upptaget läggs (n) till.
    :param name: String - Namnet
    :param directory: String - platsen där filen ska skapas
    :return: String - namnet, om upptaget finns +(n) med
    """

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
    :return: 0 om namnet ej har rätt karaktärer
    :return 1 om namnet är för kort
    :return 2 om namnet är för långt
    :return 3 om namnet är Ok
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


def print_menu():
    """
    Printar ut menyn
    :return:
    """
    print("Menu: \n")
    print("1. Play Game")
    print("2. See statistics")
    print("3. Exit")


def main():
    """
    Här anropas nästan alla andra metoder. Den anropar mainmenu()
    och från den körs allt. Huvudmetoden helt enkelt.
    :return:
    """

    print("\t\tWelcome to Quiz Game!\n")

    # Credit för
    # os.path.join till http://stackoverflow.com/questions/13223737/how-to-read-a-file-in-other-directory-in-python
    filename = os.path.join("QuestionFolder", "fragor2.txt")
    questions = read_files(filename)

    game = Game(questions)
    game.mainmenu()


if __name__ == "__main__":
    main()
