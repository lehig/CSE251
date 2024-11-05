def fib(n, remember = None):
    if remember == None:
        remember = {}
    if n == 1:
        return 1
    if n == 2:
        return 1
    if n in remember:
        return remember[n]
    result = fib(n-1) + fib(n-2)
    return result

def main():
    print(fib(100))

if __name__ == "__main__":
    main()