import numpy as np
import math


def euclid(a, n):
    m = n
    q = np.zeros(15, dtype=int)
    i = 0
    while n % a:
        q[i] = -(n / a)
        i += 1
        n, a = a, n % a
    q[i] = -(n / a)
    a_1 = np.zeros(15, dtype=int)
    a_1[1] = 1
    a_1[2] = q[0]
    for j in range(2, i+1):
        j += 1
        a_1[j] = q[j - 2] * a_1[j - 1] + a_1[j - 2]
    return a_1[i+1] % m


def solver(a, b, m):
    a = a % m
    d = math.gcd(a, m)
    if b % m:
        ans = np.zeros(d, dtype=int)
        a1, b1, m1 = int(a / d), int(b / d), int(m / d)
        inv_a = euclid(a1, m1)
        x0 = (b1 * inv_a) % m1
        for k in range(d):
            ans[k] = x0 + k * m1
        return ans
    else:
        print("There is no answer.")
        return 0


alphabet = np.array(['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                     'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я'])
file = open("text.txt", "r", encoding='utf-8')
text = file.read()
print(len(text))
text = text[1:]
print(len(text))
temporary = np.zeros(len(text), dtype=int)
print(text)
for i in range(0, len(alphabet)):  # iterating per alphabet
    for j in range(0, len(text)):  # iteration through the whole text
        if text[j] == alphabet[i]:  # checking for matching
            temporary[j] = i  # saving letter code
tempbigrams = np.zeros(int(len(text) / 2), dtype=int)
rarity2 = np.zeros(len(alphabet) ** 2, dtype=int)  # creating array of rarity for begram
most_common_bigrams = np.array([545, 417, 572, 414, 168], dtype=int)
for i in range(0, len(tempbigrams)):
    tempbigrams[i] = temporary[2 * i] * len(alphabet) + temporary[2 * i + 1]
    rarity2[tempbigrams[i]] += 1
most_common_bigram1 = np.argmax(rarity2)
tempr = np.array(rarity2, dtype=int)
tempr[most_common_bigram1] = 0
most_common_bigram2 = np.argmax(tempr)
print(most_common_bigram1, most_common_bigram2, rarity2[most_common_bigram1], rarity2[most_common_bigram2])
A = solver(most_common_bigrams[0] - most_common_bigrams[1], most_common_bigram1 - most_common_bigram2, len(alphabet) **
           2)
print(rarity2)
print(temporary[:100])
print(tempbigrams[:50])
print(A)
# print(solver(545 - 417, 411, 961))
# print(euclid(128, 961))
