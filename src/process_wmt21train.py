import os
import pycountry
import bnlp  # bengali
import jieba  # chinese
from nltk import word_tokenize


# hindi
# run this setup once
from inltk.inltk import setup

try:
    setup("hi")
except RuntimeError:  # if it's already running, will give runtime error
    pass


from inltk.inltk import tokenize as hi_tokenize
import spacy


class WMT21TrainData:
    def __init__(self, filename):
        self.filename = filename
        self.basename = os.path.basename(filename)
        parsed = self.basename.split(".")
        if parsed[2] == "src":
            self.dataset, self.langpair, _, self.language = parsed
        elif parsed[2] == "ref":
            self.dataset, self.langpair, _, self.ref_version, self.language = parsed
        self.source_lang_2, self.target_lang_2 = self.langpair.split("-")
        self.source_lang_3 = self.iso2_to_3(self.source_lang_2)
        self.source_lang_3 = self.iso2_to_3(self.target_lang_2)
        self.language_full = self.iso2_to_full(self.language)
        self.data = self.read_file(filename)

        # dataset related feature processing
        self.data_size = len(self.data.splitlines())
        self.tokens = self.tokenize(self.data)
        self.types = set(self.tokens)
        self.ttr = self.type_token_ratio()

    def read_file(self, filename):
        file = open(filename)
        return file.read()

    def iso2_to_3(self, iso2_language_code):
        return pycountry.languages.get(alpha_2=iso2_language_code).alpha_3

    def iso2_to_full(self, iso2_language_code):
        return pycountry.languages.get(alpha_2=iso2_language_code).name

    def tokenize(self, data):
        try:
            return word_tokenize(data, language=self.language_full)
        except:

            if self.language_full == "Bengali":
                bnltk = bnlp.NLTKTokenizer()
                return bnltk.word_tokenize(data)

            elif self.language_full == "Chinese":
                # was going to use spacy, but saw a few people saying it gave strange results? so decided to use jieba
                # jieba.cut returns generator
                return list(jieba.cut(data, cut_all=True))

            elif self.language_full == "Hindi":
                return hi_tokenize(data, "hi")

            elif (
                self.language_full == "Japanese"
            ):  # little slow, looked into other packages too, but ran into installation troubles
                nlp = spacy.load("ja_core_news_sm")

                ret = []

                for line in data.splitlines():
                    doc = nlp(line)
                    for token in doc:
                        ret.append(token.text)
                return ret

            else:
                # hausa, xhosa, zulu - can use space for segmentation,
                # but they're agglutinative (잡+다, 잡+히+다 type grammatical/meaning change. but not german, kaffeepause/krankenwagen fusional but not agglutinative)
                # so tokenization might be more involved than space segmentation?
                # started to look into packages for tokenization: https://www.masakhane.io/home

                # also had trouble finding icelandic tokenizer, but for now using white space segmentation

                # print("{} not supported by NLTK, tokenized by space".format(self.language_full))
                # print("--++--")
                # print(self.data[:20])
                # print("--++--\n\n")
                return self.data.split(" ")

    def type_token_ratio(self):
        return len(self.types) / len(self.tokens)

    def subword_tokenize(self):
        pass

    def word_overlap(self):
        pass
