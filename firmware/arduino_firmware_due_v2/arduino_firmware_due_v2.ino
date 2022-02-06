/*
SCPI learning device
SCPI (standard commands for portable instruments)

Description:
Demonstrates the control of the brightness of a LED using SCPI commands.

Pinout:
- DO: led 1 (digital)
- DO: led 2 (pwm)

- DI: button
- AI: potentiometer
- AI: LM35 temperature sensor
- AO: ledLM35 temperature sensor

Hardware required:
A LED attached to digital pin 9
or a resistor from pin 9 to pin 13 to use the built-in LED

Classical Commands:
SOURce:VOLTage:RANGe value
SOURce:VOLTage value ... SOUR:VOLT 3.1

Commands:
  # working
  *IDN?
    Gets the instrument's identification string

  # not implemented
  *RST = *CLS
    Info: reset instrument. Set all switches off
    Example: *RST or *CLS
 
  OUTPut:VOLTage
    Example: OUTPut:VOLTage value
    Example: OUTP:VOLT value

*/

#include "Arduino.h"
#include "EEPROM.h"
#include "Vrekrer_scpi_parser.h"

// create SCPI communication object
SCPI_Parser my_instrument;

// constants
#define ADC_VREF_mV    5000.0 // in millivolt
#define ADC_RESOLUTION 1024.0

#define LM35_PIN A0
#define VOLTAGE_IN_PIN A1
#define VOLTAGE_OUT_PIN 10

// variables
//float temperatura;
//float voltage;
//float voltage_out;

int is_simulated_eeprom_addr = 0;
int is_simulated = 0;

int brightness = 0;
const int ledPin = 9;
const int intensity[11] = {0, 3, 5, 9, 15, 24, 38, 62, 99, 159, 255};

void setup()
{
  /* SCPI COMMANDS */
  // STATus Subsystem
  my_instrument.RegisterCommand(F("*IDN?"), &Identify);
  my_instrument.RegisterCommand(F("*RST"), &Reset);  
  my_instrument.RegisterCommand(F("*CLS"), &Reset);  

  // CONFIGure
  my_instrument.SetCommandTreeBase(F("CONFIgure"));
    my_instrument.RegisterCommand(F(":SIMUlation"), &SetSimulation);
    my_instrument.RegisterCommand(F(":SIMUlation?"), &GetSimulation);

  // Mmeasuring commands
  my_instrument.SetCommandTreeBase(F("MEASure"));
  my_instrument.RegisterCommand(F(":TEMPerature?"), &GetTemperature);
  my_instrument.RegisterCommand(F(":VOLTage?"), &GetVoltage); // MEAS:VOLT?
  //my_instrument.RegisterCommand(F(":CURRage?"), &GetCurrent);

  // control-output commands
  my_instrument.SetCommandTreeBase(F("OUTPut"));
    //my_instrument.RegisterCommand(F(":STATe"), &SetState); // main device on/off
    //my_instrument.RegisterCommand(F(":STATe?"), &GetState); // main device on/off
     my_instrument.RegisterCommand(F(":VOLTage"), &SetVoltage); // OUTP:VOLT 3.14

  // system specific
  my_instrument.SetCommandTreeBase(F("SYSTem:LED"));
    my_instrument.RegisterCommand(F(":BRIGhtness"), &SetBrightness);
    my_instrument.RegisterCommand(F(":BRIGhtness?"), &GetBrightness);
    my_instrument.RegisterCommand(F(":BRIGhtness:INCrease"), &IncDecBrightness);
    my_instrument.RegisterCommand(F(":BRIGhtness:DECrease"), &IncDecBrightness);


  /* SERIAL BEGIN */
  Serial.begin(9600);

  /* HARDWARE IO CONFIGURATION */
  //pinMode(ledPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(VOLTAGE_OUT_PIN, OUTPUT);  // sets the pin as output
  pinMode(VOLTAGE_IN_PIN, INPUT);   // sets the pin as output

  analogWrite(ledPin, 0);
  analogWrite(VOLTAGE_OUT_PIN, 0);

  // read configuration from EEPROM
  is_simulated = EEPROM.read(is_simulated_eeprom_addr);
}

void loop()
{
  // PROCESS SCPI COMMANDS
  my_instrument.ProcessInput(Serial, "\n");
}

