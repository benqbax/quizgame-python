import unittest
import quizgame_gui
import random
import tkinter as tk
import os

def randomword(length):
    """
    Skapar en random sträng
    #http://stackoverflow.com/questions/2030053/random-strings-in-python
    :param length: Längden på ordet
    :return: Sträng med random bokstäver
    """
    valid_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join((random.choice(valid_letters) for i in range(length)))


ranWor1 = randomword(10)
ranWor2 = randomword(5)
ranWor3 = randomword(15)
questionlist = []
for i in range(0, 11):
    questionlist.append((quizgame_gui.Question(ranWor1, [ranWor1, ranWor2, ranWor3], ranWor2)))
root = tk.Tk()
app = quizgame_gui.MainApplication(root, questionlist)


class GameGUITest(unittest.TestCase):

    def test_calc_highscore(self):
        """
        Testar att man kalkylera highscoren
        :return:
        """

        highscore = quizgame_gui.Highscore(root, listOfQuestions=questionlist)

        test_highscore = highscore.calc_highscore(directory="Tests/Testing Files")
        self.assertTrue(test_highscore is not None)
        self.assertTrue(test_highscore, sorted(test_highscore))

        # Testa felhanteringen
        self.assertRaises(FileNotFoundError, highscore.calc_highscore, "hejsn")

    def test_calc_stats(self):
        """
        Kollar att calc_stats fungerar. Först läses antalet rätt på fråga 1 i checkfirstque.
        Därefter sparas en ny fil med endast 1 rätt
        just på fråga 1. Sedan kollar vi att den nya listan med antalet
        rätt är uppdaterad, och därmed är antalet rätt på fråga 1 större än innan.
        :return:
        """
        statistics = quizgame_gui.Highscore(root, listOfQuestions=questionlist)

        checkfirstque = statistics.calc_stats("Tests/Testing Files")[1]

        # lägga till ett rätt till fråga 1
        rightorwrong = [[1, 'R'], [2, 'F'], [3, 'F'], [4, 'F'], [5, 'F'], [6, 'F'], [7, 'F'], [8, 'F'], [9, 'F'],
                        [10, 'F'], [11, 'F']]
        quizgame_gui.save(10, randomword(5), rightorwrong, "Tests/Testing Files")

        teststat2 = statistics.calc_stats("Tests/Testing Files")
        self.assertTrue(teststat2[1] > checkfirstque)

        self.assertRaises(FileNotFoundError, statistics.calc_stats, "hejsn")


    def test_right_or_wrong(self):
        """
        Testar att right or wrong
        :return:
        """
        game = quizgame_gui.Game(root, qList=questionlist)
        for question in game.qList:
            # Positivt test
            self.assertTrue(quizgame_gui.Game.right_or_wrong(question, question.get_right()))
            # Negativt test
            self.assertFalse(quizgame_gui.Game.right_or_wrong(question, "Köttfärs"))

    def test_calc_procentage(self):
        """
        Testar att calc_procentage fungerar
        :return:
        """
        game = quizgame_gui.Highscore(root, listOfQuestions=questionlist)
        rightorwrong = [[1, 'R'], [2, 'F'], [3, 'F'], [4, 'F'], [5, 'F'], [6, 'F'], [7, 'F'], [8, 'F'], [9, 'F'],
                        [10, 'R'], [11, 'F']]
        statList = game.calc_stats(directory="Tests/Testing Files")
        statListProcent = game.calc_procentage(statList, directory="Tests/Testing Files")
        length = len(os.listdir("Tests/Testing Files"))
        for question in statListProcent:
            procent = format(question[2] * 100 / length, '.2f')
            self.assertEqual(procent, question[1])
