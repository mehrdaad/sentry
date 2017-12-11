from __future__ import absolute_import, print_function

import six
import os
import io
import re

LOCALES_DIR = 'src/sentry/data/error-locale'

translation_lookup_table = set()
target_locale = {}

for locale in os.listdir(LOCALES_DIR):
    fn = os.path.join(LOCALES_DIR, locale)
    if not os.path.isfile(fn):
        continue

    with io.open(fn, encoding='utf-8') as f:
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
                translation_lookup_table.add((translation_regexp, key))


def find_translation(message):
    for translation in translation_lookup_table:
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
    if not isinstance(original_message, six.string_types):
        return original_message

    type = None
    message = original_message.strip()

    # Handle both cases. Just a message and message preceeded with error type
    # eg. `ReferenceError: foo`, `TypeError: bar`
    match = re.match('^(?P<type>[a-zA-Z]*Error): (?P<message>.*)', message)

    if match is not None:
        type = match.groupdict().get('type')
        message = match.groupdict().get('message')

    translation, format_string_data = find_translation(message)

    if translation is None:
        return original_message
    else:
        translated_message = target_locale.get(translation, original_message)

        if type is not None:
            translated_message = type + ': ' + translated_message

        if format_string_data is None:
            return translated_message
        else:
            return format_message(translated_message, format_string_data)


def translate_exception(data):
    if 'sentry.interfaces.Message' in data:
        data['sentry.interfaces.Message']['message'] = translate_message(
            data['sentry.interfaces.Message']['message'])

    if 'sentry.interfaces.Exception' in data:
        for entry in data['sentry.interfaces.Exception']['values']:
            if 'value' in entry:
                entry['value'] = translate_message(entry['value'])

    return data
