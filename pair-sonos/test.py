class A:
    def __init__(self, i = 2, j = 3):
        self.i = i
        self.j = j
    def __str__(self):
        return"A"
    def __eq__(self, other):
        return self.i * self.j == other.i * other.j

def main():
    x = A(1, 2)
    y = A(2, 1)
    print(x == y)
	
main()