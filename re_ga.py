import string
import re
from random import choice, randint, sample

class Gene(object):
    def __init__(self, operator, value):
        self.value = value
        self.operator = operator
    def copy(self):
        return Gene(self.operator, self.value)
    
REOR = '|'
dataset = []

#data set is a list of dictionaries with the values
def fitness_test(ge, print_flag=False):
    
    global dataset
    total = 0.
    correct = 0.
    incorrect = 0.
    
    female_regex = ge.build_re()
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

    if print_flag is True:
        
        print 'RE : ' + female_regex
        #print 'Correct Guesses : ' + str(correct)
        #print 'Incorrect Guesses : ' + str(incorrect)
        #print 'Total Occurences : ' + str(total)
        #print 'Fitness Score : ' + str(score)
        print '% Accuracy : ' + str((correct / total))
    
    return ge, score

def generate_dataset():
    with open('names/yob1980.txt') as f:
        for line in f:
            name, gender, occurences = line.split(',')
            dataset.append({'name' : name,
                            'gender' : gender,
                            'occurences' : occurences})

#Utilities
def get_random_chars(floor, ceiling):
    r = range(randint(floor, ceiling))
    return ''.join([choice(string.ascii_lowercase) for _ in r])

def get_random_operator():
    #TODO feminine names are mostly defined by suffix, weight accordingly
    return choice(['^', '$'])

#Main GA class
class GeneratedExpression(object):

    def __init__(self, nodes):

        self.nodes = nodes
        
        if len(self.nodes) == 0:
            for x in xrange(0,randint(5,20)):
                v, o = get_random_chars(1,5), get_random_operator()
                self.nodes.append(Gene(o, v))
            
    def build_re(self):

        self.nodes = [node for node in self.nodes if node.value != '']
        startswith = [n.value for n in self.nodes if n.operator == '^']
        endswith = [n.value for n in self.nodes if n.operator == '$']
        
        return '(' + '|'.join(endswith) + ')$' + '|' + \
               '^(' + '|'.join(startswith) + ')'

    def branch_out(self):
        
        result = self.copy()

        x = randint(0, len(result.nodes) - 1)
        node = result.nodes[x]
        left_value = get_random_chars(1, 1) + node.value
        right_value = get_random_chars(1, 1) + node.value

        result.nodes[x] = Gene(get_random_operator(), left_value)
        result.nodes.insert(x + 1, Gene(get_random_operator(), right_value))
        return result
        
    def mutate(self):
        
        result = self.copy()
        node = choice(result.nodes)

        node.value = get_random_chars(0,3)
        node.operator = get_random_operator()
        
        return result

    def smart_mutate(self):
        
        result = self.copy()
        node = choice(result.nodes)
        value = get_random_chars(1,1) + node.value[1:]
        result.nodes.append(Gene(node.operator, value))
        
        return result
                         
    def splice(self, other):
        result = self.copy()
        result.nodes = sample(result.nodes, randint((len(result.nodes) - 1) / 5, (len(result.nodes) - 1) / 2)) + \
                       sample([n.copy() for n in other.nodes], randint((len(other.nodes) - 1)/ 5, (len(other.nodes) - 1) / 2))
        return result
        
    def copy(self):
        result = GeneratedExpression([x.copy() for x in self.nodes])
        return result
        
class Pool(object):

    def __init__(self, fitness, size=50, maxdepth=5):
        self.fitness = fitness
        self.ge = [GeneratedExpression([]) for _ in xrange(size)]
        self.generation = 0
        
    def run(self, number_of_generations=10):

        for gen in xrange(number_of_generations):
            self.ge = self.strategy(self.scores)
            self.generation += 1
            
        return self.scores

    @property
    def scores(self):
        scores = [self.fitness(ge) for ge in self.ge]
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
            mutations = [a.mutate() for a in top]
            smart_mutations = [a.smart_mutate() for a in top]
            spliced = [a.splice(b) for a, b in zip(top, sample(top, len(top)))]
            branch = [a.branch_out() for a in top]

            print #print a linebreak
            print 'Generation : ' + str(self.generation)
            fitness_test(scores[0][0], print_flag=True)

            return top + mutations + branch + spliced + smart_mutations

    pool = MyPool(fitness_test)
    print pool.run(10000) #run x generatations and print the results
