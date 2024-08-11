# -*- coding: utf-8 -*-
import re
import codecs

class Tokenizer:
    '''Class for tokenizer'''

    def __init__(self, text=None):
        if text is not None:
            self.text = text
            self.clean_text()
        else:
            self.text = None
        self.sentences = []
        self.tokens = []
        self.stemmed_word = []
        self.final_tokens = []

    def read_from_file(self, filename):
        with codecs.open(filename, encoding='utf-8') as f:
            self.text = f.read()
            self.clean_text()

    def generate_sentences(self):
        '''Generates a list of sentences'''
        if not self.text:
            return
        self.sentences = re.split(r'(?<=।)\s+', self.text)

    def print_sentences(self, sentences=None):
        if sentences:
            for i in sentences:
                print(i)
        else:
            for i in self.sentences:
                print(i)

    def clean_text(self):
        '''Clean the text'''
        if self.text:
            # Remove digits
            self.text = re.sub(r'\d+', '', self.text)
            # Remove specified punctuation
            self.text = re.sub(r'[,\(\)"\'‘’‘’‘’.:\[\]]', '', self.text)

    def remove_only_space_words(self):
        self.tokens = list(filter(lambda tok: tok.strip(), self.tokens))

    def tokenize(self):
        '''Tokenize the text'''
        if not self.sentences:
            self.generate_sentences()

        tokens = []
        for each in self.sentences:
            word_list = each.split()
            tokens.extend(word_list)
        self.tokens = tokens
        self.remove_only_space_words()

    def hyphenated_tokens(self):
        '''Handle hyphenated tokens'''
        hyphen_tokens = []
        for token in self.tokens:
            if '-' in token:
                parts = token.split('-')
                hyphen_tokens.extend(parts)
            else:
                hyphen_tokens.append(token)
        self.tokens = hyphen_tokens

    def tokens_count(self):
        '''Return number of tokens'''
        return len(self.tokens)

    def sentence_count(self):
        '''Return number of sentences'''
        return len(self.sentences)

    def len_text(self):
        '''Return length of original text'''
        return len(self.text)

    def generate_stem_words(self, word):
        '''Generate stem of a word'''
        suffixes = {
            1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
            2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
            3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
            4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
            5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
        }

        for L in range(5, 0, -1):
            if len(word) > L + 1:
                for suf in suffixes[L]:
                    if word.endswith(suf):
                        return word[:-L]
        return word

    def generate_stem_dict(self):
        '''Generate dictionary of stemmed words'''
        stem_word = {}
        for each_token in self.tokens:
            stem = self.generate_stem_words(each_token)
            stem_word[each_token] = stem
            self.stemmed_word.append(stem)
        return stem_word

    def remove_stop_words(self):
        '''Remove stop words from tokens'''
        with codecs.open("stopwords.txt", encoding='utf-8') as f:
            stopwords = [line.strip() for line in f]

        self.final_tokens = [token for token in self.stemmed_word if token not in stopwords]
        return self.final_tokens

    def print_tokens(self, print_list=None):
        '''Print tokens'''
        tokens_to_print = print_list if print_list else self.final_tokens
        for token in tokens_to_print:
            print(token)

if __name__ == "__main__":
    t = Tokenizer("यह वाक्य हिन्दी में है।")
    t.tokenize()
    t.print_tokens()
    print(t.sentence_count(), t.tokens_count(), t.len_text())
