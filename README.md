# VCART
_VCART (Very Cheap Argentinian Radio Telescope) esta basado en el proyecto "Mini Radio Telescope" de @jaguirre, @otinney y @brianxshen, el objetivo es poder realizar un mapa del firmamento en la frecuencia de 1 GHz aproximadamente, y de esta manera encontrar "puntos calientes" como el Sol y satelites utilizando una antena de DirecTV y un SDR de bajo costo_

## Componentes
* Antena parabolica (con LNB)
* Arduino Nano
* RTL-SDR
* Motores paso a paso


## Capturas
![Captura1](https://github.com/ordonezt/vcart/blob/master/Capturas/editado_mapa_potencia_1.0GHz_20x10_SOL.png)
![Captura2](https://github.com/ordonezt/vcart/blob/master/Capturas/editado_mapa_potencia_1.0GHz_20x20_sol_en_la_punta.png)
![Captura3](https://github.com/ordonezt/vcart/blob/master/Capturas/editado_mapa_potencia_1.0GHz_20x10_SATELITE.png)


## Codigo
* El script de Python es [python_vcart_A.py](https://github.com/ordonezt/vcart/blob/develop/Python/SDR/python_vcart_A.py)
* El programa del Arduino es [arduino_vcart_A.ino](https://github.com/ordonezt/vcart/blob/develop/Arduino/arduino_vcart_A/arduino_vcart_A.ino)
