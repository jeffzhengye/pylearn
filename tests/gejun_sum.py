__author__ = 'jeffye'


def sum_consecutives(s):
    i = 1
    li = []
    if i < len(s):
        n = 1
    while s[i] != s[i + 1] and s[i] != s[i - 1]:
        sum = s[i]
        i = i + 1
        return sum

    while s[i] == s[i + 1]:
        n = n + 1
        sum = s[i] * n
        i = i + 1
        return sum
    li.append(sum)

    return li


def sum_consecutives_corrected(s):
    start = 0
    li = []

    n = 1
    while start < len(s):
        if start == len(s) - 1:  # last element
            li.append(s[start])
            break
        elif s[start] == s[start + n]:  # equal, just record the length
            n += 1
        else:  # first not equal, sum all previous equal elements and append to li
            li.append(sum(s[start: start + n]))
            start += n
            n = 1

    return li


if __name__ == '__main__':
    test_li = [-5, -5, 7, 7, 12, 0]  # should return [-10,14,12,0]
    print(sum_consecutives_corrected(test_li))

