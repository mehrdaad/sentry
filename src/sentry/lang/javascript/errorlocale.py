from __future__ import absolute_import, print_function

import os
import re

LOCALES_DIR = 'src/sentry/data/error-locale'

translations_lookup_table = []
target_locale = {}

for locale in os.listdir(LOCALES_DIR):
    fn = os.path.join(LOCALES_DIR, locale)
    if not os.path.isfile(fn):
        continue

    with open(fn) as f:
        for line in f:
            key, translation = line.split(',', 1)
            translation = translation.strip()

            if 'en-US' in locale:
                target_locale[key] = translation
            else:
                translation_regexp = re.escape(translation)
                # Some generic errors are substrings of more detailed ones, so we need an
                # exact match
                translation_regexp = '^' + \
                    translation_regexp.replace(
                        '\%s', '(?P<format_string_data>[a-zA-Z0-9-_\$]+)') + '$'
                translation_regexp = re.compile(translation_regexp)
                translations_lookup_table.append((translation_regexp, key))


def find_translation(message):
    for translation in translations_lookup_table:
        translation_regexp, key = translation
        match = translation_regexp.match(message)

        if match is not None:
            format_string_data = match.groupdict().get('format_string_data')

            if format_string_data is None:
                return [key, None]
            else:
                return [key, format_string_data]

    return [None, None]


def format_message(message, data):
    return message.replace('%s', data)


def translate_message(original_message):
    original_message = original_message.strip()
    translation, format_string_data = find_translation(original_message)

    if translation is None:
        return original_message
    else:
        translated_message = target_locale.get(translation, original_message)

        if format_string_data is None:
            return translated_message
        else:
            return format_message(translated_message, format_string_data)


def translate_exception(data):
    type, message = data['sentry.interfaces.Message']['message'].split(':', 1)

    print('Input: ' + message)
    print('Output: ' + translate_message(message))
    data['sentry.interfaces.Message']['message'] = type + ': ' + translate_message(message)

    for entry in data['sentry.interfaces.Exception']['values']:
        print('Input: ' + entry['value'])
        print('Output: ' + translate_message(entry['value']))
        entry['value'] = translate_message(entry['value'])
