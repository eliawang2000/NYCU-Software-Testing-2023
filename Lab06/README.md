# ST-Lab06

- Environment
    
    <aside>
    💡 DISTRIB_ID=Ubuntu
    DISTRIB_RELEASE=16.04
    DISTRIB_CODENAME=xenial
    DISTRIB_DESCRIPTION="Ubuntu 16.04.7 LTS"
    
    </aside>
    
- Result
    
    
    |  | Valgrind | ASan |
    | --- | --- | --- |
    | Heap out-of-bounds | O | O |
    | Stack out-of-bounds | X | O |
    | Global out-of-bounds | X | O |
    | use-after-free | O | O |
    | use-after-return | O | O |
- Heap out-of-bounds
    1. code
        
        ```cpp
        #include <stdlib.h>
        
        int main(int argc, char **argv){
          int *array = new int[100];
          array[100] = 0; // BOOM
          int res = array[argc + 100];  // BOOM
          delete [] array;
          return res;
        }
        ```
        
    2. Valgrind report
        
        ```cpp
        ==3560== Memcheck, a memory error detector
        ==3560== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
        ==3560== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
        ==3560== Command: ./heap
        ==3560== 
        ==3560== Invalid write of size 4
        ==3560==    at 0x40066D: main (in /home/alphabet/Elia/heap)
        ==3560==  Address 0x5b1ae10 is 0 bytes after a block of size 400 alloc'd
        ==3560==    at 0x4C2E80F: operator new[](unsigned long) (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        ==3560==    by 0x40065E: main (in /home/alphabet/Elia/heap)
        ==3560== 
        ==3560== Invalid read of size 4
        ==3560==    at 0x40068B: main (in /home/alphabet/Elia/heap)
        ==3560==  Address 0x5b1ae14 is 4 bytes after a block of size 400 alloc'd
        ==3560==    at 0x4C2E80F: operator new[](unsigned long) (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        ==3560==    by 0x40065E: main (in /home/alphabet/Elia/heap)
        ==3560== 
        ==3560== 
        ==3560== HEAP SUMMARY:
        ==3560==     in use at exit: 72,704 bytes in 1 blocks
        ==3560==   total heap usage: 2 allocs, 1 frees, 73,104 bytes allocated
        ==3560== 
        ==3560== LEAK SUMMARY:
        ==3560==    definitely lost: 0 bytes in 0 blocks
        ==3560==    indirectly lost: 0 bytes in 0 blocks
        ==3560==      possibly lost: 0 bytes in 0 blocks
        ==3560==    still reachable: 72,704 bytes in 1 blocks
        ==3560==         suppressed: 0 bytes in 0 blocks
        ==3560== Rerun with --leak-check=full to see details of leaked memory
        ==3560== 
        ==3560== For counts of detected and suppressed errors, rerun with: -v
        ==3560== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
        ```
        
    3. ASan report
        
        ```cpp
        =================================================================
        ==3646==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61400000ffd0 at pc 0x00000040080e bp 0x7ffd24899bf0 sp 0x7ffd24899be0
        WRITE of size 4 at 0x61400000ffd0 thread T0
            #0 0x40080d in main /home/alphabet/Elia/heap.cpp:5
            #1 0x7fe19f3a883f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2083f)
            #2 0x400708 in _start (/home/alphabet/Elia/heap2+0x400708)
        
        0x61400000ffd0 is located 0 bytes to the right of 400-byte region [0x61400000fe40,0x61400000ffd0)
        allocated by thread T0 here:
            #0 0x7fe19f7eb712 in operator new[](unsigned long) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x99712)
            #1 0x4007e2 in main /home/alphabet/Elia/heap.cpp:4
        
        SUMMARY: AddressSanitizer: heap-buffer-overflow /home/alphabet/Elia/heap.cpp:5 main
        Shadow bytes around the buggy address:
          0x0c287fff9fa0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fff9fb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fff9fc0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
          0x0c287fff9fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0c287fff9fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        =>0x0c287fff9ff0: 00 00 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa
          0x0c287fffa000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fffa010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fffa020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fffa030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fffa040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
        Shadow byte legend (one shadow byte represents 8 application bytes):
          Addressable:           00
          Partially addressable: 01 02 03 04 05 06 07 
          Heap left redzone:       fa
          Heap right redzone:      fb
          Freed heap region:       fd
          Stack left redzone:      f1
          Stack mid redzone:       f2
          Stack right redzone:     f3
          Stack partial redzone:   f4
          Stack after return:      f5
          Stack use after scope:   f8
          Global redzone:          f9
          Global init order:       f6
          Poisoned by user:        f7
          Container overflow:      fc
          Array cookie:            ac
          Intra object redzone:    bb
          ASan internal:           fe
        ==3646==ABORTING
        ```
        
    4. Conclusion
        
        Valgrind 可以／ASan 可以
        
