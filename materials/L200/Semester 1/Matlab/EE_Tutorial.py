# # # # name = input('enter user name: ')
# # # # age = int(input('enter user age: '))
# # # #
# # # # print(f'{name} is {age} years old.')
# # #
# # # while True:
# # #     print('''
# # #     What is the sum of 2 and 3?
# # #     a. 2
# # #     b. 3
# # #     c. 5
# # #     d. 23
# # #     ''')
# # #
# # #     user = input('ans: ')
# # #
# # #     if user == 'a':
# # #         print('incorrect answer!')
# # #     elif user == 'b':
# # #         print('incorrect answer!')
# # #     elif user == 'c':
# # #         print('you are correct!')
# # #         break
# # #     else:
# # #         print('incorrect answer!')
# #
# # def addnumbers(a,b):
# #     # a = int(input('enter a number: '))
# #     # b = int(input('enter another number: '))
# #
# #     result = a + b
# #     print(f'the sum  of {a} and {b} = {result}')
# #
# # addnumbers(1,2)
# #
# #
# #
# #
# #
# #
# #
# from math import pi,sqrt
# import random
# x = random.randint(1,100)
# print(x)
#

#
#
#
#
#
#
#
#
while True:
    import random
    computer = random.choice(['apple','banana','grape','orange','melon'])

    attempts = 5
    for attempt in range(1,attempts + 1):
        print(['apple','banana','grape','orange','melon'])
        user = input('From the above list, guess a fruit: ')

        if user == computer:
            print(f'Congratulations! You guessed the word in {attempt} attempts.')
            break
        else:
            print('you guessed wrong!')

            if attempt == attempts:
                print(f'Game over! The correct word is {computer}')
                print(f"the correct word was {computer}" )

    option = input('Do you want to play again? (yes or no)')
    valid = ['yes','no']
    while option not in valid:
        print('invalid input!')
        option = input('Do you want to play again? (yes or no)')

    if option == 'no':
        print('thank you for playing! Goodbye.')
        break






