module SimpleC{

	uses interface Leds;
	uses interface Boot;
	uses interface LabelServer;
	uses interface ToolI;
}
implementation{
	uint8_t   secret;

	uint8_t	  secret2;	

	event void Boot.booted(){

call LabelServer.addLabel(0, 1);

call LabelServer.addLabel(0, 2);

call LabelServer.addLabel(1, 3);

call LabelServer.addLabel(2, 1);

call LabelServer.addLabel(2, 2);

call LabelServer.addLabel(3, 2);

dbg("Boot","labels setup for all variables");
		dbg("Boot","I am up and running");

if ((call LabelServer.checkTransfer(2,1) == SUCCESS )&&(call LabelServer.checkTransfer(3,1) == SUCCESS )){ call ToolI.add(secret, secret2);} else {dbg("Boot","Cannot execute call ToolI.add(secret, secret2)");}

		secret = 0;

call LabelServer.modifyLabel(2, secret);
call LabelServer.modifyLabel(2, secret2);

		secret = secret + secret2;

	}



}

