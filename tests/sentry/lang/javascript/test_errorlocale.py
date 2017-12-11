# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from sentry.testutils import TestCase
from sentry.lang.javascript.errorlocale import translate_message


class ErrorLocaleTest(TestCase):
    def test_basic_translation(self):
        actual = 'Type mismatch'
        expected = translate_message('Typenkonflikt')
        assert actual == expected

    def test_unicode_translation(self):
        expected = 'Division by zero'
        actual = translate_message('División por cero')
        assert actual == expected

    def test_same_translation(self):
        expected = 'Out of memory'
        actual = translate_message('Out of memory')
        assert actual == expected

    def test_unknown_translation(self):
        expected = 'Some unknown message'
        actual = translate_message('Some unknown message')
        assert actual == expected

    def test_translation_with_type(self):
        expected = 'RangeError: Subscript out of range'
        actual = translate_message('RangeError: Indeks poza zakresem')
        assert actual == expected

    def test_translation_with_type_and_colon(self):
        expected = 'RangeError: Cannot define property: object is not extensible'
        actual = translate_message(
            'RangeError: Nie można zdefiniować właściwości: obiekt nie jest rozszerzalny')
        assert actual == expected

    def test_interpolated_translation(self):
        expected = 'Type \'foo\' not found'
        actual = translate_message('Nie odnaleziono typu „foo”')
        assert actual == expected

    def test_interpolated_translation_with_colon(self):
        expected = '\'this\' is not of expected type: foo'
        actual = translate_message('Typ obiektu „this” jest inny niż oczekiwany: foo')
        assert actual == expected

    def test_interpolated_translation_with_colon_in_front(self):
        expected = 'foo: an unexpected failure occurred while trying to obtain metadata information'
        actual = translate_message(
            'foo: wystąpił nieoczekiwany błąd podczas próby uzyskania informacji o metadanych')
        assert actual == expected

    def test_interpolated_translation_with_type(self):
        expected = 'TypeError: Type \'foo\' not found'
        actual = translate_message('TypeError: Nie odnaleziono typu „foo”')
        assert actual == expected

    def test_interpolated_translation_with_type_and_colon(self):
        expected = 'ReferenceError: Cannot modify property \'foo\': \'length\' is not writable'
        actual = translate_message(
            'ReferenceError: Nie można zmodyfikować właściwości „foo”: wartość „length” jest niezapisywalna')
        assert actual == expected
