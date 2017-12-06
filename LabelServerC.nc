module LabelServerC{
  provides interface LabelServer;
}
implementation{
	uint32_t labels[20];

	error_t declassifyVar(uint8_t var, uint8_t label);
	uint32_t setLabel(uint8_t obj, uint8_t label);
	error_t checkTransfer(uint8_t src, uint8_t dest);
	
	command error_t LabelServer.addLabel(uint8_t obj, uint8_t label){
		uint32_t newPriv;
		newPriv = setLabel(labels[obj],label);
		if(newPriv == -1)
			return FAIL;
		else{
			labels[obj] = newPriv;
			return SUCCESS;
		}
	}
	command error_t LabelServer.checkTransfer(uint8_t src,uint8_t dest){
		return checkTransfer(src, dest);
	}

	command error_t LabelServer.declassify(uint8_t obj, uint8_t label){
		return declassifyVar(obj, label);
	}

	error_t declassifyVar(uint8_t var, uint8_t label){
		uint32_t mask;
		uint8_t i;
		mask = 1;
		for(i=0;i<label;i++){
			mask<<1;
		}
		mask = ~i;
		labels[var] = labels[var] & mask;
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