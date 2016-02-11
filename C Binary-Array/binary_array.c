#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "binary_array.h"

#define BITS_IN_BYTE 8


// The binary structure that stores the binary value
struct binary_array {
    int length;                      // the length (in bits) of the binary value
    unsigned char *binaryCharArray;  // a pointer to the binary char array
} typedef binary;  // Typedef the binary struct as a type called 'Binary'


// A function that exits the program with an exit status of 1 and
// prints an error message to standard out. The message is passed 
// in as a parameter.
static void ThrowException(char const *errorMessage) {
    printf("Exception Thrown: \n");
    printf("          %s\n", errorMessage);
    exit(1);
}



/**
 *  Initialises a binary array and sets all of the elements to zero.
 *  The length of the array is specified as an integer greater than 
 *  or equal to zero (a length of 22 means a 22-binary-value array is created)
 *
 *  If zero is specified, a null binary array is set to NULL and the length is
 *  set to zero.
 *
 *  Examples:
 *  binary *bin_array_A = initialize_binary(0);
 *  binary *bin_array_B = initialize_binary(310);
 *
 *  @param length  the length of the binary array
 *  @return  a zeroed-out binary value of the length specified
 */
binary* initialize_binary(int length) {
    // The length can't be less than one
    if (length < 0) {
        ThrowException("initialize_binary: The length specified is invalid (cannot be less than 0)");
    }

    // allocate a struct and a new NULL unsigned char pointer
    binary *newBinaryStruct = (binary *)calloc(1, sizeof(binary)); 
    unsigned char *newBinaryCharArray = NULL;

    // If the length specified is 0, return the NULL binaryCharArray pointer
    if (length == 0) {
        newBinaryStruct->length = 0;
        newBinaryStruct->binaryCharArray = newBinaryCharArray;
        return newBinaryStruct;

    } else {
        // length / BITS_IN_BYTE                      the max number of bytes that evenly fit
        // (((length % BITS_IN_BYTE ) > 0) ? 1 : 0)   whether or not another byte should be added
        int byteLength = length / BITS_IN_BYTE  +  (((length % BITS_IN_BYTE ) > 0) ? 1 : 0);

        // Allocate a new char array for the binary value and set the struct's fields
        newBinaryCharArray = (unsigned char *)calloc(byteLength, sizeof(unsigned char));
        newBinaryStruct->binaryCharArray = newBinaryCharArray;
        

        // Zero out all of the bytes
        int allBits = byteLength * BITS_IN_BYTE;

        // Temporarily set the max length so all of the bytes can be zeroed
        newBinaryStruct->length = allBits;

        for (int index = 0; index < allBits; index++) {
            set_bit(newBinaryStruct, index, 0);
        }

        // Reset the length to the actual specified length of bits
        newBinaryStruct->length = length; 

        return newBinaryStruct;
    }
}




/**
 *  Initializes a binary array from an input string. The string
 *  must consist of only 0s and 1s.
 *
 *  @param inputString  the input string of a binary array
 *                        (eg. "0100110101100101")
 *  @return  a binary value from the representation of the input string
 */
binary *string_to_binary(const char *inputString) {

    int length = (int) strlen(inputString);
    binary *newBinaryStruct = initialize_binary(length);
    length--; // set size to the computer value for the next operations

    for (int index = length; index >= 0; index--) {
        int nextBinVal = inputString[index] - '0';   // get the integer value from the char

        if ( nextBinVal != 1  &&  nextBinVal != 0 ) {
            ThrowException("string_to_binary: Invalid bit entered (not a 0 or 1)");
        }

        set_bit(newBinaryStruct, (length - index), nextBinVal);
    }

    return newBinaryStruct;
}



/**
 *  Returns a char pointer to a null-terminated string that represents the 
 *  value in the binary array. 
 *
 *  Note: the char pointer must be freed after use
 *  Example:
 *
 *  //...
 *  char *stringResult = binary_to_string(input);
 *  printf("Binary string: %s\n", stringResult);
 *  free(stringResult);
 *  //...
 *
 *  @param input  the binary value
 *  @return  a char pointer to the calloc'ed string
 */
char *binary_to_string(binary const *input) {
    int length = input->length;
    char *str = (char *)calloc(length + 1, sizeof(char)); // initialize a null terminated string

    for (int index = 0; index < length; index++) {
        // set the string at the index to the corresponding bit in the binary char array
        // if the integer value is 0, set the string value to '0', else set to '1'
        str[index] = (char) ((get_bit(input, (length - 1 - index) ) == 0) ? '0' : '1');
    }

    str[length] = '\0'; // null terminate the string
    return str;
}



/**
 *  This function cleanly frees the binary array struct.
 *  This needs to be called after a binary value is no longer
 *  needed.
 *
 *  @param input  the binary value to free
 *  @return void
 */
