echo off
cd /d  C:/Program Files/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin  
STM32_Programmer_CLI.exe -C port=SWD freq=4000 -w  "D:/ATE-work/Cefaly4_Enhance_v1.00.004.hex  "-v -rst