// functions
float get_temperature(int pin){
  float senzor_celsius; 
  int senzor_adc;  
  float senzor_mv; 
  float senzor_fahrenheit; 
  
  // vrednost 10 bitnega registra ADC
  //senzor_adc = analogRead(A1);
  senzor_adc = analogRead(pin);
  
  // coversion: ADC -> mV
  senzor_mv = (senzor_adc/ADC_RESOLUTION)*ADC_VREF_mV;
  
  // coversion: mV -> °C
  // T[°C]=0,1[°𝐶/𝑚𝑉] ∗ 𝑈_𝑜𝑢𝑡 [𝑚𝑉]
  senzor_celsius = senzor_mv/10; 

  // coversion: °C -> °F
  senzor_fahrenheit = (senzor_celsius*9)/5 + 32;
 
  return senzor_celsius;
}

// functions
float get_voltage(int pin){
  float senzor_celsius; 
  int senzor_adc;  
  float senzor_mv; 
  
  // vrednost 10 bitnega registra ADC
  //senzor_adc = analogRead(A1);
  senzor_adc = analogRead(pin);
  
  // coversion: ADC -> mV
  senzor_mv = (senzor_adc/ADC_RESOLUTION)*ADC_VREF_mV;
  
  // coversion: mV -> °C
  // T[°C]=0,1[°𝐶/𝑚𝑉] ∗ 𝑈_𝑜𝑢𝑡 [𝑚𝑉]
  senzor_celsius = senzor_mv/10; 
 
  return senzor_celsius;
}

// functions
void SetSimulation(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  // For simplicity no bad parameter check is done.
  if (parameters.Size() > 0) {
    is_simulated = constrain(String(parameters[0]).toInt(), 0, 1);  

    // write to eeprom to preserve simulation status until next time
    EEPROM.write(is_simulated_eeprom_addr, is_simulated);

  }
}

void GetSimulation(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  // read configuration from EEPROM
  is_simulated = EEPROM.read(is_simulated_eeprom_addr);

  interface.println(String(is_simulated, DEC));
}

void Identify(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.println(F("ArduinoUNO,scpi_learning_device,#00,v0.1"));
}

void SetBrightness(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  // For simplicity no bad parameter check is done.
  if (parameters.Size() > 0) {
    brightness = constrain(String(parameters[0]).toInt(), 0, 10);
    analogWrite(ledPin, intensity[brightness]);
  }
}

void GetBrightness(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.println(String(brightness, DEC));
}

void IncDecBrightness(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  String last_header = String(commands.Last());
  last_header.toUpperCase();
  if (last_header.startsWith("INC")) {
    brightness = constrain(brightness + 1, 0, 10);
  } else { // "DEC"
    brightness = constrain(brightness - 1, 0, 10);
  }
  analogWrite(ledPin, intensity[brightness]);
}

/* function for MEASure:TEMPerature? */
void GetTemperature(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  float temperatura;
  temperatura = get_temperature(LM35_PIN);
  interface.println(String(temperatura, DEC));
  //interface.println(F("GetTemperature Executed"));
}

/* function for MEASure:VOLTage? MEAS:VOLT? */
void GetVoltage(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  int voltage_adc;
  //voltage = get_voltage(VOLTAGE_IN_PIN);
  voltage_adc = analogRead(VOLTAGE_IN_PIN);
  interface.println(String(voltage_adc, DEC));
  interface.println(F("getvoltage"));
}

/* function for setting voltage output OUTP:VOLT 3.14 value */
void SetVoltage(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  float voltage_v_out;
  int voltage_mv_out;
  int voltage_out_u8;

  // For simplicity no bad parameter check is done.
  if (parameters.Size() > 0) {

    // expected input is 0-5V
    voltage_v_out = constrain(String(parameters[0]).toFloat(), 0, 5);
    //voltage_v_out = String(parameters[0]).toFloat();
    voltage_mv_out = voltage_v_out *1000;

    // cant map decimal values. thats why in milivolts
    voltage_out_u8 = map(voltage_mv_out, 0, 5000, 0, 255);
    analogWrite(VOLTAGE_OUT_PIN, voltage_out_u8);
  }
  
  //interface.println(F("SetVoltage"));
  //interface.println(String(voltage_v_out, DEC));
  //interface.println(String(voltage_mv_out, DEC));
  //interface.println(String(voltage_out_u8, DEC));
}

/* function for *CLS and *RST command*/
void Reset(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  /* resets device. All variables and outputs are set to default state or 0. */
  interface.println(F("Reset"));
}