- Stack out-of-bounds
    1. code
        
        ```cpp
        #include <iostream>
        #include <cstdlib>
        
        using namespace std;
        int num[5]; 
        int main() {
            
            for (int i = 0; i <= 5; i++) {
                num[i] = i; // i = 5, BOOM
            }
        
            cout << num[6] << endl; // BOOM
        
            return 0;
        }
        ```
        
    2. Valgrind report
        
        ```cpp
        ==27765== Memcheck, a memory error detector
        ==27765== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
        ==27765== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
        ==27765== Command: ./stack
        ==27765== 
        0
        ==27765== 
        ==27765== HEAP SUMMARY:
        ==27765==     in use at exit: 72,704 bytes in 1 blocks
        ==27765==   total heap usage: 2 allocs, 1 frees, 73,728 bytes allocated
        ==27765== 
        ==27765== LEAK SUMMARY:
        ==27765==    definitely lost: 0 bytes in 0 blocks
        ==27765==    indirectly lost: 0 bytes in 0 blocks
        ==27765==      possibly lost: 0 bytes in 0 blocks
        ==27765==    still reachable: 72,704 bytes in 1 blocks
        ==27765==         suppressed: 0 bytes in 0 blocks
        ==27765== Rerun with --leak-check=full to see details of leaked memory
        ==27765== 
        ==27765== For counts of detected and suppressed errors, rerun with: -v
        ==27765== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
        ```
        
    3. ASan report
        
        ```cpp
        =================================================================
        ==28201==ERROR: AddressSanitizer: global-buffer-overflow on address 0x000000602274 at pc 0x000000400c2e bp 0x7ffe2c6f1660 sp 0x7ffe2c6f1650
        WRITE of size 4 at 0x000000602274 thread T0
            #0 0x400c2d in main /home/alphabet/Elia/stack.cpp:17
            #1 0x7f365379c83f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2083f)
            #2 0x400a28 in _start (/home/alphabet/Elia/stack2+0x400a28)
        
        0x000000602274 is located 44 bytes to the left of global variable '__ioinit' defined in '/usr/include/c++/5/iostream:74:25' (0x6022a0) of size 1
          '__ioinit' is ascii string ''
        0x000000602274 is located 0 bytes to the right of global variable 'num' defined in 'stack.cpp:13:5' (0x602260) of size 20
        SUMMARY: AddressSanitizer: global-buffer-overflow /home/alphabet/Elia/stack.cpp:17 main
        Shadow bytes around the buggy address:
          0x0000800b83f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8410: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8420: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8430: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        =>0x0000800b8440: 00 00 00 00 00 00 00 00 00 00 00 00 00 00[04]f9
          0x0000800b8450: f9 f9 f9 f9 01 f9 f9 f9 f9 f9 f9 f9 00 00 00 00
          0x0000800b8460: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8470: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8490: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Shadow byte legend (one shadow byte represents 8 application bytes):
          Addressable:           00
          Partially addressable: 01 02 03 04 05 06 07 
          Heap left redzone:       fa
          Heap right redzone:      fb
          Freed heap region:       fd
          Stack left redzone:      f1
          Stack mid redzone:       f2
          Stack right redzone:     f3
          Stack partial redzone:   f4
          Stack after return:      f5
          Stack use after scope:   f8
          Global redzone:          f9
          Global init order:       f6
          Poisoned by user:        f7
          Container overflow:      fc
          Array cookie:            ac
          Intra object redzone:    bb
          ASan internal:           fe
        ==28201==ABORTING
        ```
        
    4. Conclusion
        
        Valgrind 不可以／ASan 可以
        
