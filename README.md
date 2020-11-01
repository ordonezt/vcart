# VCART
_VCART (Very Cheap Argentinian Radio Telescope) esta basado en el proyecto "Mini Radio Telescope" de @jaguirre, @otinney y @brianxshen, el objetivo es poder realizar un mapa del firmamento en la banda Ku del espectro frecuencial, y de esta manera encontrar "puntos calientes" como el Sol y satelites utilizando una antena de DirecTV y un SDR de bajo costo_

## Componentes
* Antena parabolica (con LNB)
* Arduino Mega + Shield Ramps
* RTL-SDR
* Motores paso a paso


## Capturas
![Captura1](https://github.com/ordonezt/vcart/blob/master/Capturas/luna.png)
![Captura2](https://github.com/ordonezt/vcart/blob/master/Capturas/satelite_1.png)
![Captura3](https://github.com/ordonezt/vcart/blob/master/Capturas/satelite_2.png)


## Codigo
* El script de Python es [python_vcart_A.py](https://github.com/ordonezt/vcart/blob/develop/Python/SDR/python_vcart_A.py)
* El programa del Arduino es [Motores_Serial.ino](https://github.com/ordonezt/vcart/blob/develop/Arduino/Motores_Serial/Motores_Serial.ino)
