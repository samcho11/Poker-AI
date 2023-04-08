import numpy as np
from statistics import mode
from copy import copy

# output deck[num,suit], len(deck) = 52 *2
# deck = [2,0,3,0,4,0, ..., 13,0,14,0,2,1, ... 14,3]
def generate_deck() -> list:
    # suit = [0,1,2,3] = ["C","D","H","S"]
    # num = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    deck = np.zeros(13*4*2)
    for j in range(4):
        for i in range(13):
            deck[i*2 + j*13*2] = i+2
            deck[i*2+1 + j*13*2] = j
    return deck

# User interface: input the number of players
# output: number of player
def num_player_input() -> int:
    print("Enter number of players(Max 8): ")
    num_player = input()
    while num_player not in ["1","2","3","4","5","6","7","8"]:
        print("Please enter valid number of players")
        print("Enter number of players(Max 8): ")
        num_player = input()
    print("Number of player: " + num_player)
    return int(num_player)

# Randomly choose (5 + num_player) cards from a deck
# Input: number of players, deck
# Output: drawn card, [num, suit], len(drawn_card) = num_player*2 +5
def shuffle(num_player:int, deck:list)->list:
    draw = np.random.choice(52, size=(num_player*2 +5),replace=False)
    drawn_card = np.zeros((num_player*2 +5)*2)
    for i in range(num_player*2 +5):
        drawn_card[i*2] = deck[draw[i]*2]
        drawn_card[i*2+1] = deck[draw[i]*2+1]
    return drawn_card

# Build a class of grading the hands 
class Check():
    # Input: my_card(list): hands of a single player + board, len(my_card) = 7*2
    # Output: the score of the combination
    # Straight flush   - score:9
    # Four of a kind   - score:8
    # Full house       - score:7
    # Flush            - score:6
    # Straight         - score:5
    # Triple           - score:4
    # Two pair         - score:3
    # One pair         - score:2
    # High             - score:1
    def evaluate(self, my_card):
        my_num = my_card[::2]
        my_suit = my_card[1::2]
        if self.check_fourcard(my_num):
            return 8
        if self.check_fullhouse(my_num):
            return 7
        if self.check_flush(my_suit):
            if self.check_straightflush(my_num,my_suit):
                return 9
            else: 
                return 6
        if self.check_straight(my_num):
            return 5
        if self.check_triple(my_num):
            return 4
        if self.check_twopair(my_num):
            return 3
        if self.check_onepair(my_num):
            return 2
        else:
            return 1
        
    def check_fourcard(self, my_num):
        if my_num.count(mode(my_num)) == 4:
            return True
        return False
    
    # By hierchy, assume there is no four of a kind
    def check_fullhouse(self, my_num):
        if my_num.count(mode(my_num)) == 3:
            triple = mode(my_num)
            temp_num = my_num.copy()
            # remove 2 of the triple to find another pair 
            temp_num.remove(triple)
            temp_num.remove(triple)
            if temp_num.count(mode(temp_num)) == 2:
                return True
        return False
    
    def check_flush(self, my_suit):
        if my_suit.count(mode(my_suit)) >= 5:
            return True
        return False
    
    def check_straight(self, my_num):
        # remove duplicate by using dict
        my_num_no_dup = list(dict.fromkeys(my_num))
        my_num_no_dup.sort()
        count = 1
        max_count = 1
        temp = int(my_num_no_dup[0])
        for i in range(len(my_num_no_dup)-1):
            if temp == int(my_num_no_dup[i+1]) - 1:
                count += 1
                temp = int(my_num_no_dup[i+1])
                if count >= max_count:
                    max_count = count
            else:
                temp = int(my_num_no_dup[i+1])
                count = 1     
        # Check A bottom straight
        if max_count < 5:
            if my_num_no_dup[-1] == 14:
                if my_num_no_dup[0] == 2:
                    if my_num_no_dup[1] == 3:
                        if my_num_no_dup[2] == 4:
                            if my_num_no_dup[3] == 5:
                                max_count = 5
        if max_count >= 5:
            return True
        else:
            return False
    
    # Flush is assumed
    def check_straightflush(self, my_num, my_suit):
        # filter only the numbers with max_suit, then examine straight
        max_suit = mode(my_suit)
        indices = [i for i in range(7) if my_suit[i] == max_suit]
        temp_num = [my_num[indices[i]] for i in range(len(indices))]
        temp_num.sort()
        count = 1
        max_count = 1
        temp = int(temp_num[0])
        for i in range(len(temp_num)-1):
            if temp == int(temp_num[i+1]) - 1:
                count += 1
                temp = int(temp_num[i+1])
                if count >= max_count:
                    max_count = count
            else:
                temp = int(temp_num[i+1])
                count = 1  
        # Check A bottom straight
        if max_count < 5:
            if temp_num[-1] == 14:
                if temp_num[0] == 2:
                    if temp_num[1] == 3:
                        if temp_num[2] == 4:
                            if temp_num[3] == 5:
                                max_count = 5   
        if max_count >= 5:
            return True
        else:
            return False
    # By hierchy, assume no four of a kind, full house
    def check_triple(self, my_num):
        if my_num.count(mode(my_num)) == 3:
            return True
        return False
    
    # By hierchy, assume no triple
    def check_twopair(self, my_num):
        if my_num.count(mode(my_num)) == 2:
            double = mode(my_num)
            temp_num = my_num.copy()
            # delete one number of the first pair to find another pair
            temp_num.remove(double)
            if temp_num.count(mode(temp_num)) == 2:
                return True
        return False
    
    # By hierchy, assume no two pair
    def check_onepair(self, my_num):
        if my_num.count(mode(my_num)) == 2:
            return True
        return False

