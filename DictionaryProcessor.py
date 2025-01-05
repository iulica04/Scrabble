class DictionaryProcessor:
    """
    Processes a dictionary file for the Scrabble game.

    Attributes:
        dictionary_path (str): The path to the dictionary file.
        words (list): A list of words loaded from the dictionary file.
        letters (set): A set of unique letters extracted from the words.
    """

    def __init__(self, dictionary_path):
        """
        Initializes the DictionaryProcessor with the given dictionary file path.

        Args:
            dictionary_path (str): The path to the dictionary file.
        """
        self.dictionary_path = dictionary_path
        self.words = self.load_dictionary()
        self.letters = self.extract_letters()

    def load_dictionary(self):
        """
        Loads the dictionary file and returns a list of words.

        Returns:
            list: A list of words from the dictionary file.
        """
        with open(self.dictionary_path, 'r') as file:
            return [line.strip() for line in file]

    def extract_letters(self):
        """
        Extracts unique letters from the loaded words.

        Returns:
            set: A set of unique letters from the words.
        """
        letters = set()
        for word in self.words:
            letters.update(word)
        return letters