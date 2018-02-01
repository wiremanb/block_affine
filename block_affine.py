import string

class block_affine:
    MUL = 0;
    OFFSET = 0;
    inputFile = "";
    saveFile = "";
    alphabetType = "";
    inText = "";
    
    def __init__(self, inputFile, saveFile, alphabetType, multiplier, offset):
        self.MUL = int(multiplier);
        self.inputFile = inputFile;
        self.saveFile = saveFile;
        self.alphabetType = alphabetType;
        self.OFFSET = int(offset);

        # Check to see if values are co-prime
        if self.rp(self.MUL, self.OFFSET) != 1:
            print("[BLOCK-AFFINE] -> Multiplier and offset are not co-prime... retry with co-prime values");
            exit(0);

        # open input file
        try:
            self.inputFile = open(inputFile, 'r');
            self.inText = self.inputFile.read();
        except:
            print("[BLOCK-AFFINE] -> Error.. trying to open file: {0}".format(inputFile));
        
        # open save file
        try:
            self.saveFile = open(saveFile, 'w');
        except:
            print("[BLOCK-AFFINE] -> Error.. trying to open file: {0}".format(saveFile));

        print("\n************** OUTPUT *****************")
        print("[BLOCK-AFFINE] -> Alphabet Type: {0}".format(self.alphabetType));
        print("[BLOCK-AFFINE] -> Saving output to: {0}".format(saveFile));

    # greatest common divisor
    def gcd(self, x,y):
        while y is not 0:
            x, y = y, x % y;
        return x;
    
    # check for co-prime
    def rp(self, x, y):
        return self.gcd(x,y);

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    # check for modular inverse
    def modinv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            print("[BLOCK-AFFINE] -> Modular inverse doesn't exist...");
            exit(0);
        else:
            return x % m

    def encrypt(self):
        ALPHABET = [];
        MOD = 0;
        INPUT = [];
        INPUT = list(self.inText);
        OUTPUT = "";

        # Remove spaces
        for i in range(0, len(INPUT)):
            if INPUT[i] == " ":
                INPUT.remove(i);
        
        # pad input if odd number of values
        if len(INPUT) % 2 != 0:
            print("[BLOCK-AFFINE] -> Length of the input string is odd.. padding input");
            INPUT.append('A');

        print("[BLOCK-AFFINE] -> Input text list: {0}".format(INPUT));
        if(self.alphabetType.lower() == "s"):
            ALPHABET = list(string.ascii_uppercase);
            MOD = len(ALPHABET);
            print("[BLOCK-AFFINE] -> Aphabet S: {0}".format(ALPHABET));
            print("[BLOCK-AFFINE] -> Using MOD: {0}".format(MOD));
            blockSize = -1;
            # perform block affine cipher
            for i in range(0, len(INPUT)):
                if INPUT[i] in ALPHABET:
                    tmp = (((self.MUL * ALPHABET.index(INPUT[i])) + self.OFFSET) % MOD);
                    OUTPUT += str(tmp).zfill(2);
                if blockSize % 2 == 0:
                    OUTPUT += " ";
                blockSize += 1;
            self.saveFile.write(OUTPUT);
            return OUTPUT;

        elif(self.alphabetType.lower() == "l"):
            ALPHABET = list(string.ascii_uppercase+string.ascii_lowercase);
            MOD = len(ALPHABET);
            print("[BLOCK-AFFINE] -> Aphabet L: {0}".format(ALPHABET));
            print("[BLOCK-AFFINE] -> Using MOD: {0}".format(MOD));
            blockSize = -1;
            # perform block affine cipher
            for i in range(0, len(INPUT)):
                if INPUT[i] in ALPHABET:
                    tmp = (((self.MUL * ALPHABET.index(INPUT[i])) + self.OFFSET) % MOD);
                    OUTPUT += str(tmp).zfill(2);
                if blockSize % 2 == 0:
                    OUTPUT += " ";
                blockSize += 1;
            self.saveFile.write(OUTPUT);
            return OUTPUT;
        else:
            print("[BLOCK-AFFINE] -> Error.. expected alphabet type of S or L!");

    def decrypt(self):
        ALPHABET = [];
        MOD = 0;
        INPUT = [];
        INPUT = list(self.inText);
        NEW_INPUT = [];
        OUTPUT = "";

        # Remove spaces .. note: had to do this differently than encrypt..
        for i in range(0, len(INPUT)):
            try:
                INPUT.remove(" ");
            except:
                continue;

        blockSize = -1;
        # Find values from list
        for i in range(0, len(INPUT)):
            if blockSize % 2 == 0:
                NEW_INPUT.append(int(INPUT[i-1] + INPUT[i]));
            blockSize = blockSize + 1;

        print("[BLOCK-AFFINE] -> Input text list: {0}".format(NEW_INPUT));
        if(self.alphabetType.lower() == "s"):
            ALPHABET = list(string.ascii_uppercase);
        elif(self.alphabetType.lower() == "l"):
            ALPHABET = list(string.ascii_uppercase+string.ascii_lowercase);
        else:
            print("[BLOCK-AFFINE] -> Error.. expected alphabet type of S or L!");
            exit(0);
        MOD = len(ALPHABET);
        print("[BLOCK-AFFINE] -> Using MOD: {0}".format(MOD));
        blockSize = -1;
        # Decrypt block affine
        for i in range(0, len(NEW_INPUT)):
            tmp = ((self.modinv(self.MUL, MOD) * (NEW_INPUT[i] - self.OFFSET)) % MOD);
            OUTPUT += ALPHABET[tmp];
        self.saveFile.write(OUTPUT);
        self.saveFile.close();
        return OUTPUT;

def main():
    userInput = raw_input("[BLOCK-AFFINE] -> Encrypt or Decrypt (E or D)? ");
    if userInput.lower() == "e":
        print("[BLOCK-AFFINE] -> You are encrypting text...");
        # pt = raw_input("[BLOCK-AFFINE] -> Enter input text file name (ex: vigenerecipheroutput.txt): ");
        pt = "vigenerecipheroutput.txt";
        # sf = raw_input("[BLOCK-AFFINE] -> Where do you want to save your encrypted text (ex: blockaffinecipheroutput.txt)? ");
        sf = "blockaffinecipheroutput.txt";
        m = raw_input("[BLOCK-AFFINE] -> Enter multiplier: ");
        o = raw_input("[BLOCK-AFFINE] -> Enter offset: ");
        at = raw_input("[BLOCK-AFFINE] -> Enter alphabet type (S or L): ");
        ba = block_affine(pt,sf,at,m,o);
        print(ba.encrypt());
    else:
        print("[BLOCK-AFFINE] -> You are decrypting text...");
        # et = raw_input("[BLOCK-AFFINE] -> Enter encrypted text file name (ex: blockaffinecipheroutput.txt): ");
        et = "blockaffinecipheroutput.txt";
        # sf = raw_input("[BLOCK-AFFINE] -> Where do you want to save your encrypted text (ex: blockaffinecipherplaintextoutput.txt)? ");
        sf = "blockaffinecipherplaintextoutput.txt";
        m = raw_input("[BLOCK-AFFINE] -> Enter multiplier: ");
        o = raw_input("[BLOCK-AFFINE] -> Enter offset: ");
        at = raw_input("[BLOCK-AFFINE] -> Enter alphabet type (S or L): ");
        ba = block_affine(et,sf,at,m,o);
        print(ba.decrypt());

if __name__ == "__main__":
    main();