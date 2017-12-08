configuration SimpleAppC{
}
implementation{
	components MainC, SimpleC, LedsC, LabelServerC,ToolC;
	SimpleC.LabelServer-> LabelServerC;
	SimpleC.Leds->LedsC;
	SimpleC->MainC.Boot;
	SimpleC.ToolI->ToolC;
}
