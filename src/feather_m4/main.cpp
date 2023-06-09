#include <SPI.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include <Adafruit_MCP4728.h>
#include <Wire.h>

Adafruit_MCP4728 mcp;

Adafruit_INA219 ina219_A(0x40);
Adafruit_INA219 ina219_B(0x41);
Adafruit_INA219 ina219_C(0x44);
Adafruit_INA219 ina219_D(0x45);

const int chipSelect = 10;
int currenthour;
float set_voltage;

void setup(void)
{
  Serial.begin(115200);
  uint32_t currentFrequency;
  if (!mcp.begin(0x64)) {
    Serial.println("Failed to find MCP4728 chip");
    while (1) {
      delay(10);
    }
  }
}
void loop(void)
{

  float shuntvoltage_A = 0;
  float busvoltage_A = 0;
  float current_mA_A = 0;
  float loadvoltage_A = 0;
  float power_mW_A = 0;

  float shuntvoltage_B = 0;
  float busvoltage_B = 0;
  float current_mA_B = 0;
  float loadvoltage_B = 0;
  float power_mW_B = 0;


  if (!ina219_A.begin())
  {

    Serial.println("Failed to find INA219 A chip");
  }
  else
  {

    shuntvoltage_A = ina219_A.getShuntVoltage_mV();
    busvoltage_A = ina219_A.getBusVoltage_V();
    current_mA_A = ina219_A.getCurrent_mA();
    power_mW_A = ina219_A.getPower_mW();
    loadvoltage_A = busvoltage_A + (shuntvoltage_A / 1000);

    Serial.print("A Bus Voltage:   ");
    Serial.print(busvoltage_A);
    Serial.println(" V");
    Serial.print("A Current:       ");
    Serial.print(current_mA_A);
    Serial.println(" mA");
  }


  if (!ina219_B.begin())
  {

    Serial.println("Failed to find INA219 B chip");
  }

  else
  {

    shuntvoltage_B = ina219_B.getShuntVoltage_mV();
    busvoltage_B = ina219_B.getBusVoltage_V();
    current_mA_B = ina219_B.getCurrent_mA();
    power_mW_B = ina219_B.getPower_mW();
    loadvoltage_B = busvoltage_B + (shuntvoltage_B / 1000);

    // Serial.print("B Bus Voltage:   ");
    // Serial.print(busvoltage_B);
    // Serial.println(" V");
    // Serial.print("B Current:       ");
    // Serial.print(current_mA_B);
    // Serial.println(" mA");

  }
  



  if (Serial.available() > 0) {
    String receivedData = Serial.readString();
    Serial.print("Set Voltage:  ");
    Serial.println(receivedData);
    set_voltage = receivedData.toFloat();

  }



  Serial.print("Set Voltage:  ");
  Serial.println(set_voltage);
  float digital_v_input;
  digital_v_input = (1242.9 * set_voltage) - 2.796;
  Serial.print("digital intput:  ");
  Serial.println(digital_v_input); 
  Serial.println("");




  mcp.setChannelValue(MCP4728_CHANNEL_D, digital_v_input);
  mcp.saveToEEPROM();
  delay(3000);
}






























// }

// void loop() { delay(1000); }