- Global out-of-bounds
    1. code
        
        ```cpp
        #include <stdlib.h>
        int global_array[10];
        int main(int argc, char **argv){
        //   return global_array[argc + 100];  // BOOM
            global_array[10] = 0; // out-of-bounds write
            int x = global_array[11]; // out-of-bounds read
            return 0;
        }
        ```
        
    2. Valgrind report
        
        ```cpp
        ==3923== Memcheck, a memory error detector
        ==3923== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
        ==3923== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
        ==3923== Command: ./global
        ==3923== 
        ==3923== 
        ==3923== HEAP SUMMARY:
        ==3923==     in use at exit: 0 bytes in 0 blocks
        ==3923==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
        ==3923== 
        ==3923== All heap blocks were freed -- no leaks are possible
        ==3923== 
        ==3923== For counts of detected and suppressed errors, rerun with: -v
        ==3923== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
        ```
        
    3. ASan report
        
        ```cpp
        =================================================================
        ==4054==ERROR: AddressSanitizer: global-buffer-overflow on address 0x000000601108 at pc 0x0000004007cc bp 0x7ffd2a825570 sp 0x7ffd2a825560
        WRITE of size 4 at 0x000000601108 thread T0
            #0 0x4007cb in main /home/alphabet/Elia/global.cpp:5
            #1 0x7f2e33ef883f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2083f)
            #2 0x4006d8 in _start (/home/alphabet/Elia/global2+0x4006d8)
        
        0x000000601108 is located 0 bytes to the right of global variable 'global_array' defined in 'global.cpp:2:5' (0x6010e0) of size 40
        SUMMARY: AddressSanitizer: global-buffer-overflow /home/alphabet/Elia/global.cpp:5 main
        Shadow bytes around the buggy address:
          0x0000800b81d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b81e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b81f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8210: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        =>0x0000800b8220: 00[f9]f9 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
          0x0000800b8230: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8240: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8250: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8260: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0000800b8270: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Shadow byte legend (one shadow byte represents 8 application bytes):
          Addressable:           00
          Partially addressable: 01 02 03 04 05 06 07 
          Heap left redzone:       fa
          Heap right redzone:      fb
          Freed heap region:       fd
          Stack left redzone:      f1
          Stack mid redzone:       f2
          Stack right redzone:     f3
          Stack partial redzone:   f4
          Stack after return:      f5
          Stack use after scope:   f8
          Global redzone:          f9
          Global init order:       f6
          Poisoned by user:        f7
          Container overflow:      fc
          Array cookie:            ac
          Intra object redzone:    bb
          ASan internal:           fe
        ==4054==ABORTING
        ```
        
    4. Conclusion
        
        Valgrind 不可以／ASan 可以
        
