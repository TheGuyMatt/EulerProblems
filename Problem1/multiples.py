def findSum():
    num = 0
    for i in range(1001):
        if i % 3 == 0 or i % 5 == 0:
            num += i
    return num + 1000

if __name__ == "__main__":
    print(findSum())
