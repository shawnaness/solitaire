#!/usr/bin/env python
import sys
import pyCardDeck
from colorama import init, Fore, Style

class Solitaire:

	def __init__(self):
		init() # colorama
		self.deck = pyCardDeck.Deck()
		self.deck.load_standard_deck()
		self.deck.shuffle()

		self.foundations = {}
		self.foundations["Hearts"] = []
		self.foundations["Clubs"] = []
		self.foundations["Diamonds"] = []
		self.foundations["Spades"] = []

		self.tableau = []
		self.numHiddenTableau = []

		for i in range(7):
			self.tableau.append([])
			self.numHiddenTableau.append(i)
		for i in range(7):
			for j in range(i, 7):
				self.tableau[j].append(self.deck.draw())

		self.hand = []
		self.discard = []

		self.ranks = {
			"A": 1, "2": 2, "3": 3, "4": 4,
			"5": 5, "6": 6, "7": 7, "8": 8,
			"9": 9, "10": 10, "J": 11,
			"Q": 12, "K": 13
		}
		self.shortSuit = {
			"Hearts": "H", "Clubs": "C",
			"Diamonds": "D", "Spades": "S"
		}

	def toColorString(self, card):
		if card.suit == "Hearts" or card.suit == "Diamonds":
			return Fore.RED + card.rank + self.shortSuit[card.suit] + Style.RESET_ALL
		else:
			return card.rank + self.shortSuit[card.suit]

	def printHand(self):
		if self.hand:
			toPrint = "(top) "
			for card in self.hand:
				toPrint += self.toColorString(card) + " "
			toPrint += "(bottom)"
			return toPrint
		else:
			return "empty"

	def printFoundations(self):
		print("Foundations:")
		for key, value in self.foundations.items():
			if value:
				print(key + ": " + self.toColorString(value[-1]))
			else:
				print(key + ": ____")
		print()

	def printTableau(self):
		print("Tableau:")
		for i in range(len(self.tableau)):
			print(i, end=" ")
			pile = self.tableau[i]
			if len(pile) <= self.numHiddenTableau[i]:
				self.numHiddenTableau[i] = len(pile) - 1

			for j in range(len(pile)):
				if j < self.numHiddenTableau[i]:
					print("|", end="\t")
				else:
					print(self.toColorString(pile[j]), end="\t")
			print()

	def printField(self):
		print("Hand:", self.printHand())
		print("Deck:", len(self.deck))
		print("Discard:", len(self.discard))
		print()

		self.printFoundations()
		self.printTableau()

	def validFoundationMove(self, card):
		if self.foundations[card.suit]:
			last = self.foundations[card.suit][-1]
			return (self.ranks[card.rank] - self.ranks[last.rank]) == 1
		else:
			return self.ranks[card.rank] == 1

	def validTableauMove(self, index, card):
		pile = self.tableau[index]
		if pile:
			last = pile[-1]
			numberValid = (self.ranks[last.rank] - self.ranks[card.rank]) == 1
			if (last.suit == "Hearts" or last.suit == "Diamonds"):
				colorValid = (card.suit == "Clubs" or card.suit == "Spades")
			else:
				colorValid = (card.suit == "Hearts" or card.suit == "Diamonds")
			return numberValid and colorValid
		else:
			return self.ranks[card.rank] == 13

	def drawCard(self):
		self.discard.extend(self.hand)
		self.hand.clear()
		if len(self.deck) < 3:
			print('Deck empty. Resetting discard...')
			self.deck.add_many(self.discard)
			self.discard.clear()
		numDraw = min(3, len(self.deck))	
		for i in range(numDraw):
			self.hand.append(self.deck.draw())


	def playHand(self):	
		if self.hand:
			card = self.hand[0]
			place = input('Type a pile 0-6 or \'foundation\' (or \'f\') to place the ' + 
				card.name + ': ')
			if (place == "foundation" or place == "f"):
				if (self.validFoundationMove(card)):
					self.foundations[card.suit].append(self.hand.pop(0))
				else:
					print("Invalid.")
			elif (place.isdigit()): # tests if is number
				if (int(place) >= 0 and int(place) <= 6):
					if (self.validTableauMove(int(place), card)):
						self.tableau[int(place)].append(self.hand.pop(0))
					else:
						print("Invalid.")
				else:
					print("Invalid.")
			else:
				print("Invalid.")
		else:
			print("Invalid.")

	def moveCard(self, move):
		if (move >= 0 and move <= 6):
			pile = self.tableau[move]
			pileOrCard = input("Type \'card\' to move the bottommost card " +
				"or \'pile\' to move the full visible pile: ")
			if (pileOrCard == "card"):
				card = pile[-1]
				place = input('Type a pile 0-6 or \'foundation\' (or \'f\') to place the ' + 
					card.name + ': ')
				if (place == "foundation" or place == "f"):
					if (self.validFoundationMove(card)):
						self.foundations[card.suit].append(pile.pop())
					else:
						print("Invalid.")
				elif (place.isdigit()): # tests if is number
					if (int(place) >= 0 and int(place) <= 6):
						if (int(place) != move): # if == move, don't do anything
							if (self.validTableauMove(int(place), card)):
								self.tableau[int(place)].append(pile.pop())
							else:
								print("Invalid.")
					else:
						print("Invalid.")
				else:
					print("Invalid.")
			elif (pileOrCard == "pile"):
				visiblePile = pile[self.numHiddenTableau[int(move)]:]
				place = input('Type a pile 0-6 to place the pile: ')
				if (int(place) >= 0 and int(place) <= 6):
					if (int(place) != move):
						if (self.validTableauMove(int(place), visiblePile[0])):
							self.tableau[int(place)].extend(visiblePile)
							self.tableau[move] = pile[:self.numHiddenTableau[move]]
						else:
							print("Invalid.")
				else:
					print("Invalid.")
			else:
				print("Invalid.")
		else:
			print("Invalid.")


	def makeMove(self, move):
		if (move == "draw"):
			self.drawCard()
		elif (move == "hand"):
			self.playHand()
		elif (move.isdigit()): # tests if is number
			self.moveCard(int(move))
		elif (move == "exit"):
			quit()
		else:
			print("Invalid move. Try again!")
		print("------------------------------------------------")


	def checkWin(self):
		return (len(self.foundations["Hearts"]) == 13 and
			len(self.foundations["Clubs"]) == 13 and
			len(self.foundations["Diamonds"]) == 13 and
			len(self.foundations["Spades"]) == 13)
				
	def solitaire(self):
		print("Welcome to Solitaire!")
		print("------------------------------------------------")
		
		gameWon = False
		while (not gameWon):
			self.printField()
			move = input('Type \'draw\' to draw from deck,' +
				' \'hand\' to play the top card from your hand,' +
				' a number 0-6 to move a card from the table, ' +
				' or \'exit\': ')
			self.makeMove(move)
			gameWon = self.checkWin()
		print("Yay! You won!")
		input("Press enter to quit: ")
			


def main():
	game = Solitaire()
	game.solitaire()

if __name__ == "__main__": main()
