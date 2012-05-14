#To run the script: python match-date.py. To run tests: python match-date.py -t
#The WORST case scenarion is tested. 

import random, argparse, unittest, sys, argparse

n = 100

def girlsBoys(_random=True):
	#generate boys list
	boys = [('boy'+str(i+1),i) for i in range(n)]

	#generate girls list and randomly sort the list. 
	#Random shuffling is done  because order matters, 
	#the first girls in the list get to choose from a larger list of boys.
	girls = random.shuffle(['girl'+str(i+1) for i in range(n)])

	#generate rankings
	rankings = [i+1 for i in range(n)]

	#girls don't know what they want and make boys lists with random preferences
	girlsPickBoys = {}
	for girl in girls:
		if _random:
			random.shuffle(rankings)
		for i in range(n):
			if i==0:
				girlsPickBoys[girl] = {}
			girlsPickBoys[girl][rankings[i]] = boys[i]
	return boys,girls,girlsPickBoys,rankings

def cupidoMatches(boys,girls,girlsPickBoys,rankings):
	#matches happen!
	pickedBoys = []
	matchesScore = 0
	matches = []
	for girl in girls:
		#We explore all the best rankings starting from 1 (i+1). If a boy is not already picked, it will be matched with the girl
		for i in range(n):
			match = girlsPickBoys[girl][i+1]
			if match not in pickedBoys:
				pickedBoys.append(match)
				matches.append((girl,match[0],i+1))
				matchesScore+=i+1
				break
			else:
				#if a boy is picked we don't care, we want to loop to the next ranking.
				pass
	return matchesScore,matches

def run():
	#A simple handy function to run the entire script, it runs when the script is called without the argument '-t'
	boys,girls,girlsPickBoys,rankings = girlsBoys(_random=True)
	matchesScore, matches = cupidoMatches(boys,girls,girlsPickBoys,rankings)
	print 'The matches score is:%s\n'%matchesScore
	print 'The matches are:\n',matches

#Testing it all works
class TestSequenceFunctions(unittest.TestCase):
	
	def test_DataCreation(self):
		boys,girls,girlsPickBoys,rankings = girlsBoys(_random=False)
		assert len(boys)==len(girls) and len(girls) == len(rankings) and len(rankings)==len(girlsPickBoys.keys())
	
	def test_MatchesUnique(self):
		#Checking if the matches are unique and if boys and girls are equal to n
		boys,girls,girlsPickBoys,rankings = girlsBoys()
		matchesScore, matches = cupidoMatches(boys,girls,girlsPickBoys,rankings)
		boys = set([match[1] for match in matches])
		girls = set([match[0] for match in matches])
		assert len(girls)==len(boys) and len(boys)==n

	def test_WORST(self):
		#In the worst case scenario all girls rank the boys in the same way, this means no randomization of rankings
		boys,girls,girlsPickBoys,rankings = girlsBoys(_random=False)
		matchesScore, matches = cupidoMatches(boys,girls,girlsPickBoys,rankings)
		assert matchesScore == n*(n+1)/2

#Add a command line option to run the tests
parser = argparse.ArgumentParser(description='Run tests')
parser.add_argument('-t',action='store_true')
args = parser.parse_args()
if args.t==True:
	unittest.main(argv=[sys.argv[0]])
else:
	run()