- Use-after-free
    1. code
        
        ```cpp
        #include <stdlib.h>
        
        int main(int argc, char **argv){
          int *array = new int[100];
          delete [] array;
          return array[argc];  // BOOM
        }
        ```
        
    2. Valgrind report
        
        ```cpp
        ==4133== Memcheck, a memory error detector
        ==4133== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
        ==4133== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
        ==4133== Command: ./free
        ==4133== 
        ==4133== Invalid read of size 4
        ==4133==    at 0x40068A: main (in /home/alphabet/Elia/free)
        ==4133==  Address 0x5b1ac84 is 4 bytes inside a block of size 400 free'd
        ==4133==    at 0x4C2F74B: operator delete[](void*) (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        ==4133==    by 0x400675: main (in /home/alphabet/Elia/free)
        ==4133==  Block was alloc'd at
        ==4133==    at 0x4C2E80F: operator new[](unsigned long) (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        ==4133==    by 0x40065E: main (in /home/alphabet/Elia/free)
        ==4133== 
        ==4133== 
        ==4133== HEAP SUMMARY:
        ==4133==     in use at exit: 72,704 bytes in 1 blocks
        ==4133==   total heap usage: 2 allocs, 1 frees, 73,104 bytes allocated
        ==4133== 
        ==4133== LEAK SUMMARY:
        ==4133==    definitely lost: 0 bytes in 0 blocks
        ==4133==    indirectly lost: 0 bytes in 0 blocks
        ==4133==      possibly lost: 0 bytes in 0 blocks
        ==4133==    still reachable: 72,704 bytes in 1 blocks
        ==4133==         suppressed: 0 bytes in 0 blocks
        ==4133== Rerun with --leak-check=full to see details of leaked memory
        ==4133== 
        ==4133== For counts of detected and suppressed errors, rerun with: -v
        ==4133== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
        ```
        
    3. ASan report
        
        ```cpp
        ==4185==ERROR: AddressSanitizer: heap-use-after-free on address 0x61400000fe44 at pc 0x0000004007d4 bp 0x7ffdf04f2b10 sp 0x7ffdf04f2b00
        READ of size 4 at 0x61400000fe44 thread T0
            #0 0x4007d3 in main /home/alphabet/Elia/free.cpp:6
            #1 0x7fa1ecb4d83f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2083f)
            #2 0x4006b8 in _start (/home/alphabet/Elia/free2+0x4006b8)
        
        0x61400000fe44 is located 4 bytes inside of 400-byte region [0x61400000fe40,0x61400000ffd0)
        freed by thread T0 here:
            #0 0x7fa1ecf90d0a in operator delete[](void*) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x99d0a)
            #1 0x4007a7 in main /home/alphabet/Elia/free.cpp:5
        
        previously allocated by thread T0 here:
            #0 0x7fa1ecf90712 in operator new[](unsigned long) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x99712)
            #1 0x400797 in main /home/alphabet/Elia/free.cpp:4
        
        SUMMARY: AddressSanitizer: heap-use-after-free /home/alphabet/Elia/free.cpp:6 main
        Shadow bytes around the buggy address:
          0x0c287fff9f70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fff9f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fff9f90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fff9fa0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fff9fb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
        =>0x0c287fff9fc0: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd
          0x0c287fff9fd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
          0x0c287fff9fe0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
          0x0c287fff9ff0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
          0x0c287fffa000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
          0x0c287fffa010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
        Shadow byte legend (one shadow byte represents 8 application bytes):
          Addressable:           00
          Partially addressable: 01 02 03 04 05 06 07 
          Heap left redzone:       fa
          Heap right redzone:      fb
          Freed heap region:       fd
          Stack left redzone:      f1
          Stack mid redzone:       f2
          Stack right redzone:     f3
          Stack partial redzone:   f4
          Stack after return:      f5
          Stack use after scope:   f8
          Global redzone:          f9
          Global init order:       f6
          Poisoned by user:        f7
          Container overflow:      fc
          Array cookie:            ac
          Intra object redzone:    bb
          ASan internal:           fe
        ==4185==ABORTING
        ```
        
    4. Conclusion
        
        Valgrind 可以／ASan 可以
        
