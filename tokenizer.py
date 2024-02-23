class Tokenizer:
    RESERVED_WORDS = {
        'program': 1, 'begin': 2, 'end': 3, 'int': 4, 'if': 5, 'then': 6, 'else': 7,
        'while': 8, 'loop': 9, 'read': 10, 'write': 11
    }
    SPECIAL_SYMBOLS = {
        ';': 12, ',': 13, '=': 14, '!': 15, '[': 16, ']': 17, '&&': 18, '||': 19,
        '(': 20, ')': 21, '+': 22, '-': 23, '*': 24, '!=': 25, '==': 26, '<': 27,
        '>': 28, '<=': 29, '>=': 30
    }
    EOF = 33
    ERROR = 34

    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.tokens = []
        self.current_index = 0
        self.tokenize_line()

    def tokenize_line(self):
        for line in self.file:  # Iterate over each line in the file
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            token = ""
            i = 0  # Index to keep track of current character position
            while i < len(line):
                char = line[i]
                if char.isspace():  # End of current token
                    self.add_token(token)
                    token = ""
                elif char in self.SPECIAL_SYMBOLS:  # Check for multi-char symbols
                    self.add_token(token)  # Add the token before the symbol
                    token = ""
                    # Check if the next character is part of a two-character symbol
                    if i + 1 < len(line) and line[i+1] in self.SPECIAL_SYMBOLS:
                        two_char_symbol = char + line[i+1]
                        if two_char_symbol in self.SPECIAL_SYMBOLS:
                            self.add_token(two_char_symbol)  # Add the two-character symbol
                            i += 1  # Skip the next character as it's part of the symbol
                        else:
                            self.add_token(char)  # Add the single-character symbol
                    else:
                        self.add_token(char)  # Add the single-character symbol
                else:
                    token += char  # Continue building the current token
                i += 1
            self.add_token(token)  # Add the last token in the line

        # End of file
        self.tokens.append((Tokenizer.EOF, 'EOF'))
    
    def add_token(self, token):
        if not token:  # Ignore empty tokens
            return
        if token in self.RESERVED_WORDS:
            self.tokens.append((self.RESERVED_WORDS[token], token))
        elif token in self.SPECIAL_SYMBOLS:
            self.tokens.append((self.SPECIAL_SYMBOLS[token], token))
        elif token.isdigit():
            self.tokens.append((31, token))  # Assuming 31 is the token type for integers
        elif self.is_identifier(token):
            self.tokens.append((32, token))  # Assuming 32 is the token type for identifiers
        else:
            self.tokens.append((Tokenizer.ERROR, token))

    def is_identifier(self, token):
        return token[0].isupper() and all(c.isupper() or c.isdigit() for c in token[1:])
            
    def get_token(self):
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index][0]  # Return the token type
        return Tokenizer.EOF  # Default to EOF if out of bounds

    def skip_token(self):
        if self.get_token() not in (Tokenizer.EOF, Tokenizer.ERROR):
            self.current_index += 1
            if self.current_index >= len(self.tokens):  # If at end, tokenize next line
                self.tokenize_line()
                
    def int_val(self):
        if self.get_token() == 31:  # Assuming 31 is the token type for integers
            return int(self.tokens[self.current_index][1])
        raise Exception("Current token is not an integer.")

    def id_name(self):
        if self.get_token() == 32:  # Assuming 32 is the token type for identifiers
            return self.tokens[self.current_index][1]
        raise Exception("Current token is not an identifier.")
    
    
def main(input_file):
    tokenizer = Tokenizer(input_file)
    while True:
        token_type = tokenizer.get_token()
        if token_type == Tokenizer.EOF:
            print(f"Token: {token_type}. End of file reached.")
            break
        elif token_type == Tokenizer.ERROR:
            print(f"Token: {token_type}. Error token encountered.")
            break
        else:
            print(f"Token: {token_type}")
        tokenizer.skip_token()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python tokenizer.py <input_file>")
    else:
        main(sys.argv[1])

