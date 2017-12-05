configuration SimpleAppC{
}
implementation{
	components MainC, SimpleC, LedsC, LabelServerC;
	SimpleC.LabelServer-> LabelServerC;
	SimpleC.Leds->LedsC;
	SimpleC->MainC.Boot;
	
}