void free_binary(binary *input) {
    input->length = 0;
    free(input->binaryCharArray);  // free the binary char array
    input->binaryCharArray = NULL;
    free(input);                   // free the binary struct
}



/**
 *  This function returns the length of a specified binary
 *  (eg. an 11 element binary array has a length of 11)
 *
 *  @param input  the binary value
 *  @return  an integer value of the binary's length
 */
int get_length(binary const *input) {
    return input->length;
}



/**
 *  This function returns the bit at an index in a given binary value.
 *
 *  @param input  the input binary value
 *  @param index  the index of the requested bit
 *  @return  the integer representation of the bit (either 0 or 1)
 */
int get_bit(binary const *input, int index) {
    
    int byteIdx = index / BITS_IN_BYTE;  // get the index of the byte
    int bitIdx = index % BITS_IN_BYTE;   // get the bit index inside the byte

    if ( (index < 0) || index >= input->length ) {
        ThrowException("get_bit: The index specified is out of range");
    }

    // since the first section returns a hex value, shift the AND result back
    // to the ones place ( >> bitIdx)
    return ( (input->binaryCharArray[byteIdx] & (0x1 << bitIdx)) >> bitIdx);
}



/**
 *  This function sets a bit at an index in a given binary value.
 *
 *  @param input  the input binary value
 *  @param index  the index of the requested bit
 *  @param bit  the bit value to set (either a 0 or a 1)
 *  @return void
 */
void set_bit(binary *input, int index, int bit) {

    int byteIdx = index / BITS_IN_BYTE;  // get the index of the byte
    int bitIdx = index % BITS_IN_BYTE;   // get the bit index inside the byte

    if ( (index < 0) || index >= input->length ) {
        ThrowException("set_bit: The index specified is out of range");
    }

    if (bit == 1) {
        // OR the value at the location with a mask of 0s and a 1, which is at the index
        input->binaryCharArray[byteIdx] |= (0x1 << bitIdx);
    } else if (bit == 0) {
        // AND the value at the location with a mask of 1s and a 0, which is at the index
        input->binaryCharArray[byteIdx] &= ~(0x1 << bitIdx);
    } else {
        ThrowException("set_bit: Invalid bit entered (not a 0 or 1)");
    }
}



/**
 *  This is an internal helper function that doesn't need to be accessed.
 *  It resizes a binary value to a given length, either truncating the old
 *  binary value or padding its high-order bits with zeros. This is used 
 *  for simplifying operations between binary values of different lengths.
 *
 *  @param input  the binary value to be resized
 *  @param length  the new length of the binary value
 *  @return void
 */
void resize_binary(binary *input, int length) {
    // The length can't be less than one
    if (length <= 0) {
        ThrowException("resize_binary: The length specified is invalid");
    }

    int currentLength = get_length(input);

    if (currentLength != length) {
        binary *tmpResizedBinary = initialize_binary(length);  // initialize a new temporary binary

        int smallestLength = length;

        if (currentLength < length) {
            smallestLength = currentLength;
        }

        // set each bit of the new tmpResizedBinary to the old binary char array
        for (int index = 0; index < smallestLength; index++) {
            set_bit(tmpResizedBinary, index, get_bit(input, index));
        }


        free(input->binaryCharArray);                               // free the old binary char array
        input->length = length;                                     // set the new length
        input->binaryCharArray = tmpResizedBinary->binaryCharArray; // set the new binary char array
        tmpResizedBinary->binaryCharArray = NULL;                   // point the tmpResizedBinary char array to NULL
        free_binary(tmpResizedBinary);                              // wipe the temporary tmpResizedBinary struct
    }
}



/**
 *  This function copies everything from the binary 'input'
 *  to the binary 'copy'. Any two binary values can be 
 *  passed in as parameters.
 *
 *  @param copy  the binary which will store 'input''s values
 *  @param input  the input binary to be copied
 *  @return void
 */
void copy_binary(binary *copy, binary const *input) {
    int length = input->length;

    // Copy the values from input in case the user is
    // copying the value to itself (retarded idea)
    binary *temp = initialize_binary(0);
    temp->length = input->length;
    temp->binaryCharArray = input->binaryCharArray;

    free(copy->binaryCharArray);  // free the current value in the 'copy' binary

    // Allocate a new char array for the binary 'copy' and set the struct's fields
    int byteLength = length / BITS_IN_BYTE  +  (((length % BITS_IN_BYTE ) > 0) ? 1 : 0);
    unsigned char *newBinaryCharArray = (unsigned char *)calloc(byteLength, sizeof(unsigned char));
    copy->binaryCharArray = newBinaryCharArray;
    copy->length = length;
    
    // set each bit in 'copy' to the same as in 'temp'
    for (int index = 0; index < length; index++) {
        set_bit(copy, index, get_bit(temp, index));
    }

    temp->binaryCharArray = NULL; // Remove the pointer to 'input''s binaryCharArray
    free_binary(temp);            // Free the temporary value
}



