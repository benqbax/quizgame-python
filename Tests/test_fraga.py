import unittest
import quizgame_nogui
import random


# http://stackoverflow.com/questions/2030053/random-strings-in-python


def randomword(length):
    valid_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join((random.choice(valid_letters) for i in range(length)))


class FragaTest(unittest.TestCase):
    """
    Test för frågeklassen
    """

    # Fyller questionlist med frågor med random strängar, där med 10 frågor med alt1,2,3 som rätt svar
    questionlist = []
    for i in range(0, 9):
        ranWor1 = randomword(10)
        ranWor2 = randomword(5)
        ranWor3 = randomword(15)
        questionlist.append((quizgame_nogui.Question(ranWor1, [ranWor1, ranWor2, ranWor3], ranWor2)))

    for i in range(0, 9):
        ranWor1 = randomword(10)
        ranWor2 = randomword(5)
        ranWor3 = randomword(15)
        questionlist.append((quizgame_nogui.Question(ranWor1, [ranWor1, ranWor2, ranWor3], ranWor1)))

    for i in range(0, 9):
        ranWor1 = randomword(10)
        ranWor2 = randomword(5)
        ranWor3 = randomword(15)
        questionlist.append((quizgame_nogui.Question(ranWor1, [ranWor1, ranWor2, ranWor3], ranWor3)))

    def test_init(self):
        """
        Testa att man kan skapa ett Question objekt
        :return:
        """
        for question in self.questionlist:

            # Positiva testar
            self.assertEqual(question.question, question[0])
            self.assertEqual(question.get_question(), question[0])
            self.assertEqual(question.answers, question[1])
            self.assertEqual(question.get_answers(), question[1])
            self.assertEqual(question.right, question[2])
            self.assertEqual(question.get_right(), question[2])
            self.assertIsInstance(question, quizgame_nogui.Question)
            self.assertIsInstance(question[0], str)
            self.assertIsInstance(question[1], list)
            self.assertIsInstance(question[2], str)

            # Negativa testar
            self.assertRaises(TypeError, question.__init__, 1, [1, 2, 1], 1)
            self.assertRaises(TypeError, question.__init__, "Kor", "hej", 1)
            self.assertRaises(TypeError, question.__init__, "Vem skapade USA?", [1,2,3], "2")
            self.assertRaises(TypeError, question.__init__, "Hur gammal är jag?", ["20", "21", "22"], "23")
            self.assertRaises(TypeError, question.__init__, "Hur gammal är jag?", ["20", "21", "22"], 22)

    def test_get_question(self):
        """
        Testar get_question()
        :return:
        """
        for question in self.questionlist:
            self.assertEqual(question[0], question.get_question())
            self.assertIsInstance(question[0], str)

    def test_get_answers(self):
        """
        Testar get_answers()
        :return:
        """
        for question in self.questionlist:
            self.assertEqual(question[1], question.get_answers())
            self.assertIsInstance(question.get_answers(), list)

    def test_get_right(self):
        """
        Testar get_right()
        :return:
        """
        for question in self.questionlist:
            self.assertEqual(question[2], question.get_right())
            self.assertIsInstance(question[2], str)

    def test_getitem(self):
        """
        Testar __getimem__
        :return:
        """
        for question in self.questionlist:
            # Negativt test
            self.assertRaises(IndexError, question.__getitem__, 4)
            self.assertRaises(IndexError, question.__getitem__, "kebab")

            # Positivt test
            self.assertEqual(question[0], question.question)
            self.assertEqual(question[1], question.answers)
            self.assertEqual(question[2], question.right)
