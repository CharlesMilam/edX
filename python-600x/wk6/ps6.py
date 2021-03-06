import string

### DO NOT MODIFY THIS FUNCTION ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print 'Loading word list from file...'
    # inFile: file
    in_file = open(file_name, 'r', 0)
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print '  ', len(word_list), 'words loaded.'
    in_file.close()
    return word_list

### DO NOT MODIFY THIS FUNCTION ###
def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

### DO NOT MODIFY THIS FUNCTION ###
def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        # assert 0 <= shift < 26, 'shift is not in the proper range (0 -26): %r' % shift
        self.encrypting_dict = {}
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase

        # add lowercase characters
        for idx, char in enumerate(lowercase):
            # once beyond the end of the alphabet loop back around from the beginning, offset by the value of shift
            if idx + shift <= 25:
                self.encrypting_dict[char] = lowercase[idx + shift]
            else:
                self.encrypting_dict[char] = lowercase[(idx + shift) - 26]

        # add uppercase characters
        for idx, char in enumerate(uppercase):
            # once beyond the end of the alphabet loop back around from the beginning, offset by the value of shift
            if idx + shift <= 25:
                self.encrypting_dict[char] = uppercase[idx + shift]
            else:
                self.encrypting_dict[char] = uppercase[(idx + shift) - 26]

        return self.encrypting_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        enc_msg = ''
        enc_dict = self.build_shift_dict(shift)
        # print 'pt msg', self.message_text
        for char in self.message_text:
            if char in string.ascii_lowercase or char in string.ascii_uppercase:
                enc_msg += enc_dict[char]
            else:
                enc_msg += char

        return enc_msg


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less
        code is repeated
        '''
        Message.__init__(self, text)
        self.shift = shift
        # print 'pt text', self.message_text
        # print 'pt shift', self.shift

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class

        Returns: a COPY of self.encrypting_dict
        '''
        self.encrypting_dict = self.build_shift_dict(self.shift)
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.apply_shift(self.shift)

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift (ie. self.encrypting_dict and
        message_text_encrypted).

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        shift_vals = range(0, 26)
        best_shift = None
        best_count = 0
        word_count = 0
        test_msg = self.message_text.split(' ')
        denc_msg = ''
        best_msg = ''
        # print 'test msg:', test_msg
        # print 'test msg', test_msg
        for val in shift_vals:
            # print 'val:', val
            for word in test_msg:
                # print 'word:', word
                self.message_text = word
                # print 'message_text:', self.message_text
                test_word = self.apply_shift(26 - val)
                # print 'test word:', test_word
                if is_word(self.valid_words, test_word):
                    word_count += 1
                    # print 'word count:', word_count
                    denc_msg += test_word + ' '
                    # print 'denc msg:', denc_msg
            # print 'word count', word_count, best_count, best_shift, best_msg
            if word_count > best_count:
                # print 'in > word count'
                best_count = word_count
                best_shift = 26 - val
                best_msg = denc_msg
                word_count = 0

            word_count = 0
            denc_msg = ''

        return (best_shift, string.rstrip(best_msg))



# Test case (PlaintextMessage) - shift is in the proper range
# plaintext = PlaintextMessage('test', 27)
# plaintext.get_encrypting_dict()
# print 'Should assert that shift is out of range'
# print
# print '-' * 15
# print

# Test case (PlaintextMessage) - get_shift returns correctly
plaintext = PlaintextMessage('test', 3)
print 'Should return 3 => ', str(plaintext.get_shift())
print
print '-' * 15
print

# Test case (PlaintextMessage) - should return the encrypted dictionary
plaintext = PlaintextMessage('test', 2)
print 'encrypting dictionary: '
enc_dict =  plaintext.get_encrypting_dict()
print enc_dict
print 'should get c:', enc_dict['a']
print 'should get z:', enc_dict['x']
print 'should get a:', enc_dict['y']
print 'should get b:', enc_dict['z']
print 'should get C:', enc_dict['A']
print 'should get Z:', enc_dict['X']
print 'should get A:', enc_dict['Y']
print 'should get B:', enc_dict['Z']
print
print '-' * 15
print

# Test case (PlaintextMessage) - should return the encrypted message
plaintext = PlaintextMessage('amyz', 2)
print 'should print bnza:', plaintext.apply_shift(1)
print 'should print eqcd:', plaintext.apply_shift(4)
print
print '-' * 15
print

# Test case (PlaintextMessage) - should return the correct encrypted message after change_shift has been called
plaintext = PlaintextMessage('amyz', 1)
print 'should print bnza:', plaintext.get_message_text_encrypted()
plaintext.change_shift(4)
print 'should print eqcd:', plaintext.get_message_text_encrypted()
print
print '-' * 15
print

#Example test case (PlaintextMessage)
plaintext = PlaintextMessage('Nonsense', 2)
print 'Expected Output: Pqpugpug'
print 'Actual Output:', plaintext.get_message_text_encrypted()
print
print '-' * 15
print

#Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq')
print 'Expected Output:', (24, 'hello')
print 'Actual Output:', ciphertext.decrypt_message()
print
print '-' * 15
print

#Example test case (PlaintextMessage)
plaintext = PlaintextMessage('Message is Nonsense words: cultivate lamp wish amount gradual whichever add throat there unite pronunciation sleep conversation reduction gap', 2)
encoded_msg = plaintext.get_message_text_encrypted()
enc_text = CiphertextMessage(encoded_msg)
print 'Encoded Msg:', encoded_msg
print
print 'Plaintext:', 'Message is Nonsense words: cultivate lamp wish amount gradual whichever add throat there unite pronunciation sleep conversation reduction gap'
print 'Decoded Msg', enc_text.decrypt_message()
print
print '-' * 15
print

def decrypt_story():
    story_text = get_story_string()

    ciphertext = CiphertextMessage(story_text)

    return ciphertext.decrypt_message()

print 'dec story', decrypt_story()
