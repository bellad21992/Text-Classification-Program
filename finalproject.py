#
# finalproject2.py - Final Project, Part 2
#
# Part 3 - Adding Featuers to the model
#

import math

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
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}
        
    # pt 1, pr 2
    def __repr__(self):
        """ returns a string that includes the name of the model as well as the sizes of 
            the dictionaries for each feature of the text.
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of periods: ' + str(len(self.punctuation))
        return s
    
    # pt 1, pr 4
    def add_string(self, s):
        """ Analyzyes the string txt and adds its pieces to the model by augmenting the 
            feature dictionaries defiined in the constructor. Should not explicitly return a value
        """
        # update punctuation
        words = s.split(' ')
        for i in range(len(words)):
            if '.' in words[i]:
                if '.' not in self.punctuation:
                    self.punctuation['.'] = 1
                else: 
                    self.punctuation['.'] += 1
            elif ',' in words[i]:
                if ',' not in self.punctuation:
                    self.punctuation[','] = 1
                else:
                    self.punctuation[','] += 1
            elif '!' in words[i]:
                if '!' not in self.punctuation:
                    self.punctuation['!'] = 1
                else:
                    self.punctuation['!'] += 1
            elif '?' in words[i]:
                if '?' not in self.punctuation:
                    self.punctuation['?'] = 1
                else:
                    self.punctuation['?'] += 1
                
        # update sentnece_lengths
        if '?' in s:
            words = s.split('?')
        elif '!' in s:
            words = s.split('!')
        else:
            words = s.split('.')
        if words[-1] == '':
            words = words[:-1]
        for i in range(len(words)):
            words[i] = words[i].split(' ')
        for w in range(len(words)):
            if words[w][0] == '':
                words[w] = words[w][1:]
            if len(words[w]) not in self.sentence_lengths:
                self.sentence_lengths[len(words[w])] = 1
            else:
                self.sentence_lengths[len(words[w])] += 1
        
        # update words        
        word_list = clean_text(s)
        for w in range(len(word_list)):
            if word_list[w] not in self.words:
                self.words[word_list[w]] = 1
            else:
                self.words[word_list[w]] += 1
                
        # update word_lengths    
        for w in range(len(word_list)):
            if len(word_list[w]) not in self.word_lengths:
                self.word_lengths[len(word_list[w])] = 1
            else:
                self.word_lengths[len(word_list[w])] += 1
        
        # update stems
        for w in range(len(word_list)):
            if stem(word_list[w]) not in self.stems:
                self.stems[stem(word_list[w])] = 1
            else:
                self.stems[stem(word_list[w])] += 1
        
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
        c = str(self.name) + '_stems'
        d = str(self.name) + '_sentence_lengths'
        e = str(self.name) + '_punctuation'
        f = open(a, 'w')
        g = open(b, 'w')
        h = open(c, 'w')
        i = open(d, 'w')
        j = open(e, 'w')
        f.write(str(self.words))
        g.write(str(self.word_lengths))
        h.write(str(self.stems))
        i.write(str(self.sentence_lengths))
        j.write(str(self.punctuation))
        f.close()
        g.close()
        h.close()
        i.close()
        j.close()
        
    # pt 2, pr 2
    def read_model(self):
        """ reads the stored dictionaries for the TextModel object from their files and assigns
            them to the attributes of the called TextModel
        """
        a = str(self.name) + '_words'
        b = str(self.name) + '_word_lengths'
        c = str(self.name) + '_stems'
        d = str(self.name) + '_sentence_lengths'
        e = str(self.name) + '_punctuation'
        f = open(a, 'r')
        g = open(b, 'r')
        h = open(c, 'r')
        i = open(d, 'r')
        j = open(e, 'r')
        a_str = f.read()
        b_str = g.read()
        c_str = h.read()
        d_str = i.read()
        e_str = j.read()
        f.close()
        g.close()
        h.close()
        i.close()
        j.close()
        self.words = dict(eval(a_str))
        self.word_lengths = dict(eval(b_str))
        self.stems = dict(eval(c_str))
        self.sentence_lengths = dict(eval(d_str))
        self.punctuation = dict(eval(e_str))
    
    # pt 4, pr 2
    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores measuring the similarity of self
            and other for each type of feature, making repeated calls to compare_dictionaries
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuation, self.punctuation)
        score = [word_score] + [word_lengths_score] + [stems_score] + [sentence_lengths_score] + [punctuation_score]
        return score
    
    # pt 4, pr 3
    def classify(self, source1, source2):
        """ compares the called TextModel object(self) to two other "source" TextModel objects
            (source1 and source 2) and determines which of these other TextModels is the most likely
            source of the called TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print('scores for ' + source1.name + ':' + str(scores1))
        print('scores for ' + source2.name + ':' + str(scores2))
        
        higher1 = 0
        higher2 = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                higher1 += 1
            elif scores1[i] < scores2[i]:
                higher2 += 1
        if higher1 > higher2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        elif higher2 > higher1:
            print(self.name + ' is more likely to have come from ' + source2.name)
        
