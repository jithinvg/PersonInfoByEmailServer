from twisted.internet import reactor,protocol
import json
from rapportive import rapportive
import sys


sys.stdout.write("Person API Server Has Started")

class PersonProtocol(protocol.Protocol):

    def connectionMade(self):
        try:
            sys.stdout.write("Connected to host @"+self.transport.getPeer().host+".\n")
        except:
            sys.stdout.write("ERROR: Some error occured during connection")       
            
            
    
    def dataReceived(self, data):
        try:
            sys.stdout.write("Host @"+self.transport.getPeer().host+" asked for: "+data) 
            profile = rapportive.request(data)
            data_info = {}
            
            has_data  = False
            try:
                data_info["name"] = profile.name
                has_data = True
            except:
                pass
            try:
                data_info["memberships"] = profile.memberships
                has_data = True
            except:
                pass
            try:
                data_info["jobinfo"] = profile.jobinfo
                has_data = True
            except:
                pass

            encoded_data = ""
            
        
            if has_data == True:
                data_info["CODE"] = 1
                encoded_data = json.dumps(data_info)      
            else:
                error_data = {"CODE":0,"ERROR":"Could not find Email id", "ERROR_CODE":404}
                encoded_data = json.dumps(error_data)
        
            self.transport.write(encoded_data)
        except:
            data_info = {"CODE":0,"ERROR":"Internal Server Error", "ERROR_CODE":500}
            encoded_data = json.dumps(data_info)
            self.transport.write(encoded_data)
        self.transport.loseConnection()
    

class PersonFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return PersonProtocol()
    

reactor.listenTCP(34892, PersonFactory())
reactor.run()