# Build a class of checking a tie after a showdown
class Check_tie():
    # Input: highest_score(int): combination of possible winners (ex: 9 -> straight flush)
    #        num_winner(int): number of possible winners
    #        hands(list): hands of players, len(hands) = 4 * num_winner
    #        shared_card(list): 5 cards on the board, len(shared_card) = 2*5 
    # Output: the hand of the winners(list)
    def evaluate(self, highest_score, num_winner, hands, shared_card):
        num = hands[::2] + shared_card[::2]
        suit = hands[1::2] + shared_card[1::2]
        if highest_score == 9:
            return self.tie_straightflush(num_winner, num,suit)
        if highest_score == 8:
            return self.tie_fourcard(num,suit)
        if highest_score == 7:
            return self.tie_fullhouse(num_winner, num,suit)
        if highest_score == 6:
            return self.tie_flush(num_winner, num,suit)
        if highest_score == 5:
            return self.tie_straight(num_winner, num,suit)
        if highest_score == 4:
            return self.tie_triple(num_winner, num,suit)
        if highest_score == 3:
            return self.tie_twopair(num_winner, num,suit)
        if highest_score == 2:
            return self.tie_onepair(num_winner, num,suit)
        else:
            return self.tie_high(num_winner, num,suit)
        
    # Input: num_winner(int): number of possible winners
    #        num(list): number of players' hands + number of the board
    #        suit(list): suit of players' hands + suit of the board
    #        ## num and suit are in same order ##
    # Output: the hands of highest scores
    # score: highest num of 5 consecutive numbers of same suit
    def tie_straightflush(self,num_winner, num, suit):
        max_suit = mode(suit)
        scoreboard = []
        result_hands = []
        for i in range(num_winner):
            my_num = [num[i*2], num[i*2 +1]] + num[num_winner*2:]
            my_suit = [suit[i*2], suit[i*2+1]] + suit[num_winner*2:]
            indices = [i for i in range(7) if my_suit[i] == max_suit]
            # sort out the non-max_suit numbers, then examine straight
            temp_num = [my_num[indices[i]] for i in range(len(indices))]
            temp_num.sort()
            count = 1
            max_count = 1
            score = 0
            temp = int(temp_num[0])
            for i in range(len(temp_num)-1):
                if temp == int(temp_num[i+1]) - 1:
                    count += 1
                    temp = int(temp_num[i+1])
                    if count >= max_count:
                        max_count = count
                        if max_count > 4:
                            score = temp_num[i+1]
                else:
                    temp = int(temp_num[i+1])
                    count = 1  
            # Check A bottom straight
            if max_count < 5:
                if temp_num[-1] == 14:
                    if temp_num[0] == 2:
                        if temp_num[1] == 3:
                            if temp_num[2] == 4:
                                if temp_num[3] == 5:
                                    score = temp_num[3]
            scoreboard.append(score)
        indices = [i for i in range(len(scoreboard)) if scoreboard[i] == max(scoreboard)] 
        for i in range(len(indices)):
            result_hands.append(num[indices[i]*2])
            result_hands.append(suit[indices[i]*2])
            result_hands.append(num[indices[i]*2+1])
            result_hands.append(suit[indices[i]*2+1])
        return result_hands

    # Assumes that inputs are already 4 cards
    # There can only be 2 people with four cards
    # Output: the hands of highest scores
    # score: higher fourcard    
    def tie_fourcard(self,num,suit):
        result_hands = []
        # score: higher fourcard
        temp = np.zeros(2)
        for i in range(2):
            my_num = [num[i*2], num[i*2+1], num[-5], num[-4]
                    , num[-3], num[-2], num[-1]] 
            temp[i] = mode(my_num)
        if temp[0] >= temp[1]:
            result_hands.append(num[0])
            result_hands.append(suit[0])
            result_hands.append(num[1])
            result_hands.append(suit[1])
        if temp[1] >= temp[0]:
            result_hands.append(num[2])
            result_hands.append(suit[2])
            result_hands.append(num[3])
            result_hands.append(suit[3])
        return result_hands
    
    # Output: the hands of highest scores
    # score: triple * 15 + double
    def tie_fullhouse(self,num_winner,num,suit):
        result_hands = []
        scoreboard = np.zeros(num_winner)
        for i in range(num_winner):
            score = 0
            my_num = [num[i*2], num[i*2+1], num[-5], num[-4]
                    , num[-3], num[-2], num[-1]] 
            # sort(), in case there are two triples / two two pairs
            my_num.sort(reverse=True)
            triple = mode(my_num)
            score += triple*15
            temp_num = my_num.copy()
            temp_num.remove(triple)
            temp_num.remove(triple)
            doub = mode(temp_num)
            score += doub
            scoreboard[i] = score
        indices = [i for i in range(len(scoreboard)) if scoreboard[i] == max(scoreboard)] 
        for i in range(len(indices)):
            result_hands.append(num[indices[i]*2])
            result_hands.append(suit[indices[i]*2])
            result_hands.append(num[indices[i]*2+1])
            result_hands.append(suit[indices[i]*2+1])
        return result_hands
     
    # Output: the hands of highest scores
    # score: highest num of 5 or longer consecutive numbers
    def tie_straight(self,num_winner, num,suit):
        scoreboard = []
        result_hands = []
        for i in range(num_winner):
            my_num = [num[i*2], num[i*2 +1]] + num[num_winner*2:]
            my_num_no_dup = list(dict.fromkeys(my_num))
            my_num_no_dup.sort()
            count = 1
            max_count = 1
            score = 0
            temp = int(my_num_no_dup[0])
            for i in range(len(my_num_no_dup)-1):
                if temp == int(my_num_no_dup[i+1]) - 1:
                    count += 1
                    temp = int(my_num_no_dup[i+1])
                    if count >= max_count:
                        max_count = count
                        if max_count > 4:
                            score = my_num_no_dup[i+1]
                else:
                    temp = int(my_num_no_dup[i+1])
                    count = 1  
            # Check A bottom straight
            if max_count < 5:
                if my_num_no_dup[-1] == 14:
                    if my_num_no_dup[0] == 2:
                        if my_num_no_dup[1] == 3:
                            if my_num_no_dup[2] == 4:
                                if my_num_no_dup[3] == 5:
                                    score = 5
            scoreboard.append(score)
        indices = [i for i in range(len(scoreboard)) if scoreboard[i] == max(scoreboard)] 
        for i in range(len(indices)):
            result_hands.append(num[indices[i]*2])
            result_hands.append(suit[indices[i]*2])
            result_hands.append(num[indices[i]*2+1])
            result_hands.append(suit[indices[i]*2+1])
        return result_hands     
    
    # Output: the hands of highest scores
    # score: sum of 5 cards of same suit in desc order
    def tie_flush(self,num_winner, num,suit):
        scoreboard = []
        result_hands = []
        for i in range(num_winner):
            my_num = [num[i*2], num[i*2 +1]] + num[num_winner*2:]
            my_suit = [suit[i*2], suit[i*2+1]] + suit[num_winner*2:]
            max_suit = mode(my_suit)
            indices = [i for i in range(7) if my_suit[i] == max_suit]
            temp_num = [my_num[indices[i]] for i in range(len(indices))]
            temp_num.sort(reverse=True)
            score = 0
            score = score + temp_num[0] + temp_num[1] +  temp_num[2]+ temp_num[3]+ temp_num[4]
            scoreboard.append(score)
        indices = [i for i in range(len(scoreboard)) if scoreboard[i] == max(scoreboard)] 
        for i in range(len(indices)):
            result_hands.append(num[indices[i]*2])
            result_hands.append(suit[indices[i]*2])
            result_hands.append(num[indices[i]*2+1])
            result_hands.append(suit[indices[i]*2+1])
        return result_hands  

    # Output: the hands of highest scores
    # score: triple*15^2 + highest num except triple*15 + next highest num
    def tie_triple(self,num_winner, num,suit):
        result_hands = []
        scoreboard = np.zeros(num_winner)
        for i in range(num_winner):
            score = 0
            my_num = [num[i*2], num[i*2+1], num[-5], num[-4]
                    , num[-3], num[-2], num[-1]] 
            triple = mode(my_num)
            score += triple*15**2
            temp_num = my_num.copy()
            temp_num.remove(triple)
            temp_num.remove(triple)
            temp_num.remove(triple)
            temp_num.sort(reverse=True)
            score = score + temp_num[0]*15 + temp_num[1]
            scoreboard[i] = score
        indices = [i for i in range(len(scoreboard)) if scoreboard[i] == max(scoreboard)] 
        for i in range(len(indices)):
            result_hands.append(num[indices[i]*2])
            result_hands.append(suit[indices[i]*2])
            result_hands.append(num[indices[i]*2+1])
            result_hands.append(suit[indices[i]*2+1])
        return result_hands  

    # Output: the hands of highest scores
    # score: higher pair*15^2 + lower pair*15 + highest card except them
    def tie_twopair(self,num_winner, num,suit):
        result_hands = []
        scoreboard = np.zeros(num_winner)
        for i in range(num_winner):
            score = 0
            my_num = [num[i*2], num[i*2+1], num[-5], num[-4]
                    , num[-3], num[-2], num[-1]] 
            my_num.sort(reverse=True)
            double = mode(my_num)
            score += double*15**2
            temp_num = my_num.copy()
            temp_num.remove(double)
            temp_num.remove(double)
            double = mode(temp_num)
            score += double*15
            temp_num.remove(double)
            temp_num.remove(double)
            score += temp_num[0]
            scoreboard[i] = score
        indices = [i for i in range(len(scoreboard)) if scoreboard[i] == max(scoreboard)] 
        for i in range(len(indices)):
            result_hands.append(num[indices[i]*2])
            result_hands.append(suit[indices[i]*2])
            result_hands.append(num[indices[i]*2+1])
            result_hands.append(suit[indices[i]*2+1])
        return result_hands  

    # Output: the hands of highest scores
    # score: pair*15^3 + highest*15^2 + next*15 + next
    def tie_onepair(self,num_winner, num,suit):
        result_hands = []
        scoreboard = np.zeros(num_winner)
        for i in range(num_winner):
            score = 0
            my_num = [num[i*2], num[i*2+1], num[-5], num[-4]
                    , num[-3], num[-2], num[-1]] 
            my_num.sort(reverse=True)
            pair = mode(my_num)
            score += pair*15**3
            temp_num = my_num.copy()
            temp_num.remove(pair)
            temp_num.remove(pair)
            score = score + temp_num[0]*15**2 + temp_num[1]*15 + temp_num[2]
            scoreboard[i] = score
        indices = [i for i in range(len(scoreboard)) if scoreboard[i] == max(scoreboard)] 
        for i in range(len(indices)):
            result_hands.append(num[indices[i]*2])
            result_hands.append(suit[indices[i]*2])
            result_hands.append(num[indices[i]*2+1])
            result_hands.append(suit[indices[i]*2+1])
        return result_hands  

    # Output: the hands of highest scores
    # score: highest*15^4 + next*15^3 + next*15^2 +next*15 + next
    def tie_high(self,num_winner, num,suit):
        result_hands = []
        scoreboard = np.zeros(num_winner)
        for i in range(num_winner):
            score = 0
            my_num = [num[i*2], num[i*2+1], num[-5], num[-4]
                    , num[-3], num[-2], num[-1]] 
            my_num.sort(reverse=True)
            score = score + my_num[0]*15**4 + my_num[1]*15**3 + my_num[2]*15**2 + my_num[3]*15 + my_num[4]
            scoreboard[i] = score
        indices = [i for i in range(len(scoreboard)) if scoreboard[i] == max(scoreboard)] 
        for i in range(len(indices)):
            result_hands.append(num[indices[i]*2])
            result_hands.append(suit[indices[i]*2])
            result_hands.append(num[indices[i]*2+1])
            result_hands.append(suit[indices[i]*2+1])
        return result_hands 
    
