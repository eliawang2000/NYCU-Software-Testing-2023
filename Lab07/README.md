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
    
    <img width="706" alt="截圖 2023-05-01 下午8 15 12" src="https://user-images.githubusercontent.com/104348186/235620731-9ad25e94-257a-4a4f-918e-1fd8355968fb.png">

    

- Screenshot of crash detail (with ASAN error report)
    
    <img width="1257" alt="截圖 2023-05-01 下午8 15 59" src="https://user-images.githubusercontent.com/104348186/235620768-ee688bdd-44e2-4b31-8297-b077808acb1b.png">