# pt 1, pr 3 
def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list containing the 
        words in txt after it has been 'cleaned'. This function will b used when u need
        to process each word in a text individually, w/o having to worry abt punctuation
    """
    text = ''
    for i in range(len(txt)):
        if txt[i] != '.' and txt[i] != ',' and txt[i] != '?' and \
           txt[i] != '!' and txt[i] != ':' and txt[i] != ';' and txt[i] != '"':
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
    
# pt 3, pr 2
def stem(s): 
    """ accepts a string as a parameter. the function should return the stem of s.
    """
    word = ''
    if 'ing' in s:
        if s[-4:-3] == s[-5:-4]:
            word = s[:-4]
        else:
            word = s[:-3]
    elif 'er' in s:
        if s[-3:-2] == s[-2:-1]:
            word = s[:-3]
        elif s[-1] == 's':
            word = s[:-3]
        else:
            word = s[:-2]
    elif s[-1:] == 'y':
        if s == 'very':
            word = s
        word = s[:-1] + 'i'
    elif s[-3:] == 'ies':
        word = s[:-2]
    elif s[-1:] == 'e':
        if s == 'the':
            word = s
        else:
            word = s[:-1]
    elif s[-2:] == 'ed':
        word = s[:-2]
    elif s[-1:] == 's':
        if s[-2:] == 'es':
            word = s[:-2]
        elif s == 'is':
            word = s
        elif s == 'this':
            word = s
        else:
            word = s[:-1]
    elif s[-4:] == 'tion':
        word = s[:-3]
    elif s[-2:] == 'ly':
        if s[-3] == 'e':
            word = s[:-3]
        else:
            word = s[:-2]
    else:
        word = s
    return word

# pt 4, pr 1
def compare_dictionaries(d1, d2):
    """ takes two feature dictionaries d1 and d2 as inputs, and computes and returns 
        their log similarity score
    """
    score = 0
    total = 0 
    for i in d1:
        total += d1[i]
    for j in d2:
        if j in d1:
            score += (math.log(d1[j]/total)) * d2[j]
        else:
            score += (math.log(0.5/total)) * d2[j]
    return score

# pt 4 test function
def test():
    """ tests the TextModel Implementation on strings"""
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
    
# pt 5 test function        
def run_tests():
    """ tests the TextModel Implementation on text files """
    source1 = TextModel('greys anatomy script')
    source1.add_file('greys_anatomy_script.txt')

    source2 = TextModel('gossip girl script')
    source2.add_file('gossip_girl_script.txt')

    new1 = TextModel('greys anatomy scene')
    new1.add_file('greys_anatomy_end_scene.txt')
    print()
    new1.classify(source1, source2)

    # Add code for three other new models below.
    new2 = TextModel('gossip girl scene')
    new2.add_file('gossip_girl_end_scene.txt')
    print()
    new2.classify(source1, source2)
    
    new3 = TextModel('skins script')
    new3.add_file('skins_script.txt')
    print()
    new3.classify(source1, source2)
    
    new4 = TextModel('private practice script')
    new4.add_file('private_practice_script.txt')
    print()
    new4.classify(source1, source2)
    
    
