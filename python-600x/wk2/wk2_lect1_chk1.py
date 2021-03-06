# number guessing game

low = 0
high = 100
guess = (low + high) / 2
guess_msg = "Enter 'h' for too high, 'l' for too low, 'c' for correct: "
error_msg = "Please respond with only 'h', 'l' or 'c' \nTry again"
resp = ""
proper_resps = ['h', 'l', 'c']

print 'Please think of a number between 0 and 100!'
while resp != 'c':
    print
    print 'Is your secret number ' + str(guess) + "?"
    print

    resp = raw_input(guess_msg)
    print
    while resp not in proper_resps:
        print
        print error_msg
        print
        resp = raw_input(guess_msg)

    if resp == 'h':
        high = guess
        guess = (low + high) / 2
    elif resp == 'l':
        low = guess
        guess = (low + high) / 2

print 'Your secret number is ' + str(guess)
