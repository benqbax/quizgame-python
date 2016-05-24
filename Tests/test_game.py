import unittest
import fragesport_betygB
import random
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


class GameTest(unittest.TestCase):
    ranWor1 = randomword(10)
    ranWor2 = randomword(5)
    ranWor3 = randomword(15)
    questionlist = []
    for i in range(0, 11):
        questionlist.append((fragesport_betygB.Question(ranWor1, [ranWor1, ranWor2, ranWor3], ranWor2)))

    game = fragesport_betygB.Game(questionlist)

    def test_init(self):
        """
        Testar att man kan skapa ett nytt spel
        :return:
        """
        for question in self.game.listOfQuestions:
            self.assertIsInstance(question, fragesport_betygB.Question)


        self.assertEqual(self.game.listOfQuestions, self.questionlist)

        self.assertRaises(TypeError, self.game.__init__, 2)
        self.assertRaises(TypeError, self.game.__init__, [2,3,2])

        self.assertIsInstance(self.game, fragesport_betygB.Game)

    def test_calc_highscore(self):
        """
        Testar att man kalkylera highscoren
        :return:
        """

        test_highscore = self.game.calc_highscore(directory="Tests/Testing Files")
        highscore_length = len(os.listdir("Tests/Testing Files"))

        self.assertEqual(len(test_highscore), highscore_length)
        self.assertTrue(test_highscore is not None)
        self.assertTrue(test_highscore, sorted(test_highscore))
        self.assertIsInstance(test_highscore, list)

        # Testa felhanteringen
        self.assertRaises(FileNotFoundError, self.game.calc_highscore, "imaginaryFolder")
        self.assertRaises(FileNotFoundError, self.game.calc_highscore, "hejsn")
        self.assertRaises(FileNotFoundError, self.game.calc_highscore, "hejsn")

    def test_calc_stats(self):
        """
        Kollar att calc_stats fungerar. 
        Först läses antalet rätt på fråga 1 i checkfirstque. 
        Därefter sparas en ny fil med endast 1 rätt
        just på fråga 1. Sedan kollar vi att den nya listan
        med antalet rätt är uppdaterad, och därmed är antalet rätt på fråga 1 större än innan.
        :return:
        """
        # testa att typ om man får rätt på alla, så att alla resultat har ökat med ett
        checkfirstque = self.game.calc_stats("Tests/Testing Files")[1]

        # lägga till ett rätt till fråga 1
        rightorwrong = [[1, 'R'], [2, 'F'], [3, 'F'], [4, 'F'], [5, 'F'], [6, 'F'], [7, 'F'], [8, 'F'], [9, 'F'], [10, 'F'], [11, 'F']]
        fragesport_betygB.save(1, randomword(5), rightorwrong, "Tests/Testing Files")

        new_stats = self.game.calc_stats("Tests/Testing Files")

        # Kollar att den nya dictionaryns första fråga har ett högre värde
        self.assertTrue(new_stats[1] > checkfirstque)
        self.assertIsInstance(new_stats, dict)

        # Testa felhanteringen
        self.assertRaises(FileNotFoundError, self.game.calc_stats, "hejsn")

    def test_right_or_wrong(self):
        """
        Testar att check_answer get true när man har svarat rätt
        :return:
        """
        for question in self.game.listOfQuestions:
            # Positivt test
            self.assertTrue(self.game.right_or_wrong(question, question.get_right()))
            self.assertTrue(self.game.right_or_wrong(question, question[2]))
            self.assertTrue(self.game.right_or_wrong(question, question.right))

            # Negativt test
            self.assertFalse(self.game.right_or_wrong(question, "Fel svar"))

    def test_chosen(self):
        """
        Testar chosen metoden
        :return:
        """
        # Testar att den ger false när man trycker in 1,2 eller 3
        self.assertTrue(self.game.chosen(1))
        self.assertTrue(self.game.chosen(2))
        self.assertTrue(self.game.chosen(3))

        # Testar att den ger True när man trycker in allt annat...
        self.assertFalse(self.game.chosen("#"))
        self.assertFalse(self.game.chosen("ds"))
        self.assertFalse(self.game.chosen("dsadsada1 "))
        self.assertFalse(self.game.chosen("1dasda "))
        self.assertFalse(self.game.chosen("2sdasd "))
        self.assertFalse(self.game.chosen("3dsadsa "))

    def test_calc_procentage(self):
        """
        Testar att calc_procentage fungerar
        :return:
        """
        rightorwrong = [[1, 'R'], [2, 'F'], [3, 'F'], [4, 'F'], [5, 'F'], [6, 'F'], [7, 'F'], [8, 'F'], [9, 'F'],
                        [10, 'R'], [11, 'F']]
        #fragesport_betygB.save(2, "SADA", rightorwrong, "Tests/Testing Files")
        statList = self.game.calc_stats(directory="Tests/Testing Files")
        statListProcent = self.game.calc_procentage(statList, directory="Tests/Testing Files")
        length = len(os.listdir("Tests/Testing Files"))
        print(length)
        for question in statListProcent:
            #self.assertEqual(question[2],length)
            procent = format(question[2] * 100 / length, '.2f')
            self.assertEqual(procent, question[1])

        # Testa felhanteringen
        self.assertRaises(FileNotFoundError, self.game.calc_stats, "hejsn")
