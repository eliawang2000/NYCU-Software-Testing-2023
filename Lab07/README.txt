AFL
$ git clone https://github.com/google/AFL.git $ cd AFL
$ make
$ sudo make install

============================================================
Lab

cd Lab07
export CC=~/AFL/afl-gcc
export AFL_USE_ASAN=1
make
mkdir in
cp test.bmp in/
~/AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
./bmpgrayscale out/crashes/id:000000* a.bmp
