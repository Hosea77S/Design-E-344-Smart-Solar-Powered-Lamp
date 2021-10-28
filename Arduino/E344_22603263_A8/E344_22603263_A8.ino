//SH Phetla 22603263

/*
 * Includes
 */


/*
 * Global variables for Pins
 */
 const int LDR_Pin = A1; //Samples light sensor data
 const int SupplyVoltage_Pin = 10; //Samples Supply voltage level
 const int BatteryVoltage_Pin = A0;//Samples battery voltage level
 const int BatteryCurrent_Pin = A2;//Samples Battaery current data
 const int OverChargeProtection_Pin = 11;//Used to output overcharge protection signal

 /*
  * Global variables to process data
  */
String OVstring = "OV0";
bool OVstatus = false;
float BatteryVoltage = 0;
float SupplyVoltage = 0;
float BatteryCurrent = 0;
byte AmbientLight = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(OverChargeProtection_Pin, OUTPUT);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:

//Read keyboard command to determine whether to allow charging or not
  SetOverChargeControl();

//send the rest of the data
  CalibrateCircuitData();
  TransmitCircuitData();
  
  delay(1000);//Wait 1 second

}

void SetOverChargeControl()
{

  
  if(Serial.available() > 0)
  {
    OVstring = Serial.readString();

    if(OVstring[2] == '0')
    {
      OVstatus = false;
    }
    else if(OVstring[2] == '1')
    {
      OVstatus = true;
    }
  }
  return;
}

void CalibrateCircuitData()
{
  float BVres = 5.0/(1023.0*3.5357); //battery voltage resolution [V/bit]
  float BVmin = 5.9;//Minimum battery voltage
  float SVres = 5.0*5.0/1023.0;//Supply voltage resolution [V/bit]
  float Rmax = 1023.0;//ADC maximum value [bits]
  float Vref = 1.75; //Current sesing reference voltage [V]
  float Rmax_ambientLight = 970.0;//maximum light intensity sampled value [bits]
  
  BatteryVoltage = (float)(analogRead(BatteryVoltage_Pin))*BVres + BVmin;
  SupplyVoltage = (float)(analogRead(SupplyVoltage_Pin))*SVres;
  BatteryCurrent = ( (float)(analogRead(BatteryCurrent_Pin))/Rmax - Vref/5.0 )*1000;
  AmbientLight = (byte)((float)(analogRead(LDR_Pin))*(100/Rmax_ambientLight));

  //If battery is nearly fully charged or charging current is too high, Stop charging
  if((BatteryVoltage > 7.2) || (BatteryCurrent > 410.0))
  {
    OVstatus = false;
    OVstring[2] = '0';
  }
}

void TransmitCircuitData()
{
  String comma = " , ";//Delemeter
  digitalWrite(OverChargeProtection_Pin, OVstatus);
  Serial.println(OVstatus + comma + BatteryVoltage + comma + SupplyVoltage + comma + BatteryCurrent + comma + AmbientLight);
}
