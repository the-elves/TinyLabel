module LabelServerC{
  provides interface LabelServer;
}
implementation{
	uint32_t labels[20];
	command error_t LabelServer.addLabel(uint8_t obj){
					return SUCCESS;
	}
	command error_t LabelServer.checkTransfer(uint8_t src,uint8_t dest){
					return SUCCESS;
	}

	uint32_t setLabel(uint8_t obj, uint8_t label){
		uint32_t j=1;
		uint8_t i;
		for( i = 0 ; i < label;i++){
			j = j<<1;
		}
		return labels[obj]|j;
	}

	error_t checkTransfer(uint8_t src, uint8_t dest){
		uint8_t i = 0;
		uint8_t srcLabel, destLabel;
		bool allowed = 1;
		uint32_t mask = 1;
		for(i=0;i<32;i++){
			srcLabel = labels[src] & mask;
			destLabel = labels[dest] & mask;
			if(srcLabel != 0 ){
				if(destLabel == 0){
					allowed=0;
					break;
				}
			}
		}
		if(allowed == 1)
			return SUCCESS;
		else
			return FAIL;
		
	}
}