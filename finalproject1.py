#
# finalproject.py - Final Project, Part 1
#
# Part 1 - Building an initial text model
#

class TextModel():
    """ serves as a blueprint for objects that model a body of text
    """
    # pt 1, pr 1
    def __init__(self, model_name):
        """ constructs a new TextModel object by accepting a string model_name as 
            a parameter and initializing three attributes:
                name - string that is a label, uses model_name parameter
                words - dictionary that records # of times each word appears
                word_lengths - dictionary that records the # of times each length appears
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        
    # pt 1, pr 2
    def __repr__(self):
        """ returns a string that includes the name of the model as well as the sizes of 
            the dictionaries for each feature of the text.
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        return s
    
    # pt 1, pr 4
    def add_string(self, s):
        """ Analyzyes the string txt and adds its pieces to the model by augmenting the 
            feature dictionaries defiined in the constructor. Should not explicitly return a value
        """
        word_list = clean_text(s)
        for w in range(len(word_list)):
            if word_list[w] not in self.words:
                self.words[word_list[w]] = 1
            else:
                self.words[word_list[w]] += 1
                
            
        for w in range(len(word_list)):
            if len(word_list[w]) not in self.word_lengths:
                self.word_lengths[len(word_list[w])] = 1
            else:
                self.word_lengths[len(word_list[w])] += 1

    # pt 1, pr 5
    def add_file(self, filename):
        """ adds all of the text in the fild identified by filename to the model. It should not
            explicitly return a value.
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        s = f.read()
        self.add_string(s)
        f.close()
        
    # pt 2, pr 1
    def save_model(self):
        """ saves the TextModel object self by writing its various feature dictionaries to files.
            there will be 1 file written for each feature dictionary.
        """
        a = str(self.name) + '_words'
        b = str(self.name) + '_word_lengths' 
        f = open(a, 'w')
        g = open(b, 'w')
        f.write(str(self.words))
        g.write(str(self.word_lengths))
        f.close()
        g.close()
        
    # pt 2, pr 2
    def read_model(self):
        """ reads the stored dictionaries for the TextModel object from their files and assigns
            them to the attributes of the called TextModel
        """
        a = str(self.name) +'_words'
        b = str(self.name) + '_word_lengths'
        f = open(a, 'r')
        g = open(b, 'r')
        a_str = f.read()
        b_str = g.read()
        f.close()
        g.close()
        
        self.words = dict(eval(a_str))
        self.word_lengths = dict(eval(b_str))
    
# pt 1, pr 3 
def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list containing the 
        words in txt after it has been 'cleaned'. This function will b used when u need
        to process each word in a text individually, w/o having to worry abt punctuation
    """
    text = ''
    for i in range(len(txt)):
        if txt[i] != '.' and txt[i] != ',' and txt[i] != '?' and \
           txt[i] != '!' and txt[i] != ':' and txt[i] != '"':
               text += txt[i]
    text = text.lower()
    text = text.split(' ')
    return text

def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.
    
def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)
