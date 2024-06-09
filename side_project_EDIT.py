# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
from io import StringIO
import re

def dict_to_csv_string(dictionary):
    arabic_words = list(dictionary.keys())
    csv_string = 'Arabic word, Transcription, Translation' + '\n'
    for aw in arabic_words:
        csv_string += ','.join([aw, dictionary[aw]]) + ', \n'
    return csv_string



text = ",الكَوْن,جَريمة، جَرائِم,إرهاب,قَدْر,نِهائيّ ات"
# | Hebrew Niqqud      |           |                              |
# "\u05B0"             | ְ         | Sheva                        |
# "\u05B1"             | ֱ         | Hataf Segol                  |
# "\u05B2"             | ֲ         | Hataf Patah                  |
# "\u05B3"             | ֳ         | Hataf Qamats                 |
# "\u05B4"             | ִ         | Hiriq                        |
# "\u05B5"             | ֵ         | Tsere                        |
# "\u05B6"             | ֶ         | Segol                        |
# "\u05B7"             | ַ         | Patah                        |
# "\u05B8"             | ָ         | Qamats                       |
# "\u05B9"             | ֹ         | Holam                        |
# "\u05BA"             | ֺ         | Holam Haser for Vav          |
# "\u05BB"             | ֻ         | Qubutz                       |
# "\u05BC"             | ּ         | Dagesh or Mapiq              |
# "\u05BD"             | ֽ         | Meteg                        |
# "\u05BE"             | ־         | Maqaf                        |
# "\u05BF"             | ֿ         | Rafe                         |
# | Arabic Diacritics  |           |                              |
# "\u064B"             | ً         | Fatha                        |
# "\u064C"             | ٌ         | Damma                        |
# "\u064D"             | ٍ         | Kasra                        |
# "\u064E"             | َ         | Fathatan                     |
# "\u064F"             | ُ         | Dammatan                     |
# "\u0650"             | ِ         | Kasratan                     |
# "\u0651"             | ّ         | Shadda                       |
# "\u0652"             | ْ         | Sukun                        |
#
#
# rules = {
# "\u05D0"    | א         |
# "\u05D1"    | ב         |
# "\u05D2"    | ג         |
# "\u05D3"    | ד         |
# "\u05D4"    | ה         |
# "\u05D5"    | ו         |
# "\u05D6"    | ז         |
# "\u05D7"    | ח         |
# "\u05D8"    | ט         |
# "\u05D9"    | י         |
# "\u05DA"    | ך         |
# "\u05DB"    | כ         |
# "\u05DC"    | ל         |
# "\u05DD"    | ם         |
# "\u05DE"    | מ         |
# "\u05DF"    | ן         |
# "\u05E0"    | נ         |
# "\u05E1"    | ס         |
# "\u05E2"    | ע         |
# "\u05E3"    | ף         |
# "\u05E4"    | פ         |
# "\u05E5"    | ץ         |
# "\u05E6"    | צ         |
# "\u05E7"    | ק         |
# "\u05E8"    | ר         |
# "\u05E9"    | ש         |
# "\u05EA"    | ת         |
# }

