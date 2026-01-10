/*
** source.c - Level3 Binary Replication
** 
** This program replicates the behavior of the level3 binary.
** It validates input against specific criteria and compares
** the constructed string with a target string "********".
**
** Compile: gcc -o source source.c
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TARGET_STRING "********"
#define BUFFER_SIZE 9
#define INPUT_SIZE 64

void print_nope_and_exit(void) {
    puts("Nope.");
    exit(1);
}

void print_success(void) {
    puts("Good job.");
}

int main(void) {
    char input[INPUT_SIZE];
    char buffer[BUFFER_SIZE];
    int result;
    
    // Print prompt
    printf("Please enter key: ");
    fflush(stdout);
    
    // Read input using scanf
    result = scanf("%63s", input);
    
    // Check if scanf successfully read exactly 1 item
    if (result != 1) {
        print_nope_and_exit();
    }
    
    // Validation Point 1: Check if second character is '2' (0x32)
    if (input[1] != '2') {
        print_nope_and_exit();
    }
    
    // Validation Point 2: Check if first character is '4' (0x34)
    if (input[0] != '4') {
        print_nope_and_exit();
    }
    
    // Flush stdout
    fflush(stdout);
    
    // Initialize buffer with null bytes
    memset(buffer, 0, BUFFER_SIZE);
    
    // Set first character to '*' (0x2a = 42)
    buffer[0] = '*';
    
    // Process input in 3-character groups starting from position 2
    int counter = 2;        // Start at position 2 (skip "42" prefix)
    int offset = 1;         // Buffer position (starts at 1, not 0)
    
    while (offset <= 7 && counter < strlen(input)) {
        // Check if we have at least 3 characters left
        if (strlen(input) < counter + 3) {
            break;
        }
        
        // Extract 3 characters and convert to integer using atoi
        char temp[4];
        temp[0] = input[counter];
        temp[1] = input[counter + 1];
        temp[2] = input[counter + 2];
        temp[3] = '\0';
        
        // Convert to integer
        int ascii_value = atoi(temp);
        
        // Validation Point 3: Check if value equals 42 (0x2a = '*')
        if (ascii_value != 42) {
            print_nope_and_exit();
        }
        
        // Store the character in buffer
        buffer[offset] = (char)ascii_value;
        
        // Move to next group
        counter += 3;
        offset++;
    }
    
    // Null-terminate the buffer at the correct position
    buffer[offset] = '\0';
    
    // Compare constructed buffer with target string
    if (strcmp(buffer, TARGET_STRING) == 0) {
        print_success();
    } else {
        puts("Nope.");
    }
    
    return 0;
}
