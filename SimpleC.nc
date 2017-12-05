module SimpleC{
	uses interface Leds;
	uses interface Boot;
	uses interface LabelServer;
}
implementation{
	uin8_t secret;
	
	event void Boot.booted(){
		dbg("Boot","I am up and running");
		call LabelServer.addLabel(93);
		call Leds.led0Toggle();
	}
}
