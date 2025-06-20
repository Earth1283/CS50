vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]

def main():
    word = str(input("Input: ").strip())
    shorten(word)

def shorten(word):
    memory = str(word)
    for char in word:
        if char not in vowels:
            word = "".join(char)

if __name__ == "__main__":
    main()
