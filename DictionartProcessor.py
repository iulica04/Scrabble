class DictionaryProcessor:
    def __init__(self, dictionary_path):
        self.dictionary_path = dictionary_path
        self.words = self.load_dictionary()
        self.letters = self.extract_letters()

    def load_dictionary(self):
        with open(self.dictionary_path, 'r') as file:
            return [line.strip() for line in file]

    def extract_letters(self):
        letters = set()
        for word in self.words:
            letters.update(word)
        return letters