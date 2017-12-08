module ToolC{
	provides interface ToolI;
}
implementation{
	command error_t ToolI.add(uint8_t i1, uint8_t i2){
                return SUCCESS;
        }	
}