rules = {
'\u0621': "\u05D0'",  # ء: א'
'\u0622': "\u05D0",  # آ: א
'\u0623': "\u05D0",  # أ: א
'\u0624': "", # ؤ: ""
'\u0625': "\u05D0",  # إ: א
'\u0626': "",  # ئ: ''
'\u0627': "\u05D0",  # ا: א
'\u0628': "\u05D1\u05BC",  # ب: בּ
'\u0629': "\u05D4",  # ة: ה
'\u062A': "\u05EA",  # ت: ת
'\u062B': "\u05EA'",  # ث: ת'
'\u062C': "\u05D2'",  # ج: ג'
'\u062D': "\u05D7",  # ح: ח
'\u062E': "\u05D7'",  # خ: ח'
'\u062F': "\u05D3",  # د: ד
'\u0630': "\u05D3'",  # ذ: ד'
'\u0631': "\u05E8",  # ر: ר
'\u0632': "\u05D6",  # ز: ז
'\u0633': "\u05E1",  # س: ס
'\u0634': "\u05E9\u05C1",  # ش: שׁ
'\u0635': "\u05E6",  # ص: צ
'\u0636': "\u05E6'",  # ض: צ'
'\u0637': "\u05D8",  # ط: ט
'\u0638': "\u05D8'",  # ظ: ט'
'\u0639': "\u05E2",  # ع: ע
'\u063A': "\u05E2'",  # غ: ע'
'\u0640': "",  # ـ:
'\u0641': "\u05E4",  # ف: פ
'\u0642': "\u05E7",  # ق: ק
'\u0643': "\u05DB",  # ك: כּ
'\u0644': "\u05DC",  # ل: ל
'\u0645': "\u05DE",  # م: מ
'\u0646': "\u05E0",  # ن: נ
'\u0647': "\u05D4",  # ه: ה
'\u0648': "\u05D5",  # و: ו
'\u0649': "\u05D0",  # ى: א
'\u064A': "\u05D9",  # ي: י
'\u064B': "\u05B7",   # ً: ַ
'\u064C': "\u05BB",   # ٌ: ֻ
'\u064D': "\u05B4",   # ٍ: ִ
'\u064E': "\u05B7\u05DF",   # َ: ַן
'\u064F': "\u05BB\u05DF",   # ُ: ֻן
'\u0650': "\u05B4\u05DF",   # ِ: ִן
'\u0651': "\u0651",  # ّ: ّ
'\u0652': "\u05B0"  # ْ: ְ
}

#
# rules = {
# '\u0652': 'ְ',
# 'ء': "א'",
# 'آ': 'א',
# 'أ': 'אַ',
# 'ؤ': "",
# 'إ': 'א',
# 'ئ': '',
# 'ا': 'א',
# 'ب': 'בּ',
# 'ة': 'ה',
# 'ت': 'ת',
# 'ث': "ת'",
# 'ج': "ג'",
# 'ح': 'ח',
# 'خ': "ח'",
# 'د': 'ד',
# 'ذ': "ד'",
# 'ر': 'ר',
# 'ز': 'ז',
# 'س': 'ס',
# 'ش': 'שׁ',
# 'ص': 'צ',
# 'ض': "צ'",
# 'ط': 'ט',
# 'ظ': "ט'",
# 'ع': 'ע',
# 'غ': "ע'",
# 'ف': 'פ',
# 'ق': 'ק',
# 'ك': 'כּ',
# 'ل': 'ל',
# 'م': 'מ',
# 'ن': 'נ',
# 'ه': 'ה',
# 'و': 'ו',
# 'ى': 'א',
# 'ي': 'י',
# 'ً': 'ן',
# 'ٍ': '',
# 'َ': 'ַ',
# 'ُ': 'ֻ',
# 'ِ': 'ִ',
# 'ّ': 'ّ'
# }

suffix_letters = {
    '\u05E0': '\u05DF',  # נ, ן
    '\u05DE': '\u05DD',  # מ, ם
    '\u05E6': '\u05E5',  # צ, ץ
    '\u05E4': '\u05E3',  # פ, ף
}

words = text.split(',')

transliterated = {}
arabic_word = []
hebrew_transcript = []

hebrew_pattern = r'[\u0590-\u05FF]'
arabic_pattern = r'[\u0600-\u06FF]'
hebrew_letters = [chr(i) for i in range(0x05D0, 0x05EB)]

for w in words:
    arabic_word = w
    for count, c in enumerate(w):
        if c in rules.keys():
            w = re.sub(c, rules[c], w)
    if list(re.finditer(hebrew_pattern, w)):
        sub_words = w.split(' ')
        # print(sub_words)
        for count, sw in enumerate(sub_words):
            matches = list(re.finditer(hebrew_pattern, sw))
            if matches:
                w_list = list(sw)
                for match in matches:
                    idx = match.start()
                    letter = w_list[idx]
                    if letter in sufix_letters.keys():
                        if idx+1 < len(w_list) and all(c not in hebrew_letters for c in w_list[idx+1:]):
                            w_list[idx] = sufix_letters[w_list[idx]]
                        # if idx+1 < len(w_list) and not '\u05D0' <= w_list[idx+1] <= '\u05EA':
                        if idx+1 == len(w_list) or ():
                            w_list[idx] = sufix_letters[w_list[idx]]
                # print(w_list)
            sub_words[count] = ''.join(w_list)
        w = ' '.join(sub_words)
    transliterated[arabic_word] = w

csv_string = dict_to_csv_string(transliterated)

print(csv_string)

