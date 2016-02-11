#ifndef _BINARY_ARRAY_H_
#define _BINARY_ARRAY_H_

// The struct type that is used
typedef struct binary_array binary;

/* ------- INFO -------

How to include in a project:
1. Save both 'binary_array.c' and 'binary_array.h' in the same directory as 
    your C file that calls it

2. Add an include in your code for this header file: (#include "binary_array.h")

3. Use the functions defined in the header file in your code.

4. At compile time, compile the 'binary_array.c' file into an object file first:
    (gcc -std=c99 -c binary_array.c -o binary_array.o)

5. Then, compile your file that includes the 'binary_array.h' header with the 
    object file generated:
    (gcc exampleFile.c binary_array.o -o exampleFile)

6. Your file 'exampleFile' will now run using the functions defined in this
    header file.


The binary datatype:
The binary value is stored as bits in an unsigned char array, where each  
unsigned char has a size of 8 bits.

The stored binary has a layout the opposite way a regular char array is stored.
The high-order bit is the farthest left value, and the low end bit is the
rightmost value.

Binary char array:
  high order bit (index n (where n = length) )
 /
 100000000010
             \
              low order bit (index 0)


Regular char array:
  low order bit (index 0)
 /
 100000000010
             \
              high order bit (index n (where n = length) )


index:  7 6 5 4 3 2 1 0     15  13  11  9 8     etc...
                      |       14  12  10  |
                      |       |   |   |   |
        ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓     ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        1 0 0 1 0 1 1 1     0 0 0 0 0 1 1 0     0 1 0 0 0 0 0 0
        - - - - - - - -     - - - - - - - -     - - - - - - - -
        unsigned char[0]    unsigned char[1]    unsigned char[2]

This only matters when using 'set_bit()' or 'get_bit()', where the index
specified follows these rules here. All of the other functions abstract 
away this design structure.

*/


// Functions provided:

// Initializer functions:
// Initializes a binary array of zeros with a length of 'length' (eg. a length 
//      of 15 creates a 15-element array of zeros).
binary *initialize_binary(int length);               
// Initializes a binary array with the same value as the string passed in.
binary *string_to_binary(const char *inputString);


// Information and maintenance functions:
// Returns the binary array value as a pointer to a char array. This array needs
//      to be freed once it is no longer being used to prevent memory leaks (see 
//      documentation in binary_array.c).
char *binary_to_string(binary const *input);
// Returns the length of the binary array (a 15-element array has a size of 15).
int get_length(binary const *input);
// Copies the binary 'input' into the binary 'copy'.
void copy_binary(binary *copy, binary const *input);
// Frees the memeory used by a binary. Needs to be called once the binary value is 
// no longer needed.
void free_binary(binary *input);


// Bit-by-bit operations
// get the bit in the binary 'input' at the 'index' (returns an integer 1 or 0)
int get_bit(binary const *input, int index);
// set the bit in the binary 'input' at the 'index' to a binary value (entered as an 
// integer 1 or 0)
void set_bit(binary *input, int index, int bit);


// Bitwise operations
// All of these functions need any three binary values to be passed in. The 'result'
// binary will be modified to store the result. None of the operands or the result need 
// to be the same size.

// Note: It is possible to perform an operation between two binary values
// and store the result in one of the binary valus passed in: eg.
// AND_binary(operand_A, operand_A, operand_B);
// or even perform an operation on the same binary value and store the result in itself:
// XOR_binary(operand_A, operand_A, operand_A);   // this will zero out operand_A
void AND_binary(binary *result, binary const *operand_A, binary const *operand_B);
void OR_binary(binary *result, binary const *operand_A, binary const *operand_B);
void XOR_binary(binary *result, binary const *operand_A, binary const *operand_B);

// These two operations shift the binary value 'input' by 'shiftAmount' bits, 
// and store the result as 
void shift_left(binary *result, binary const *input, int shiftAmount);
void shift_right(binary *result, binary const *input, int shiftAmount);

// Inverts all of the bits in a binary 'input' and stores the result in 'result'
void complement_binary(binary *result, binary const *input);


// Internal functions
void resize_binary(binary *input, int length);



// Notes:
// maybe add a set_byte for faster looping instead of bit-wise operations
// add a compare binaries that uses XOR to check if they are identical
// reverse binary
// bool shiftInPlace? for complement and shifts?

#endif
