import string
import re
from random import choice, randint, sample

REOR = '|'


dataset = []
generation = 0

#data set is a list of dictionaries with the values
def fitness_test(female_regex):
    global dataset
    total = 0.
    correct = 0.
    incorrect = 0.
    
    running_time = 0.

    regex = re.compile(female_regex)

    for record in dataset:
        result = 'M'
        occurences = int(record['occurences'])
        total += occurences
        
        if re.search(regex, record['name']) is not None:
            result = 'F'

        if record['gender'] == result:
            correct += occurences
        else:
            incorrect += occurences
            

    score = ((correct - incorrect) / total + 1.0) / (len(female_regex) **.001)
    
    return score

def generate_dataset():
    with open('names/yob1980.txt') as f:
        for line in f:
            name, gender, occurences = line.split(',')
            dataset.append({'name' : name,
                            'gender' : gender,
                            'occurences' : occurences})

def accuracy(femaleRegex):
    global generation
    print 'Generation : ' + str(generation)
    generation = generation + 1
    totalOccurences=0
    correctGuesses=0
    incorrectGuesses=0
    
    totalRunningTime = 0

    regex = re.compile(femaleRegex)
    for record in dataset:
        result = 'M'
        totalOccurences += int(record['occurences'])
        
        if re.search(regex, record['name']) is not None:
            result = 'F'

        if record['gender'] == result:
            correctGuesses += int(record['occurences'])
        else:
            incorrectGuesses += int(record['occurences'])

    fitnessScore =  (((float(correctGuesses) - float(incorrectGuesses)) / float(totalOccurences)) + 1.0) / len(femaleRegex) **.001
    
    print 'RE : ' + femaleRegex
    print 'Correct Guesses : ' + str(correctGuesses)
    print 'Incorrect Guesses : ' + str(incorrectGuesses)
    print 'Total Occurences : ' + str(totalOccurences)
    print 'Fitness Score : ' + str(fitnessScore)
    print '% Accuracy : ' + str(float(correctGuesses) /float(totalOccurences))


#Utilities
def get_random_chars(floor,ceiling):
    r = range(randint(floor, ceiling))
    return ''.join([choice(string.ascii_lowercase) for _ in r])

def get_random_number(floor, ceiling):
    return randint(floor,ceiling)

def get_sample(how_many, nodes):
    return sample(nodes, how_many)

def copy(ge):
    return ge._copy()

#GA operations
def mutate(ge):
    return ge._mutate()

def smart_mutate(ge):
    return ge._smart_mutate()

def branch_out(ge):
    return ge._branch_out()

def splice(ge, foreign_nodes):
    return ge._splice(foreign_nodes)

#Main GA class
class GeneratedExpression(object):

    def __init__(self, nodes):
        self.nodes = nodes
        if len(self.nodes) == 0:
            for x in xrange(0,get_random_number(5,20)):
                self.nodes.append(get_random_chars(1,5))
            
    def build_re(self):
        self.nodes = [node for node in self.nodes if node != '']
        return '(' + '|'.join(self.nodes) + ')$'

    def _branch_out(self):
        result = self._copy()
        x = get_random_number(0,len(result.nodes)  - 1)
        left_value = get_random_chars(1,1) + result.nodes[x]
        right_value = get_random_chars(1,1) + result.nodes[x]

        result.nodes[x] = left_value
        result.nodes.insert(x + 1, right_value)
        return result
        
    def _mutate(self):
        result = self._copy()
        x = get_random_number(0,len(self.nodes) - 1)
        result.nodes[x] = get_random_chars(0,3)
        return result

    def _smart_mutate(self):
        result = self._copy()
        x = get_random_number(0,len(self.nodes) - 1)
        result.nodes.append(get_random_chars(1,1) + result.nodes[x][1:])
        return result
            
                             
    def _splice(self, foreign_ge):
        result = self._copy()
        result.nodes = get_sample(get_random_number((len(result.nodes)  - 1) / 5 , (len(result.nodes)- 1) / 2 ),result.nodes) + get_sample(get_random_number((len(foreign_ge.nodes) - 1)/ 5 , (len(foreign_ge.nodes)  - 1) / 2 ),foreign_ge.nodes)
        return result
        
    def _copy(self):
        result = GeneratedExpression([x for x in self.nodes])
        return result
        
class Pool(object):

    def __init__(self, fitness, size=50, maxdepth=5):
        self.fitness = fitness
        self.ge = [GeneratedExpression([]) for _ in xrange(size)]

    def run(self, number_of_generations=10):

        for gen in xrange(number_of_generations):
            self.ge = self.strategy(self.scores)
            
        return self.scores

    @property
    def scores(self):
        scores = [(ge, self.fitness(ge.build_re())) for ge in self.ge]
        return sorted(scores, key=lambda t: t[1], reverse=True)
    
    def strategy(self, scores):
        
        raise NotImplemented

if __name__ == "__main__":
    print 'Generating Dataset'
    generate_dataset()
    print 'Dataset generated records returned : ' + str(len(dataset))
    
    class MyPool(Pool):

        def strategy(self, scores):
            top = [a for a, s in scores[:len(scores)/5]]
            mutations = map(mutate, top)
            smart_mutations = map(smart_mutate, top)
            spliced = [splice(a, b) for a, b in zip(top, sample(top, len(top)))]
            branch = map(branch_out, top)
            
            accuracy(scores[0][0].build_re())
            
            return top + mutations + branch + spliced + smart_mutations

    pool = MyPool(fitness_test, size = 50)
    print pool.run(1000) #run x generatations and print the results
