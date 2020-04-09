import app
import unittest
import json
import pytest

class ExtractDescriptionTests(unittest.TestCase):

    def testExtractDescription(self):
        with open('./unittest-cases/mew-full.json') as json_file:
            data = json.load(json_file)
            json_file.close()
        with open('./unittest-cases/mew-eng-yellow-desc.txt') as txt_file:
            mew_desc = txt_file.read()
            txt_file.close()
            extractedDescription = app.extractDescription(data, 'mew')
            self.assertEqual(extractedDescription, mew_desc)

class ExtractEnglishDescriptionTests(unittest.TestCase):

    def testStandardDescription(self):
        with open('./unittest-cases/mew-flavor-text-entries.json') as json_file:
            data = json.load(json_file)
            json_file.close()
        with open('./unittest-cases/mew-eng-yellow-desc.txt') as txt_file:
            mew_desc = txt_file.read()
            txt_file.close()
            extractedDescription = app.extractEnglishDescription(data, 'mew')
            self.assertEqual(extractedDescription, mew_desc)

    def testMultipleYellowDescriptions(self):
        with open('./unittest-cases/mew-flavor-text-entires-multiple-yellow.json') as json_file:
            data = json.load(json_file)
            json_file.close()
        with open('./unittest-cases/mew-eng-yellow-desc.txt') as txt_file:
            mew_desc = txt_file.read()
            txt_file.close()
            extractedDescription = app.extractEnglishDescription(data, 'mew')
            self.assertEqual(extractedDescription, mew_desc)

    def testMultipleYellowEnglishDescriptions(self):
        with open('./unittest-cases/mew-flavor-text-entries-multiple-yellow-and-english.json') as json_file:
            data = json.load(json_file)
            json_file.close()
            with self.assertRaises(IndexError):
                app.extractEnglishDescription(data, 'mew')

class ReplaceUnwantedCharactersTests(unittest.TestCase):

    def testStandardReplacement(self):
        replacedString = app.replaceUnwantedCharacters('this is a test', (('t','s',),('p','q')))
        self.assertEqual(replacedString,'shis is a sess')

    def testEmptyStringReplacement(self):
        replacedString = app.replaceUnwantedCharacters('this is a test', ())
        self.assertEqual(replacedString,'this is a test')

    def testNothingToReplace(self):
        replacedString = app.replaceUnwantedCharacters('this is a test', (('r','z',),('p','q')))
        self.assertEqual(replacedString,'this is a test')


