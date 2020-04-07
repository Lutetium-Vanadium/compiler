int fact(int n) {
    if (n <= 2) { return 2 }
    return n * fact(n-1)
}

int sum = 0
int i = 2

print("importing add")
import "./add"

while i <= 5 {
    sum += fact(i)
    i += 1
}

print(`Sum of first 5 factorials {sum}`)