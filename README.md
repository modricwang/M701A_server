# M701A_server

## Environment
- Raspberry 4b 
- M701 sensor with UART
- Ubuntu 20.10
- Python - Miniforge3

## Preparation
### Turn on UART0 port
refer to: 
https://www.icode9.com/content-4-1055041.html

! Remember to turn off bluetooth

### connect the sensor to UART0 physical port
![img.png](img_connect.png)
Don't as me more about this. I just know this way works. ;)

### change UART0 port permissions
if your UART0 port mapping is '/dev/ttyAMA0':
```shell
sudo chmod 666 /dev/ttyAMA0 
```

## Run Server
### WIP