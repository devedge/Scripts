## Info

A simple binary datatype for C written for the sake of convenience. <br><br>
The binary value is stored as bits in an unsigned char array, with 8 bits stored in each unsigned char.
The high-order bit is the farthest left value, and the low order bit is the rightmost value.<br><br>
This storage structure only matters when using 'set_bit()' or 'get_bit()', where the index specified follows these rules here. All of the other functions abstract this away.
<br><br>


&ensp;`high order bit (at index n, where n = length)`<br>
`/`<br>
`100000000010`<br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`\`<br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`low order bit at index 0`<br>

<br><br>

<code>index:&ensp;&ensp;7&ensp;6&ensp;5&ensp;4&ensp;3&ensp;2&ensp;1&ensp;0&ensp;&ensp;&ensp;&ensp;&ensp;15&ensp;&ensp;13&ensp;&ensp;11&ensp;&ensp;9&ensp;8&ensp;&ensp;&ensp;&ensp;&ensp;etc...</code><br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`|`&ensp;&ensp;&ensp;&ensp;&ensp;`14`&ensp;`12`&ensp;`10`&ensp;`|`<br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`|`&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;`|`&ensp;&ensp;`|`&ensp;`|`&ensp;&ensp;`|`<br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;<code>1&ensp;0&ensp;0&ensp;1&ensp;0&ensp;1&ensp;1&ensp;1</code>&ensp;&ensp;&ensp;&ensp;<code>0&ensp;0&ensp;0&ensp;0&ensp;0&ensp;1&ensp;1&ensp;0</code>&ensp;&ensp;&ensp;&ensp;<code>0&ensp;1&ensp;0&ensp;0&ensp;0&ensp;0&ensp;0&ensp;0</code><br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;<code>-&ensp;-&ensp;-&ensp;-&ensp;-&ensp;-&ensp;-&ensp;-</code>&ensp;&ensp;&ensp;&ensp;<code>-&ensp;-&ensp;-&ensp;-&ensp;-&ensp;-&ensp;-&ensp;-</code>&ensp;&ensp;&ensp;&ensp;<code>-&ensp;-&ensp;-&ensp;-&ensp;-&ensp;-&ensp;-&ensp;-</code><br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;<code>unsigned&ensp;char[0]</code>&ensp;&ensp;&ensp;<code>unsigned&ensp;char[1]</code>&ensp;&ensp;&ensp;<code>unsigned&ensp;char[2]</code><br>
<br>


How to include:

1. Save both 'binary_array.c' and 'binary_array.h' in the same directory as
    the C file that calls it
2. Add an include in your code for the header file (`#include "binary_array.h"`)
3. Use the functions defined in the header file
4. At compile time, compile the 'binary_array.c' file into an object file first:
    `gcc -std=c99 -c binary_array.c -o binary_array.o`
5. Then, compile the file that includes the 'binary_array.h' header with the
    object file generated:
    `gcc exampleFile.c binary_array.o -o exampleFile`
6. The file 'exampleFile' will now run using the functions defined in this
    header file.
