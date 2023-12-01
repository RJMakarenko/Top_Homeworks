"""
Вам пришло секретное послание. Оно содержит много странных символов, которые вы не можете
понять.
Но вы знаете, что в этом послании используются только маленькие русские буквы. Используйте
знание языка Python
а так же знание for i, чтобы расшифровать его.
"""

# Секретное послание
secret_letter = [['DFВsjl24sfFFяВАДОd24fssflj234'], ['asdfFп234рFFdо24с$#afdFFтasfо'],
['оafбasdf%^о^FFжа$#af243ю'],['afпFsfайFтFsfо13н'],
['fн13Fа1234де123юsdсsfь'], ['чFFтF#Fsfsdf$$о'],
['и$##sfF'], ['вSFSDам'],['пSFоsfнрSDFаSFвSDF$иFFтsfaсSFя'],
['FFэasdfтDFsfоasdfFт'], ['FяDSFзFFsыSfкFFf']]

# Список с маленькими русскими буквами
small_rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и',
'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

message = ''
for i in range(len(secret_letter)):
    for letter in secret_letter[i][0]:
        message += letter if letter in small_rus else ''
    if i == 3:
        message += '!'
    message += ' '
print(message.capitalize())
print()
input('Для выхода из программы нажмите "Enter"')

# Списочное выражение. Решил потренироваться во вложенных циклах.

# message = [letter for word in secret_letter for letter in word[0] if letter in small_rus]
# print(''.join(message))