# Print out the result in readable format
# Input: highest_score(int):  
#        hands(list): hands of possible winners
#        shared_hands: 5 cards on the board 
# Prints the number of winners, winning combination, and their hands
def result_show(highest_score, hands,shared_hands):
    num_winner = int(len(hands)/4)
    print("There is/are {} winner(s)".format(num_winner))
    hands_num = hands[::2] + shared_hands[::2]
    hands_suit = hands[1::2] + shared_hands[1::2]
    for i, v in enumerate(hands_num):
        if v == 14:  
            hands_num[i] = "A"
        elif v == 13:
            hands_num[i] = "K"
        elif v == 12:
            hands_num[i] = "Q"
        elif v == 11:
            hands_num[i] = "J"
        else:
            hands_num[i] = int(hands_num[i])
    for i, v in enumerate(hands_suit):
        if v == 0:  
            hands_suit[i] = "C"
        elif v == 1:
            hands_suit[i] = "D"
        elif v == 2:
            hands_suit[i] = "H"
        else:
            hands_suit[i] = "S"  
    print("Board: ") 
    print(hands_num[-5], hands_suit[-5]
        ,hands_num[-4], hands_suit[-4]
        ,hands_num[-3], hands_suit[-3]
        ,hands_num[-2], hands_suit[-2]
        ,hands_num[-1], hands_suit[-1]
        ,"\n")
    print("Winning hands: ")
    for i in range(num_winner):
        print(hands_num[i*2], hands_suit[i*2],hands_num[i*2+1]
            ,hands_suit[i*2+1],"\n")
    if highest_score == 9:
        print("Winning combination : Straight Flush")
    elif highest_score == 8:
        print("Winning combination : Four of a kind")
    elif highest_score == 7:
        print("Winning combination : Full house")    
    elif highest_score == 6:
        print("Winning combination : Flush")
    elif highest_score == 5:
        print("Winning combination : Straight")
    elif highest_score == 4:
        print("Winning combination : Triple")
    elif highest_score == 3:
        print("Winning combination : Two Pair")
    elif highest_score == 2:
        print("Winning combination : One Pair")
    else:
        print("Winning combination : High Card")

