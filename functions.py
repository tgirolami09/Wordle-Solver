import os

class Letter:
	def __init__(self) -> None:
		self.count = 0
		self.certaintyOfCount = False #Unsure

def usablePath(fileRelativePath:str):
	scriptAbsolutePath = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(scriptAbsolutePath, fileRelativePath)

def wordListChoice():
	whatListToUse = input("Do you want the shorter word list (y or n).\nIt makes it faster and only contains the most probable words : ")
	if whatListToUse.lstrip().rstrip().lower() == "y":
		print("Using short list")
		with open (usablePath("./wordleMostProbableThird.txt"),"r") as file:
			return file.read().splitlines()
	else:
		print("Using entire list")
		with open(usablePath("./wordle_words.txt"),"r") as file:
			return file.read().splitlines()

def turnInput(forUser=True,*args:tuple[list[str],list[str]]):
	if forUser:
		guess = list(input("Give me your guess in lowercase letters : ").replace(" ",""))
		states = list(input("Give me the color of the letters in your guess 'w for grey' 'y for yellow' and 'g for green' : ").replace(" ",""))
	else:
		guess = args[0]
		states = args[1]

	positionedRight = {}
	positionedWrong = {}
	letterCount = {letter:Letter() for letter in set(guess)}
	for index,state in enumerate(states):
		letter = guess[index]
		if state == "w":
			letterCount[letter].certaintyOfCount = True
		elif state == "y":
			letterCount[letter].count += 1
			positionedWrong[index]=letter
		elif state == "g":
			letterCount[letter].count += 1
			positionedRight[index]=letter
			

	return (positionedRight,
			positionedWrong,
			letterCount,)

def remove_words_with_wrongly_positioned_letters_green(positioning_right:dict,words:list):
	for index in positioning_right:
		letter = positioning_right[index]
		words = [mot for mot in words if mot[index]==letter]
	return words

def remove_words_with_wrongly_postioned_letters_yellow(positioning_wrong:dict,words:list):
	for index in positioning_wrong:
		letter = positioning_wrong[index]
		words = [mot for mot in words if mot[index]!=letter]
	return words

def removeWordsWithWrongAmountOfLetters(letterCount:dict[str,Letter],words:list[str]):
	for letter in letterCount:
		words = [word for word in words if (word.count(letter)==letterCount[letter].count and letterCount[letter].certaintyOfCount) 
										or (word.count(letter)>=letterCount[letter].count and not letterCount[letter].certaintyOfCount)]
	return words

def help_user(words:list):
	"""
	Gives the user what word(or words)they should play
	Fast and not so good
	"""

	alphabet = list("abcdefghijklmnopqrstuvwxyz")
	dct = {}
	for letter in alphabet:
		dct[letter] = 0
	for word in words:
		for letter in word:
			dct[letter]+=1
	max_values = [0]*5
	max_values_letter = [""]*5
	for key in dct:
		if dct[key] > min(max_values):
			max_values_letter.pop(max_values.index(min(max_values)))
			max_values.pop(max_values.index(min(max_values)))
			max_values.append(dct[key])
			max_values_letter.append(key)

	tookeep = []
	value = max(max_values)
	letter = max_values_letter[max_values.index(value)]
	for word in words:
		if letter in word:
			tookeep.append(word)


	for value in max_values:
		if value != max(max_values) and len(tookeep) > 1:
			letter = max_values_letter[max_values.index(value)]
			index =-1
			while index != len(tookeep)-1 and len(tookeep) > 1:
				index+=1
				word = tookeep[index]
				if letter not in word:
					tookeep.pop(index)
					index-=1

		elif len(tookeep) == 1:
			break

	if len(tookeep) == 1:
		print("You should play :",tookeep[0])
	else:
		print("You should play :" ,end=" ")
		for word in tookeep:
			if word != tookeep[-1]:
				print(word,end=" or ")
			else:
				print(word)