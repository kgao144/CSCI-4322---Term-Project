import logging
import random
import re
from collections import namedtuple

# Fix Python2/Python3 incompatibility
try: input = raw_input
except NameError: pass

log = logging.getLogger(__name__)
# error checking variable declaration
d = 60
z = 200
b = 800
c = 900

# key class and components
class Key:
    print("Key")
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps

# decomp class and components
class Decomp:
    print("Decomp")
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0

# eliza class and components
class Eliza:
    print("Eliza")
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []

        self.keynum = 0
        self.storedkey = []

# load function to read from doctor.txt
    def load(self, path):
        key = None
        decomp = None
        
        print("Load")

        with open(path) as file:
            for line in file:
                if not line.strip():
                    continue
                tag, content = [part.strip() for part in line.split(':')]
                if tag == 'initial':
                    self.initials.append(content)
                elif tag == 'final':
                    self.finals.append(content)
                elif tag == 'quit':
                    self.quits.append(content)
                elif tag == 'pre':
                    parts = content.split(' ')
                    self.pres[parts[0]] = parts[1:]
                elif tag == 'post':
                    parts = content.split(' ')
                    self.posts[parts[0]] = parts[1:]
                elif tag == 'synon':
                    parts = content.split(' ')
                    self.synons[parts[0]] = parts
                elif tag == 'key':
                    parts = content.split(' ')
                    word = parts[0]
                    weight = int(parts[1]) if len(parts) > 1 else 1
                    key = Key(word, weight, [])
                    self.keys[word] = key
                elif tag == 'decomp':
                    parts = content.split(' ')
                    save = False
                    if parts[0] == '$':
                        save = True
                        parts = parts[1:]
                    decomp = Decomp(parts, save, [])
                    key.decomps.append(decomp)
                elif tag == 'reasmb':
                    parts = content.split(' ')
                    decomp.reasmbs.append(parts)

# match decomp r for specific results in decomposition 
    def _match_decomp_r(self, parts, words, results):
        x= 50
        x= x+1
        print(str(x) + " match decomp r")
        if not parts and not words:
            return True
        if not parts or (not words and parts != ['*']):
            return False
        if parts[0] == '*':
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self._match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith('@'):
            root = parts[0][1:]
            if not root in self.synons:
                raise ValueError("Unknown synonym root {}".format(root))
            if not words[0].lower() in self.synons[root]:
                return False
            results.append([words[0]])
            return self._match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self._match_decomp_r(parts[1:], words[1:], results)

# initial match decomp function
    def _match_decomp(self, parts, words):
        results = []
        if self._match_decomp_r(parts, words, results):
            print(str(d) + " match decomp")
            return results
        return None

# calls the next indexed phrase of doctor.txt
    def _next_reasmb(self, decomp):
        
        z+1
        print(str(z) + " next reasmb")

        index = decomp.next_reasmb_index
        print("The index for reassem: " + str(index))
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

# reassemble function for string rewording
    def _reassemble(self, reasmb, results):
        output = []
        i = 0
        for reword in reasmb:
            i= i+1
            
            if not reword:
                continue
            if reword[0] == '(' and reword[-1] == ')':
                index = int(reword[1:-1])
                if index < 1 or index > len(results):
                    raise ValueError("Invalid result index {}".format(index))
                insert = results[index - 1]
                for punct in [',', '.', ';']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
            else:
                output.append(reword)

        print("response word count = " + str(i))
        return output

# sub function to lower case words inputed by user
    def _sub(self, words, sub):
        a = 700
        a= a+1
        print(str(a) + " sub")

        output = []
        for word in words:
            word_lower = word.lower()
            if word_lower in sub:
                output.extend(sub[word_lower])
            else:
                output.append(word)
        return output

# uses the match key function to call decomposition and reassemble per key
    def _match_key(self, words, key):
        b+1
        print(str(b) + " match key")
        
        self.keynum = self.keynum+1
        print("KEY IS '" + str(key.word) + "' KEY NUM: " + str(self.keynum))

        
        for decomp in key.decomps:
            results = self._match_decomp(decomp.parts, words)
            if results is None:
                log.debug('Decomp did not match: %s', decomp.parts)
                continue
            log.debug('Decomp matched: %s', decomp.parts)
            log.debug('Decomp results: %s', results)
            results = [self._sub(words, self.posts) for words in results]
            log.debug('Decomp results after posts: %s', results)
            reasmb = self._next_reasmb(decomp)
            log.debug('Using reassembly: %s', reasmb)
            if reasmb[0] == 'goto':
                goto_key = reasmb[1]
                if not goto_key in self.keys:
                    raise ValueError("Invalid goto key {}".format(goto_key))
                log.debug('Goto key: %s', goto_key)
                return self._match_key(words, self.keys[goto_key])
            output = self._reassemble(reasmb, results)
            if decomp.save:
                self.memory.append(output)
                log.debug('Saved to memory: %s', output)
                continue
            return output
        return None  

# builds response based off of previous called functions for matching keys and decomps
    def respond(self, text):
        c+1
        print(str(c) + " respond")

        if text.lower() in self.quits:
            return None

        text = re.sub(r'\s*\.+\s*', ' . ', text)
        text = re.sub(r'\s*,+\s*', ' , ', text)
        text = re.sub(r'\s*;+\s*', ' ; ', text)
        log.debug('After punctuation cleanup: %s', text)

        words = [w for w in text.split(' ') if w]
        log.debug('Input: %s', words)

        words = self._sub(words, self.pres)
        log.debug('After pre-substitution: %s', words)

        keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys]
        keys = sorted(keys, key=lambda k: -k.weight)
        
        log.debug('Sorted keys: %s', [(k.word, k.weight) for k in keys])

        #display keyword and weight
        print('Sorted keys: %s'% [(k.word, k.weight) for k in keys])

        output = None

        for key in keys:
            if keys[0].weight < 999:
                    output = self._match_key(words, key)
            if output:
                    log.debug('Output from key: %s', output)
                    break
            else:
                output = self._match_key(words, keys[1])
            
# context recognization to check for the second highest phrase
        if not output:
            if self.memory:
                index = random.randrange(len(self.memory))
                output = self.memory.pop(index)
                log.debug('Output from memory: %s', output)
            else:
                output = self._next_reasmb(self.keys['xnone'].decomps[0])
                log.debug('Output from xnone: %s', output)

        return " ".join(output)

## definitions
    def initial(self):
        print("Define initial self")
        return random.choice(self.initials)

    def final(self):
        print("Define final self")
        return random.choice(self.finals)

    def run(self):
        print("Initial")
        print(self.initial())

        while True:
            sent = input('> ')

            output = self.respond(sent)
            if output is None:
                break

            print(output)

        print(self.final())


def main():
    eliza = Eliza()
    eliza.load('doctor.txt')
    eliza.run()

if __name__ == '__main__':
    logging.basicConfig()
    main()
