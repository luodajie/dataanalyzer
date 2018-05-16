import ConfigParser
import os

def dsn_details():
	config = ConfigParser.ConfigParser()
	config.readfp(open(os.path.join(os.getcwd(),"default_config.cfg")))

	hostname = config.get("Oracle_Config", "hostname")
	port = config.get("Oracle_Config", "port")
	service_name = config.get("Oracle_Config", "service_name")

	dsn =  hostname+":"+port+"/"+service_name
	return str(dsn)



# dsn =  str(hostname).rstrip("\n")+":"+str(port).rstrip("\n")+"/"+str(service_name).rstrip("\n")