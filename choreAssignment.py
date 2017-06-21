#! /usr/bin/env python3
# choreAssignment.py - Randomly assigns chores to people and emails them about it

import sys
import os, smtplib, random

people = sys.argv[1:]
chores = ['dishes', 'laundry', 'vacuum', 'cook']
assigned = {}

acc = input('Your email login ID:')
psw = input('Your email password:')

if os.path.exists('lastChores.txt') == True:
    lastChores = open('lastChores.txt')
    lastContent = lastChores.readlines()
    lastAssigned = {}
    for line in lastContent:
        w = line.split()
        lastAssigned[w[0]] = w[1]
    for i in range(len(people)):
        while lastAssigned[people[i]] == assigned.get(people[i], lastAssigned[people[i]]):
            randomChore = random.choice(chores)
            assigned[people[i]] = randomChore
            if i == len(people):
                duplicateDict = dict(assigned)
                j = 0
                while assigned[people[len(people)]] == lastAssigned[people[len(people)]] and assigned[people[j]] == lastAssigned[people[j]]:
                    assigned = dict(duplicateDict)
                    x = assigned[people[len(people)]]
                    y = assigned[people[j]]
                    assigned[people[len(people)]] = y
                    assigned[people[j]] = x
                    j += 1
        
        chores.remove(randomChore)
    lastChores = open('lastChores.txt', 'w')
    for k in assigned.keys():
        lastChores.write(k + ' ' + assigned[k] + '\n')
    
else:
    lastChores = open('lastChores.txt', 'w')
    rpeople = people[:]
    for iperson in people:
        # Picks a random chore and then removes it from the list
        randomChore = random.choice(chores)
        chores.remove(randomChore)
        assigned[person] = randomChore
        rpeople.remove(person)
        if chores == []:
            print('Finished assigning chores. People without a chore: ' + ', '.join(rpeople))
            break
    for k in assigned.keys():
        lastChores.write(k + ' ' + assigned[k] + '\n')
    
lastChores.close()

# Log into email account.
smtpObj = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
smtpObj.ehlo()
smtpObj.login(acc, psw)

# Emails the assigned chore to each person.
for email, chore in assigned.items():
    body = 'Subject: Your assigned chore this time.\nYou have been assigned %s to do. So please make sure you get it done. Thank you!' % chore
    print('Sending email to %s...' % email)
    sendmailStatus = smtpObj.sendmail(acc, email, body)

    if sendmailStatus != {}:
        print('There was a problem sending email to %s: %s' % (email, sendmailStatus))
smtpObj.quit()
print(assigned)
