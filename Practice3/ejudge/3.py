word_to_digit = {
    'ZER': '0', 'ONE': '1', 'TWO': '2', 'THR': '3', 'FOU': '4',
    'FIV': '5', 'SIX': '6', 'SEV': '7', 'EIG': '8', 'NIN': '9'
}

digit_to_word = {
    '0': 'ZER', '1': 'ONE', '2': 'TWO', '3': 'THR', '4': 'FOU',
    '5': 'FIV', '6': 'SIX', '7': 'SEV', '8': 'EIG', '9': 'NIN'
}


def word_to_num(word):
    num = ''
    i = 0
    while i < len(word):
        three_letters = word[i:i + 3]
        digit = word_to_digit[three_letters]
        num = num + digit
        i = i + 3

    return int(num)


def num_to_word(num):
    num_string = str(num)

    result = ''
    for digit in num_string:
        word = digit_to_word[digit]
        result = result + word

    return result


def calculate(expression):
    for op in ['+', '-', '*']:
        if op in expression:
            parts = expression.split(op)
            left = parts[0]
            right = parts[1]

            left_num = word_to_num(left)
            right_num = word_to_num(right)


            if op == '+':
                result = left_num + right_num
            elif op == '-':
                result = left_num - right_num
            elif op == '*':
                result = left_num * right_num

            return num_to_word(result)


expression = input().strip()
print(calculate(expression))