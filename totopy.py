import random
import os
prizePool = 1000000

def checkReward(winningNums, guess):
    hits = 0
    extraHit = 0

    for num in guess:
        if (num in winningNums[:6]):
            hits += 1
        if (num == winningNums[-1]):
            extraHit = 1

    if (hits == 6):
        # print('jackpot')
        return prizePool*0.38

    elif (hits == 5 and extraHit):
        # print('group 2')
        return prizePool*0.08*0.33 # Multiplied by expected share rate

    elif (hits == 5):
        # print('group 3')
        return prizePool*0.055*0.007 # Multiplied by expected share rate

    elif (hits == 4 and extraHit):
        # print('group 4')
        return prizePool*0.03*0.003 # Multiplied by expected share rate

    elif (hits == 4):
        # print('group 5')
        return 50

    elif (hits == 3 and extraHit):
        # print('group 6')
        return 25

    elif (hits == 3):
        # print('group 7')
        return 10

    else:
        return 0

def binomial(n, k):
    if 0 <= k <= n:
        a= 1
        b=1
        for t in range(1, min(k, n - k) + 1):
            a *= n
            b *= t
            n -= 1
        return a // b
    else:
        return 0

def randomTotoNum():
    return random.randrange(1,49,1)

def quickPick(number):
    pick = []
    while (len(pick) < number):
        num = randomTotoNum()
        if (num not in pick): pick.append(num)
    pick.sort();
    print(f'Drawing with {pick}')
    return pick

def produceDraw():
    winningNumbers = []
    draw = []
    while (len(draw) < 6):
        num = randomTotoNum()
        if (num not in draw): draw.append(num)
    draw.sort();
    extraNum = randomTotoNum()
    while (extraNum in draw): extraNum = randomTotoNum()
    draw.append(extraNum)

    return draw;

#############################################################################

input1 = input('Input guess (Leave blank for quick pick): ')
if (input1 == ''):
    number = int(input('Quick pick? How many numbers (6-12): '))
    inputGuess = quickPick(number)
else:
    inputGuess = [int(x) for x in input.split(',')]
# Assumption: draw jackpot is 1 million
noJackpot = True
count = 0
cost = 0
earned = 0
system = 1

if (len(set(inputGuess)) < 6): raise ValueError('Not valid input')
for num in inputGuess:
    if (num < 1 or num > 49): raise ValueError('Not valid input')

if (len(inputGuess) > 6): system = binomial(len(inputGuess),6)

while (noJackpot):
    x = produceDraw()
    hits = 0
    reward = checkReward(x, inputGuess)
    cost += system
    earned += reward
    count += 1
    if (reward == prizePool): noJackpot = False
    if (count % 100000 == 0):
        print(f'Draw number: {count:,} -- Loss: -${cost:,} and reward: ${earned:,}')


print(f'Draw number: {count:,} -- Loss: -${cost:,} and reward: ${earned:,}')
print(f'---- POT -----')
print(f'Your guess was: {inputGuess}')
print(f'Net: ${earned - cost:,}')
