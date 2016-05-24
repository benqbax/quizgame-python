import unittest
import quizgame_nogui
import random
import os


# http://stackoverflow.com/questions/2030053/random-strings-in-python


def randomword(length):
    valid_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join((random.choice(valid_letters) for i in range(length)))


class FunkTest(unittest.TestCase):
    """
    Kollar de vanliga funktionerna.
    """


    def test_check_name(self):

        self.assertEqual(quizgame_nogui.check_name(name = "\\"), 0)
        self.assertEqual(quizgame_nogui.check_name(name = "thisnameistodamnlong"), 2)
        self.assertEqual(quizgame_nogui.check_name(name = "sh"), 1)
        self.assertEqual(quizgame_nogui.check_name(name = "BestName"), 3)

    def test_create_name_file(self):
        """
        Testar create_file((
        :return:
        """

        # först skapar jag en testanvändare
        name = quizgame_nogui.create_name_file(name="testuser", directory="userscores")
        # testar att create_new_file har ett undantag för "testuser"
        self.assertEqual(name, "testuser")
        self.assertIsInstance(name, str)

        self.assertTrue(os.path.exists("userscores/testuser.txt"))

        # kör funktionen igen, så att den skapar testuser(1)
        quizgame_nogui.create_name_file(name="testuser", directory="userscores")
        self.assertTrue(os.path.exists("userscores/testuser(1).txt"))

        self.assertRaises(FileNotFoundError, quizgame_nogui.create_name_file,name = "bajs", directory="das")

        # tar bort filen så samma sak kan testas igen
        os.remove("userscores/testuser(1).txt")

    def test_read_files(self):
        """
        Testar read_files()
        :return:
        """
        # Läser in standardfrågorna
        fileName = os.path.join("QuestionFolder", "fragor2.txt")

        # Läser in en testfil med testfråga, som har en fråga som är "Test question"
        testFile = os.path.join("QuestionFolder", "fragor3.txt")

        # sparar frågorna i variabler
        questions = quizgame_nogui.read_files(fileName)
        testQuestion = quizgame_nogui.read_files(testFile)

        # här kollar jag att frågan har lästs in rätt
        for que in testQuestion:
            # kollar att inmatningen är rätt
            self.assertEqual(que.get_question(), "Test question")
            self.assertEqual(que.get_answers(), ["1","2","3"])
            self.assertEqual(que.get_right(), "3")

            self.assertIsInstance(que.get_question(), str)


        # Kollar att frågorna returneras i form av en lista
        self.assertIsInstance(questions, list)

        with open(fileName, "r") as reader:
            next(reader)
            testQuestion1 = reader.readlines()

        # Kollar att antalet frågor är korrekt
        self.assertEqual(len(testQuestion1), len(questions))



        # Felhantering
        self.assertRaises(FileNotFoundError, quizgame_nogui.read_files, "aFileThatDoesNotExist.txt")

    def test_save(self):
        """
        Först skapas en testanvändare, sen kollar man att denna användare finns med i listan.
        :return:
        """

        rightorwrong = [[1, 'R'], [2, 'F'], [3, 'F'], [4, 'F'], [5, 'F'], [6, 'F'], [7, 'F'], [8, 'F'], [9, 'F'],
                        [10, 'F'], [11, 'F']]
        name = "testuser"
        result = 1

        quizgame_nogui.save(result = result, name = name, rightOrWrong = rightorwrong, directory = "userscores")
        self.assertTrue(os.path.exists("userscores/testuser.txt"))



        # öppnar filen och kollar att den innehåller rätt saker
        with open("userscores/testuser.txt", "r") as reader:
            data = reader.readlines()
            nameAndScore = data[0].strip()
            stats = data[1:]

        testLista = []
        for rad in stats:
            alter = rad.split("/")
            testLista.append([int(alter[0].strip()), alter[1].strip()])

        # Läser in resten av filen och kollar att det stämmer den med rightorwrong
        self.assertEqual(testLista, rightorwrong)
        # Kollar att namnet och resultatet stämmer
        self.assertEqual(nameAndScore, "{}/{}".format(name, result))


        # Kolla att man får rätt error vid fel path(neg test)
        self.assertRaises(FileNotFoundError, quizgame_nogui.save, result =  1, name = "peter", rightOrWrong = rightorwrong, directory = "DoesNotExist")

    def test_save_stats(self):
        """
        Testar att save_stats sparar statistikfilen
        :return:
        """
        statlist = [[1, '36.36', 8], [2, '59.09', 13], [3, '40.91', 9], [4, '68.18', 15], [5, '27.27', 6],
                    [6, '50.00', 11], [7, '40.91', 9], [8, '59.09', 13], [9, '31.82', 7], [10, '50.00', 11],
                    [11, '31.82', 7]]

        quizgame_nogui.save_stats(statlist, "teststat.csv")
        self.assertTrue(os.path.isfile("teststat.csv"))
        self.assertTrue(os.path.exists("teststat.csv"))
