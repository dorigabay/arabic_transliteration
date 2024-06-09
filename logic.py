import re
from data import letters_rules, signs_rules, suffix_letters_rules, hebrew_letters


def arabic_to_hebrew(text):
    text = re.sub('\u060c', ',', text)
    deliminator_idx, deliminator_type = [m.start() for m in re.finditer(r'[,\.]', text)], [m.group() for m in re.finditer(r'[,\.]', text)]
    words = re.split(r'[,\. ]', text)
    words = [w for w in words if w]
    hebrew_t = []
    for w in words:
        for count, c in enumerate(w):
            if c in letters_rules.keys():
                w = re.sub(c, letters_rules[c], w)
            elif c in signs_rules.keys():
                # if the charcter before is an apostrophe, put the sign before the apostrophe:
                w = re.sub(c, signs_rules[c], w) if c != '\u064B' else w[:count-1] + signs_rules[c] + w[count-1:]
        matches = list(re.finditer(r'[\u0590-\u05FF]', w))
        if matches:
            w_list = list(w)
            for match in matches:
                idx = match.start()
                letter = w_list[idx]
                if letter in suffix_letters_rules.keys():
                    if idx+1 < len(w_list) and all(c not in hebrew_letters for c in w_list[idx+1:]):
                        w_list[idx] = suffix_letters_rules[w_list[idx]]
                    if idx+1 == len(w_list) or ():
                        w_list[idx] = suffix_letters_rules[w_list[idx]]
            hebrew_t.append(''.join(w_list))
        else:
            hebrew_t.append(w)

    # put back the deliminators:
    hebrew_t_lengths = [len(w) for w in hebrew_t]
    hebrew_t_lengths_cum = [sum(hebrew_t_lengths[:i+1]) for i in range(len(hebrew_t_lengths))]
    for i in deliminator_idx:
        type = deliminator_type.pop(0)
        idx_closest = hebrew_t_lengths_cum.index(min(hebrew_t_lengths_cum, key=lambda x: abs(x-i)))
        hebrew_t[idx_closest] = hebrew_t[idx_closest] + type if i != 0 else type + hebrew_t[idx_closest]
    hebrew_t_string = ' '.join(hebrew_t)
    return hebrew_t_string, text

