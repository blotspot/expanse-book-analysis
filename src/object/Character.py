class Character:
    """
    Represents a Character with it's aliases and alternative spellings during the books
    """

    def __init__(self, ref_name: str, alt_names: list):
        """
        :param ref_name: reference name of the Character (displayed in figures, for example)
        :param alt_names: list of alternative names and aliases for the Character
        """
        self.ref_name = ref_name
        self.alt_names = [name for name in alt_names]

    def appearance_indices(self, words: list) -> list:
        """
        Lists all indices that mark the characters appearance in the given bag of words.
        :param words: bag of words to look up the character name in.
        :return: list of indices that mark the appearance of the characters name
        """
        indices = []
        index = 0
        while len(words) > index:
            idx = index
            bigram = ' '.join(words[index:index + 1])
            trigram = ' '.join(words[index:index + 2])
            if words[idx] in self.alt_names or bigram in self.alt_names or trigram in self.alt_names:
                if bigram in self.alt_names:
                    idx = index + 1
                if trigram in self.alt_names:
                    idx = index + 2
                indices.append(idx)
            index = idx + 1
        return indices

    def appears_in(self, words: list) -> bool:
        """
        Lists all indices that mark the characters appearance in the given bag of words.
        :param words: bag of words to look up the character name in.
        :return: list of indices that mark the appearance of the characters name
        """
        index = 0
        while len(words) > index:
            idx = index
            bigram = ' '.join(words[index:index + 1])
            trigram = ' '.join(words[index:index + 2])
            if words[idx] in self.alt_names or bigram in self.alt_names or trigram in self.alt_names:
                return True
            index = idx + 1

        return False

    def __repr__(self):
        return self.ref_name
