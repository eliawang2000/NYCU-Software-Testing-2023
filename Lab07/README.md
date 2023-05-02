# ST-Lab07

- PoC: the file that can trigger the vulnerability
    
    ~/out/crashes/id:000000*
    
- The commands (steps) that you used in this lab
    1. git clone [https://github.com/chameleon10712/NYCU-Software-Testing-2023.git](https://github.com/chameleon10712/NYCU-Software-Testing-2023.git)
    2. cd NYCU-Software-Testing-2023
    3. cp -r Lab07 ~/Lab07
    4. cd ..
    5. rm -r NYCU-Software-Testing-2023
    6. cd Lab07
    7. export CC=~/AFL/afl-gcc
    8. export AFL_USE_ASAN=1
    9. make
    10. mkdir in
    11. cp test.bmp in/
    12. ~/AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
    13. ./bmpgrayscale out/crashes/id:000000* a.bmp
    
- Screenshot of AFL running (with triggered crash)
    
    ![截圖 2023-05-01 下午8.15.12.png](ST-Lab07%20ac0c9821e84c477cbcb4c1b0e7968fab/%25E6%2588%25AA%25E5%259C%2596_2023-05-01_%25E4%25B8%258B%25E5%258D%25888.15.12.png)
    

- Screenshot of crash detail (with ASAN error report)
    
    ![截圖 2023-05-01 下午8.15.59.png](ST-Lab07%20ac0c9821e84c477cbcb4c1b0e7968fab/%25E6%2588%25AA%25E5%259C%2596_2023-05-01_%25E4%25B8%258B%25E5%258D%25888.15.59.png)