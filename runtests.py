import unittest

import Tests.test_funktions
import Tests.test_funktionsGUI
import Tests.test_game
import Tests.test_gameGUI
import Tests.test_fraga

tests = unittest.TestSuite()

test_finder = unittest.TestLoader()
tests.addTests(test_finder.loadTestsFromModule(Tests.test_funktions))
tests.addTests(test_finder.loadTestsFromModule(Tests.test_funktionsGUI))
tests.addTests(test_finder.loadTestsFromModule(Tests.test_game))
tests.addTests(test_finder.loadTestsFromModule(Tests.test_fraga))
tests.addTests(test_finder.loadTestsFromModule(Tests.test_gameGUI))

tester = unittest.TextTestRunner()
tester.run(tests)
