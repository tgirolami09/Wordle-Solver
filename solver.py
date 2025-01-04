from findMaxGroups import maxGroups
from functions import *

possibleSolutions = wordListChoice()
print(f"There are {len(possibleSolutions)} possible solutions")  
letters_in_solution = set() 
help_user(possibleSolutions)

for turn in range(6):

	parsedUserTurn = turnInput()

	possibleSolutions = remove_words_with_wrongly_positioned_letters_green(parsedUserTurn[0],possibleSolutions)
	possibleSolutions = remove_words_with_wrongly_postioned_letters_yellow(parsedUserTurn[1],possibleSolutions)
	possibleSolutions = removeWordsWithWrongAmountOfLetters(parsedUserTurn[2],possibleSolutions) 

	if len(possibleSolutions) > 1:
		print(" ,".join(possibleSolutions))
		print(f"There are {len(possibleSolutions)} words left")
		with open(usablePath("./words_to_run.txt"),"w") as f:
			f.writelines("\n".join(possibleSolutions)) 		

		#Later in cpp instead of python
		maxGroups()

	elif len(possibleSolutions) == 1:
		#If the list was restricted go to a larger one to be sure
		print("The solution should be :",possibleSolutions[0])
		break

	elif len(possibleSolutions) == 0:
		print("I can't find a solution")
		break