- Use-after-return
    1. code
        
        ```cpp
        #include <iostream>
        using namespace std;
        
        int *ptr;
        __attribute__((noinline))
        void FunctionThatEscapesLocalObject() {
          int local[100];
          ptr = &local[0];
        }
        
        int main(int argc, char **argv) {
          FunctionThatEscapesLocalObject();
          return ptr[argc];
        }
        ```
        
    2. Valgrind report
        
        ```cpp
        ==5404== Memcheck, a memory error detector
        ==5404== Copyright (C) 2002-2015, and GNU GPL'd, by Julian Seward et al.
        ==5404== Using Valgrind-3.11.0 and LibVEX; rerun with -h for copyright info
        ==5404== Command: ./return
        ==5404== 
        ==5404== Invalid read of size 4
        ==5404==    at 0x40078D: main (in /home/alphabet/Elia/return)
        ==5404==  Address 0xffefffa94 is on thread 1's stack
        ==5404==  428 bytes below stack pointer
        ==5404== 
        ==5404== 
        ==5404== HEAP SUMMARY:
        ==5404==     in use at exit: 72,704 bytes in 1 blocks
        ==5404==   total heap usage: 1 allocs, 0 frees, 72,704 bytes allocated
        ==5404== 
        ==5404== LEAK SUMMARY:
        ==5404==    definitely lost: 0 bytes in 0 blocks
        ==5404==    indirectly lost: 0 bytes in 0 blocks
        ==5404==      possibly lost: 0 bytes in 0 blocks
        ==5404==    still reachable: 72,704 bytes in 1 blocks
        ==5404==         suppressed: 0 bytes in 0 blocks
        ==5404== Rerun with --leak-check=full to see details of leaked memory
        ==5404== 
        ==5404== For counts of detected and suppressed errors, rerun with: -v
        ==5404== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
        ```
        
    3. ASan report
        
        ```cpp
        =================================================================
        ==11917==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f66ccc00024 at pc 0x000000400c07 bp 0x7ffe6606d170 sp 0x7ffe6606d160
        READ of size 4 at 0x7f66ccc00024 thread T0
            #0 0x400c06 in main /home/alphabet/Elia/return.cpp:13
            #1 0x7f66d03e883f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2083f)
            #2 0x4009f8 in _start (/home/alphabet/Elia/return2+0x4009f8)
        
        Address 0x7f66ccc00024 is located in stack of thread T0 at offset 36 in frame
            #0 0x400ad5 in FunctionThatEscapesLocalObject() /home/alphabet/Elia/return.cpp:6
        
          This frame has 1 object(s):
            [32, 432) 'local' <== Memory access at offset 36 is inside this variable
        HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
              (longjmp and C++ exceptions *are* supported)
        SUMMARY: AddressSanitizer: stack-use-after-return /home/alphabet/Elia/return.cpp:13 main
        Shadow bytes around the buggy address:
          0x0fed59977fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0fed59977fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0fed59977fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0fed59977fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0fed59977ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        =>0x0fed59978000: f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
          0x0fed59978010: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
          0x0fed59978020: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
          0x0fed59978030: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 00 00 00 00
          0x0fed59978040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
          0x0fed59978050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Shadow byte legend (one shadow byte represents 8 application bytes):
          Addressable:           00
          Partially addressable: 01 02 03 04 05 06 07 
          Heap left redzone:       fa
          Heap right redzone:      fb
          Freed heap region:       fd
          Stack left redzone:      f1
          Stack mid redzone:       f2
          Stack right redzone:     f3
          Stack partial redzone:   f4
          Stack after return:      f5
          Stack use after scope:   f8
          Global redzone:          f9
          Global init order:       f6
          Poisoned by user:        f7
          Container overflow:      fc
          Array cookie:            ac
          Intra object redzone:    bb
          ASan internal:           fe
        ==11917==ABORTING
        ```
        
    4. Conclusion
        
        Valgrind 可以／ASan 可以
        
- Part2
    1. code
        
        ```cpp
        #include <iostream>
        using namespace std;
        
        int main() {
            int a[8];
            int b[8];
        
            for (int i = 0; i < 8; i++) {
                a[i] = i;
                b[i] = i;
            }
        
            cout << &a << endl;
            cout << &b << endl;
            cout << a[8+32] << endl;
        
            return 0;
        }
        ```
        
    2. ASan report
        
        0
        
    3. Conclusion
        
        越過red zone，所以ASan找不到錯誤。