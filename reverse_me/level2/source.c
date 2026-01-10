#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void no() {
    printf("Nope.\n");
    exit(1);
}

void ok() {
    printf("Good job.\n");
}

int main() {
    char input[36];  // Buffer for scanf input
    char buffer[10]; // Buffer to construct the result string
    int ret;
    int index = 2;   // Start from position 2 in input (after "00")
    int buf_pos = 1; // Start from position 1 in buffer (buffer[0] is pre-set to 'd')

    printf("Please enter key: ");
    ret = scanf("%23s", input);

    // Check scanf returned 1
    if (ret != 1) {
        no();
    }

    // Check first two characters are '0' (ASCII 0x30)
    if (input[1] != '0') {  // Note: input[1] is checked before input[0] in assembly
        no();
    }
    if (input[0] != '0') {
        no();
    }

    // Flush stdout
    fflush(stdout);

    // Initialize buffer with 'd' at position 0 and zeros for the rest
    memset(buffer, 0, 9);
    buffer[0] = 'd';  // 0x64 = 100 = 'd'
    
    // Loop: extract groups of 3 digits from input and convert to characters
    while (strlen(buffer) < 8 && index < strlen(input)) {
        char temp[4];  // Temporary buffer for 3 digits
        temp[0] = input[index];
        temp[1] = input[index + 1];
        temp[2] = input[index + 2];
        temp[3] = '\0';
        
        // Convert 3-digit ASCII number to integer, then to character
        buffer[buf_pos] = (char)atoi(temp);
        
        index += 3;
        buf_pos++;
    }

    // Null-terminate the buffer
    buffer[buf_pos] = '\0';

    // Compare with target string "delabere"
    if (strcmp(buffer, "delabere") == 0) {
        ok();
    } else {
        no();
    }

    return 0;
}
