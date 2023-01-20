# Args structure: lang_code: str, mapping: dict, start_letters_mapping: dict | None, exceptions: dict | None
uk_args = (
    "uk",
    {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "ґ": "g",
        "д": "d",
        "е": "e",
        "є": "ye",
        "ж": "zh",
        "з": "z",
        "и": "y",
        "і": "i",
        "ї": "yi",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ь": None,
        "ю": "yu",
        "я": "ya",
        "’": None,
        "'": None,
        "-": "-",
        " ": " ",
        "`": None,
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "0": "0",
    },
    {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "ґ": "g",
        "д": "d",
        "е": "e",
        "є": "ie",
        "ж": "zh",
        "з": "z",
        "и": "y",
        "і": "i",
        "ї": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ю": "iu",
        "я": "ia",
        "’": None
    },
    { # key = exception combination in Uk; value = (True if contained in word; result of automatic transliteration; desired result)
        "зг": ("zh", "zgh"),
        "иї": ("yyi", "yi")  # Київ -> Kyiv
    }
)

ru_args = (
    "ru",
    {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ъ": None,
        "ы": "y",
        "ь": None,
        "э": "e",
        "ю": "yu",
        "я": "ya",
        "-": "-",
        " ": " ",
        "«": "\'",
        "»": "\'",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "0": "0",
    },
    None,
    None
)


def transliterate(word: str, lang_args: tuple) -> str:
    lang, mapping, start_letters_mapping, exceptions = lang_args

    new_letters = []

    for w in word:
        if w.lower() not in mapping:
            continue

        if w.isupper():
            if lang == "uk":
                new_letters.append(start_letters_mapping[w.lower()].title())
            elif lang == "ru":
                new_letters.append(mapping[w.lower()].title())
        else:
            new_letters.append(mapping[w])

    all_letters = [x for x in new_letters if x]
    new_string = "".join(all_letters)

    if exceptions:
        for x, v in exceptions.items():
            if x in word.lower():
                if x.title() in word:
                    new_string = new_string.replace(v[0].title(), v[1].title())
                else:
                    new_string = new_string.replace(v[0], v[1])

    return new_string
