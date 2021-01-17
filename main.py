import Mykytea
import sys

class L2Transliteration():
    generic_kana_map = {"か": "کا", "き": "کی", "く": "کو", "け": "کِ", "こ": "کُ",
                   "さ": "سا", "し": "شی", "す": "سو", "せ": "کا", "そ": "سُ",
                   "た": "تا", "ち": "چی", "つ": "تسو", "て": "تِ", "と": "تُ",
                   "な": "نا", "に": "نی", "ぬ": "نو", "ね": "نِ", "の": "نُ",
                   "は": "ها", "ひ": "هی", "ふ": "فو", "へ": "هِ", "ほ": "هُ",
                   "ま": "ما", "み": "می", "む": "مو", "め": "مِ", "も": "مُ",
                   "ら": "را", "り": "ری", "る": "رو", "れ": "رِ", "ろ": "رُ",
                   "や": "یا", "ゆ": "یو", "よ": "یُ", "わ": "وا", "を": "اُ", "ん": "ن",
                   "ぱ": "پا", "ぴ": "پی", "ぷ": "پو", "ぺ": "پِ", "ぽ": "پُ",
                   "ば": "با", "び": "بی", "ぶ": "بو", "べ": "بِ", "ぼ": "بُ",
                   "だ": "دا", "ぢ": "جی", "づ": "زو", "で": "دِ", "ど": "دُ",
                   "ざ": "زا", "じ": "جی", "ず": "زو", "ぜ": "زِ", "ぞ": "زُ",
                   "が": "گا", "ぎ": "گش", "ぐ": "گو", "げ": "گِ", "ご": "گُ",
                   "ゃ": "یا", "ゅ": "یو", "ょ": "یُ"}
    yoon_map = {"しゃ": "شا", "しゅ": "شو", "しょ": "شُ",
                "ちゃ": "چا", "ちゅ": "چو", "ちょ": "چُ",
                "じゃ": "جا", "じゅ": "جو", "じょ": "جُ"}
    digit_map = {"１":"1", "２":"2", "３":"3", "４":"4", "５":"5",
                "６":"6", "７":"7", "８":"8", "９":"9", "０":"0"}
    punc_map = {"。":".", "、":",", "：":":", "「":'"', "」":'"'}
    midowrd_vowel_map = {"あ":"ا", "う":"و", "い":"ی", "え":"ِ", "お":"ُ"}

    def __init__(self, input):
        self.input = input
        self.source = self.list_pronunciations(mk.getTags(input))

        self.output = self.__pre_process(self.source.copy())
        self.output = self.__main_process(self.output)
        self.output = self.__post_process(self.output)
        self.output = " ".join(self.output)

    def list_pronunciations(self, string):
        return [[[t2[0] for t2 in t1][0] for t1 in word.tag][1] for word in string]

    def __pre_process(self, source):
        # Handling yoon:
        for comp, target in L2Transliteration.yoon_map.items():
            for i, word in enumerate(source):
                source[i] = word.replace(comp, target)

        
        for i, word in enumerate(source):
            # Handling word edges
            temp_pass1 = self.__word_ledge_handler(word)
            source[i] = self.__word_redge_handler(temp_pass1)

        return source

    def __main_process(self, source):
        return self.__sents_char_map(source, L2Transliteration.generic_kana_map)

    def __post_process(self, source):
        temp_pass1 = self.__sents_char_map(source, L2Transliteration.punc_map)
        temp_pass2 = self.__sents_char_map(temp_pass1, L2Transliteration.digit_map)

        for i, word in enumerate(temp_pass2):
            # Handling long vowels
            ttemp_pass1 = self.__longvowel_handler(word)

            # Handling Gemination
            temp_pass2[i] = self.__gem_handler(ttemp_pass1)
        
        return temp_pass2

    def __sents_char_map(self, sents, mapping):
        return ["".join(list(map(lambda x: mapping[f"{x}"]
                                           if mapping.get(f"{x}", 0) != 0 
                                           else x, word))) for word in sents]

    def __word_ledge_handler(self, word):
        if word == "は": return "وا"

        word = list(word)
        for vowel in (mapping := {"あ":"آ", "う":"او", "い":"ای", "え":"اِ", "お":"اُ"}):
            word[0] = mapping.get(word[0], word[0])
        
        return "".join(word)

    def __word_redge_handler(self, word):
        return word

    def __gem_handler(self, word):
        if "っ" in word:
            if len(word) == 1:
                word = "\u0651" + " "
                return word

            word = list(word)
            gem_loc = word.index("っ")
            while True:
                del word[gem_loc]
                word[gem_loc] += "\u0651"
                if "っ" in word:
                    gem_loc = word.find("っ")
                else: break
        return "".join(word)

    def __longvowel_handler(self, word):
        word = list(word)
        for i, char in enumerate(word):
            if i == 0:
                continue
            if char == "あ":
                if word[i-1] == "ا":
                    word[i]="-"
                else: word[i]="ا"
            elif char == "い":
                if word[i-1] == "ِ" or word[i-1] == "ی":
                    word[i]="-"
                else: word[i]="ی"
            elif char == "う":
                if word[i-1] == "ُ" or word[i-1] == "و":
                    word[i]="-"
                else: word[i]="و"
            elif char == "え":
                if word[i-1] == "ِ":
                    word[i]="-"
                else: word[i]="ِ"
            elif char == "い":
                if word[i-1] == "ُ":
                    word[i]="-"
                else: word[i]="ُ"
        return word

# Test sentence: 国境の長いトンネルを抜けると雪国である。

if __name__ == "__main__":
    input = sys.argv[1]

    # Initialize KyTea
    options = "-deftag UNKNOWN!!"
    mk = Mykytea.Mykytea(options)

    tran = L2Transliteration(input)
    print (tran.output)