# Plays a single game
# Input: num_player(int), deck(list)
# From result_show(), Prints the number of winners, winning combination, and their hands
def game(num_player, deck):
    shuffled_card = shuffle(num_player,deck)
    shared_card = shuffled_card[0:10].tolist()
    scoreboard = []
    hands = []
    for i in range(num_player):
        my_card = [shuffled_card[10+i*4],shuffled_card[11+i*4]
                   ,shuffled_card[12+i*4],shuffled_card[13+i*4]]
        hands += my_card
        my_card.extend(shared_card)
        showdown = Check()
        score = showdown.evaluate(my_card)
        scoreboard.append(score)
    highest_score = max(scoreboard)
    num_winner = scoreboard.count(max(scoreboard))
    result_hands = []
    # tie breaker
    if num_winner >= 2:
        print("Tie breaker initiated")
        indices = [i for i in range(len(scoreboard)) if scoreboard[i] == highest_score]
        for i in range(num_winner):
            for j in range(4):
                result_hands.append(hands[indices[i]*4+j])
        tiebreaker = Check_tie()
        result_hands = tiebreaker.evaluate(highest_score, num_winner, result_hands, shared_card)
    else:
        max_index = scoreboard.index(max(scoreboard))
        result_hands = [hands[max_index*4],hands[max_index*4+1]
                 ,hands[max_index*4+2],hands[max_index*4+3]]
    result_show(highest_score, result_hands,shared_card)


# Verify the code by running Monte Carlo simulation and comparing with actual statistics
# n = 1000000
# deck = generate_deck()
# #num_player = num_player_input()
# result = []
# for i in range(n):
#     a = game(1,deck)
#     result.append(max(a))

# result_prob = [result.count(1), ]
# model_prob = [result.count(1)/n,result.count(2)/n,result.count(3)/n,
#                          result.count(4)/n,result.count(5)/n,result.count(6)/n
#                          ,result.count(7)/n,result.count(8)/n,result.count(9)/n]
# actual_possible_prob = [23294460/133784560,58627800/133784560,31433400/133784560
#                         ,6461620/133784560,6180020/133784560,4047644/133784560
#                         ,3473184/133784560,224848/133784560,41584/133784560]
# print(model_prob)
# print(actual_possible_prob)
