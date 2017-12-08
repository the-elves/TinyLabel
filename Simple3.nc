module SimpleC{
	uses interface Leds##12;
	uses interface Boot;
	uses interface LabelServer;
	uses interface ToolI##1;
}
implementation{
	uint8_t   secret##1,2;
	uint8_t	  secret2##2;	
	event void Boot.booted(){
		dbg("Boot","I am up and running");
		call ToolI.add(secret, secret2);
		secret = 0;
		secret = secret + secret2;
	}

}