/**
 *  ANDs two binary values (operand_A and operand_B) and stores
 *  the result in a new binary value 'result'. None of the binary
 *  values need to be the same size.
 *
 *  @param result  the result of the ANDing of the two operands
 *  @param operand_A  the first binary operand
 *  @param operand_B  the second binary operand
 *  @return void
 */
void AND_binary(binary *result, binary const *operand_A, binary const *operand_B) {
    // If the length of operand_A >= length of operand_B, return it, else 
    // return the length of operand_B
    int longestLength = (get_length(operand_A) >= get_length(operand_B)) ? get_length(operand_A) : get_length(operand_B);

    // Copy the two operands into two temporary values so that any the operation
    // can happen between any three binary values
    binary *temp_a = initialize_binary(0);
    binary *temp_b = initialize_binary(0);
    copy_binary(temp_a, operand_A);
    copy_binary(temp_b, operand_B);

    // Resize everything to the same size to make the operations easier
    resize_binary(temp_a, longestLength);
    resize_binary(temp_b, longestLength);
    resize_binary(result, longestLength);

    // AND the two temp values and store the result in the 'result' binary
    for (int index = 0; index < longestLength; index++) {
        set_bit(result, index, (get_bit(temp_a, index) & get_bit(temp_b, index)));
    }

    // Free the temporary binaries
    free_binary(temp_a);
    free_binary(temp_b);
}



/**
 *  ORs two binary values (operand_A and operand_B) and stores
 *  the result in a new binary value 'result'. None of the binary
 *  values need to be the same size.
 *
 *  @param result  the result of the ORing of the two operands
 *  @param operand_A  the first binary operand
 *  @param operand_B  the second binary operand
 *  @return void
 */
void OR_binary(binary *result, binary const *operand_A, binary const *operand_B) {
    // If the length of operand_A >= length of operand_B, return it, else 
    // return the length of operand_B
    int longestLength = (get_length(operand_A) >= get_length(operand_B)) ? get_length(operand_A) : get_length(operand_B);

    // Copy the two operands into two temporary values so that any the operation
    // can happen between any three binary values
    binary *temp_a = initialize_binary(0);
    binary *temp_b = initialize_binary(0);
    copy_binary(temp_a, operand_A);
    copy_binary(temp_b, operand_B);

    // Resize everything to the same size to make the operations easier
    resize_binary(temp_a, longestLength);
    resize_binary(temp_b, longestLength);
    resize_binary(result, longestLength);

    // OR the two temp values and store the result in the 'result' binary
    for (int index = 0; index < longestLength; index++) {
        set_bit(result, index, (get_bit(temp_a, index) | get_bit(temp_b, index)));
    }

    // Free the temporary binaries
    free_binary(temp_a);
    free_binary(temp_b);
}



/**
 *  XORs two binary values (operand_A and operand_B) and stores
 *  the result in a new binary value 'result'. None of the binary
 *  values need to be the same size.
 *
 *  @param result  the result of the XORing of the two operands
 *  @param operand_A  the first binary operand
 *  @param operand_B  the second binary operand
 *  @return void
 */
void XOR_binary(binary *result, binary const *operand_A, binary const *operand_B) {
    // If the length of operand_A >= length of operand_B, return it, else 
    // return the length of operand_B
    int longestLength = (get_length(operand_A) >= get_length(operand_B)) ? get_length(operand_A) : get_length(operand_B);

    // Copy the two operands into two temporary values so that any the operation
    // can happen between any three binary values
    binary *temp_a = initialize_binary(0);
    binary *temp_b = initialize_binary(0);
    copy_binary(temp_a, operand_A);
    copy_binary(temp_b, operand_B);

    // Resize everything to the same size to make the operations easier
    resize_binary(temp_a, longestLength);
    resize_binary(temp_b, longestLength);
    resize_binary(result, longestLength);

    // XOR the two temp values and store the result in the 'result' binary
    for (int index = 0; index < longestLength; index++) {
        set_bit(result, index, (get_bit(temp_a, index) ^ get_bit(temp_b, index)));
    }

    // Free the temporary binaries
    free_binary(temp_a);
    free_binary(temp_b);
}



/**
 *  Complements (inverts) every bit from an input binary and returns it
 *  in a new binary.
 *
 *  @param result  the result of the complement as a binary
 *  @param input  the binary input to be complemented
 *  @return void
 */
void complement_binary(binary *result, binary const *input) {
    int nextInvertedBit;
    int length = get_length(input); 
    resize_binary(result, length);  // resize the result to the same length as the 'input' binary
        
    for(int index = 0; index < length; index++) {
        nextInvertedBit = (get_bit(input, index) == 1) ? 0 : 1;  // invert the next bit in 'input'
        set_bit(result, index, nextInvertedBit);                 // set that inverted bit in 'result'
    }
}


// Need to finish shift_left and shift_right

