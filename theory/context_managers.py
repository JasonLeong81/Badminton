import decorators as d
import random
import time

while True:
    # answer = input('You :')
    print('Lovely Bot: '+random.choice(d.response))
    time.sleep(1)
    print('Angry Bot: ' + random.choice(d.response1))
    time.sleep(1)
