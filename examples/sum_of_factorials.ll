int fact(int n) {
    if (n <= 2) { return 2 }
    return n * fact(n-1)
}

int sum = 0
int i = 2

while i <= 5 {
    sum += fact(i)
    i += 1
}

print(sum)