#define BAUDRATE        9600
#define PIN_LED         13
#define MILLIS_BLINK    400
#define MILLIS_MOTORES  100

typedef struct{
  byte pin;
  byte estado;
}led_t;

//Ambas medidas son relativas al posicionamiento
typedef struct{
  byte azimut;
  byte elevacion;
}posicion_t;

typedef struct{
  bool superior;
  bool inferior;
  bool derecha;
  bool izquierda;
}fin_carrera_t;

typedef struct{
  bool estado;
  unsigned long tiempo;
}espera_t;

typedef enum{
  ESPERANDO_INICIO,
  ESPERANDO_COMANDO,
  ESPERANDO_FINAL
}uart_estado_t;

void maquinaUart(char);

led_t led_blink = {PIN_LED, LOW};
posicion_t posicion = {10, 60};
fin_carrera_t fin_carrera = {false, false, false, false};
espera_t espera_motores = {false, 0};
unsigned long tiempo_blink = 0;
void (*accion)(void) = NULL;

void setup() {
  // put your setup code here, to run once:
   Serial.begin(BAUDRATE);
   pinMode(led_blink.pin, OUTPUT);
   tiempo_blink = millis();
}

void loop() {
  //Blinky (Prueba de que estamos vivos)
  if(millis() - tiempo_blink > MILLIS_BLINK)
  {
    tiempo_blink = millis();
    digitalWrite(led_blink.pin, led_blink.estado);
    led_blink.estado = ~led_blink.estado;
    //enviarEstado();
  }

  //Fines de carrera ficticios
  if(posicion.elevacion == 0)
  {
    fin_carrera.superior = false;
    fin_carrera.inferior = true;
    posicion.elevacion = 0;
  }
  else if(posicion.elevacion == 255)
  {
    fin_carrera.superior = true;
    fin_carrera.inferior = false;
    posicion.elevacion = 255;
  }

  if(posicion.azimut == 0)
  {
    fin_carrera.izquierda = false;
    fin_carrera.derecha = true;
    posicion.azimut = 0;
  }
  else if(posicion.azimut == 255)
  {
    fin_carrera.izquierda = true;
    fin_carrera.derecha = false;
    posicion.azimut = 255;
  }

  //Maquina de estados de la UART
  if(Serial.available() > 0)
  {
    maquinaUart(Serial.read());
  }

  if(espera_motores.estado == false)
  {
    if(accion != NULL)
    {
      accion();
      espera_motores.estado = true;
      espera_motores.tiempo = millis();
    }
  }

  if(espera_motores.estado == true)
    if(millis() - espera_motores.tiempo > MILLIS_MOTORES)
      {
        espera_motores.estado = false;
        //Aviso que ya termino la espera y estamos listos para un nuevo comando
        Serial.println("<OK>");
      }
}
/*############FIN DEL LOOP#############*/


void maquinaUart(char caracter)
{
  static uart_estado_t estado = ESPERANDO_INICIO;
  static char comando = 0;
  bool validar_trama = false;
  
  switch(estado)
  {
    case ESPERANDO_INICIO:
      if(caracter == '<')
        estado = ESPERANDO_COMANDO;
    break;

    case ESPERANDO_COMANDO:
      comando = caracter;
      estado = ESPERANDO_FINAL;
    break;

    case ESPERANDO_FINAL:
      if(caracter == '>')
      {
        validar_trama = true;
        Serial.println("Trama recibida");
      }
      else
        Serial.println("Error de trama");
      
      estado = ESPERANDO_INICIO;
    break;

    default:
      Serial.println("Error de trama");
      estado = ESPERANDO_INICIO;
    break;
  }

  if(validar_trama == true)
  {
   validar_trama = false; 
   
    switch(comando)
    {
      //Reset
      case '0':
        accion = reiniciar;
      break;

      //Estado
      case 'S':
        enviarEstado();
      break;

      //Derecha
      case 'R':
        accion = derecha;
      break;

      //Izquierda
      case 'L':
        accion = izquierda;
      break;

      //Arriba
      case 'U':
        accion = arriba;
      break;

      //Abajo
      case 'D':
        accion = abajo;
      break;
    }
  }
}

void reiniciar(void)
{
  if(fin_carrera.inferior == false)
  {
    abajo();
    accion = reiniciar;
    return;
  }

  if(fin_carrera.derecha == false)
  {
    derecha();
    accion = reiniciar;
    return;
  }

  //Si llego aca ya estoy en la posicion inicial, dejo de iterar
  Serial.println("<0>");
  accion = NULL;
}

void arriba(void)
{
  if(fin_carrera.superior == false)
  {
    posicion.elevacion++;
    Serial.println("<U>");
  }

  accion = NULL;
}

void abajo(void)
{
  if(fin_carrera.inferior == false)
  {
    posicion.elevacion--;
    Serial.println("<D>");
  }
  
  accion = NULL;
}

void derecha(void)
{
  if(fin_carrera.derecha == false)
  {
    posicion.azimut--;
    Serial.println("<R>");
  }
  
  accion = NULL;
}

void izquierda(void)
{
  if(fin_carrera.izquierda == false)
  {
    posicion.azimut++;
    Serial.println("<L>");
  }
  
  accion = NULL;
}

void enviarEstado(void)
{
  Serial.print("<S");
  Serial.print(posicion.elevacion, DEC);
  Serial.print('@');
  Serial.print(posicion.azimut, DEC);
  Serial.print('@');
  Serial.print(fin_carrera.derecha, BIN);
  Serial.print(fin_carrera.izquierda, BIN);
  Serial.print(fin_carrera.inferior, BIN);
  Serial.print(fin_carrera.superior, BIN);
  //Serial.print((char)(fin_carrera.derecha << 3 | fin_carrera.izquierda << 2 | fin_carrera.inferior << 1 | fin_carrera.superior << 0));
  Serial.println('>');
}
