import itertools
from functions import *

def evaluate_a_guess(guess:str,max_valids:int,wordsToRun:set[str],color_states):
		valid_states = 0
		false_states = 0
		biggest_group = 0
		for states in color_states:
			localPossibleSolutions = list(wordsToRun.copy())

			parsedTurn = turnInput(False,guess,states)
			localPossibleSolutions = remove_words_with_wrongly_positioned_letters_green(parsedTurn[0],localPossibleSolutions)
			localPossibleSolutions = remove_words_with_wrongly_postioned_letters_yellow(parsedTurn[1],localPossibleSolutions)
			localPossibleSolutions = removeWordsWithWrongAmountOfLetters(parsedTurn[2],localPossibleSolutions)

			if len(localPossibleSolutions)>=1:
				valid_states+=1
				#Maybe not because a word can be in two different groups
				#Like having two yellows and another one with two greens
				wordsToRun.difference_update(localPossibleSolutions)
				biggest_group = max(biggest_group,len(localPossibleSolutions))
				if not wordsToRun:
					break
			else:
				false_states+=1
				if len(color_states)-max_valids<false_states:
					#Means there are to many false states to be better
					break

		return valid_states,biggest_group

def maxGroups():
	#All possible color states
	color_states = list(itertools.product("wyg",repeat=5))

	with open(usablePath("./words_to_run.txt"),"r") as file:
		unchangeable_words_to_run=set(file.read().splitlines())

	with open(usablePath("./wordle_words.txt"),"r") as file:
		all_words=file.read().splitlines()

	maxValidStates = 0
	best_words = {}

	print(f"Finding the best word for you to play")
	for guess in all_words:
		valid_states,biggest_group = evaluate_a_guess(guess,maxValidStates,unchangeable_words_to_run.copy(),color_states)

		if valid_states>maxValidStates:
			print(f"Found better : {guess}, groups={valid_states}")
			maxValidStates=valid_states
			best_words={guess:biggest_group}
		elif valid_states==maxValidStates:
			best_words[guess]=biggest_group

	
	minimum = float("inf")
	bestWord = ""
	for word in best_words:
		if best_words[word]<minimum:
			minimum = best_words[word]
			bestWord = word
	print(f"You should play {bestWord}, biggestGroup={best_words[bestWord]}")