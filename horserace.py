#!/usr/bin/python

#This is a program to calculate payouts for horse racing. The user is prompted
#for the names of the horses, then the names of the bettors, then for any number
#of bets. At the end, it displays the winnings of each bettor.

#It uses parimutuel-style betting, where the odds for each horse are calculated
#by dividing the total amount bet on all the horses by the amount bet on the
#specific horse. The people who have bet on a winning horse divide up all the 
#money bet in proportion to the relative amount of their respective bets on the 
#winning horse.

#error handling can be improved, currently inputs with extra spaces can cause errors

#Reproducible bug 1:
#call the horses a, b, and c
#call the bettors x, y, and z
#enter a couple valid bets, but don't bet on all the horses yet
#enter a malformed bet with an extra space before the bet amount
#program will say the proper error message
#then it will say that a horse still needs a bet (technically true but not the right response here)

#Reproducible bug 2 (related to 1):
#call the horses a, b, and c
#call the bettors x, y, and z
#enter a few valid bets, making sure to bet on all the horses this time
#enter a malformed bet with an extra space before the bet amount
#program will respond with the correct error message
#then immediately ask for the name of the winning horse.

#I believe these are both due to something I'm doing wrong while breaking out of the first
#while True: loop in main() and possibly with how I split the input in the first
#line of main().

#If you run the program with other malformed bets (i.e. iojwefaoi wafejo ewfjoawf waf 10)
#it will do a similar thing. I'll fix it as soon as I figure out what's going on.

total_bet = 0
horses = {} #dictionaries to store (name, object) labels for easier reference
bettors = {}

class Horse(object):
    def __init__(self, name):
        global horses
        horses[name] = self
        self.name = name
        self.odds = 1
        self.bets_applied = 0

    def calc_odds(self):
        if not self.bets_applied:
            return None #nobody will win
        self.odds = float(total_bet) / self.bets_applied

class Bettor(object):
    def __init__(self, name):
        global bettors
        bettors[name] = self
        self.name = name
        self.bets = {} #dictionary of (horse.name, bet) pairs
        self.winnings = 0

    def place_bet(self, horse_name, amount):
        global total_bet
        if horse_name in self.bets:
            self.bets[horse_name] += amount
        else:
            self.bets[horse_name] = amount
        total_bet += amount
        horses[horse_name].bets_applied += amount
        for horse in horses.values(): 
            horse.calc_odds() #all the odds need to be recalculated when total_bet changes

def payout(winner):
    for bettor in bettors.values():
        if winner in bettor.bets:
            bettor.winnings = horses[winner].odds * bettor.bets[winner]
        else:
            bettor.winnings = 0
        print "%s won $%.2f" %(bettor.name, bettor.winnings)

def get_bets(bettor_names, horse_names):
    while True:
        bet = raw_input("Enter a bet (bettor horse amount) or enter \"done\" when done: ").strip().split(' ')
        if bet[0].lower().strip() == "done":
            break
        elif len(bet) != 3:
            print "You must enter a bettor's name, followed by a horse, followed by the amount you wish to bet."
            return False
        else:
            (b_name, h_name, bet_amount) = bet
        if b_name not in bettor_names:
            print "That's not the name of a bettor."
        elif h_name not in horse_names:
            print "That's not the name of a horse."
        elif not bet_amount.isdigit() or bet_amount < 0:
            print "Please enter a positive number for the bet."
        else:
            bet_amount = int(bet_amount)
            bettors[b_name].place_bet(h_name, bet_amount)
    return True

def check_bets():
    for horse in horses.values():
        if not horse.bets_applied:
            print "%s needs a bet" % (horse.name)
            return False
    return True

def main():
    horse_names = raw_input("Enter each horse's name, separated by a space: ").strip().split(' ')

    for horse_name in horse_names:
        Horse(horse_name)

    bettor_names = raw_input("Enter each bettor's name, separated by a space: ").strip().split(' ')

    for bettor_name in bettor_names:
        Bettor(bettor_name)

    while True:
        #something isn't right here. It shouldn't necessarily break out entirely
        #get_bets is returning True when it shouldn't.
        #get_bets should restart from where it left off if there's an error
        if get_bets(bettor_names, horse_names):
            break
        if check_bets():
            break

    while True:
        winner = raw_input("Enter the name of the winning horse: ")
        if winner in horses:
            payout(winner)
            break
        else:
            print "That's not the name of a horse."

if __name__ == "__main__":
    main()