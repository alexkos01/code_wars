# Вам будет предоставлено слово. Ваша задача — вернуть средний символ слова. Если длина слова
# нечетная, верните средний
# символ. Если длина слова четная, верните 2 средних символа.

def get_middle_letter(w):
    lw = len(w) // 2
    return w[lw - 1:lw + 1] if len(w) % 2 == 0 else w[lw]


print(get_middle_letter(input('enter a word\n')))
