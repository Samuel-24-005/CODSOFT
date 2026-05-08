import random
import string

def generate_password(length, use_digits, use_symbols):
    characters = string.ascii_letters

    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("=== Password Generator ===")
    while True:
        try:
            length = int(input("Enter desired password length (8-128): "))
            if 8 <= length <= 128:
                break
            else:
                print("Please enter a number between 8 and 128.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    use_digits = input("Include numbers? (y/n): ").lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").lower() == 'y'

    password = generate_password(length, use_digits, use_symbols)

    print(f"\nGenerated Password: {password}")

if __name__ == "__main__":
    main()