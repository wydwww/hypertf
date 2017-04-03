# a client running on every physical server 
from requests import put, get

rm_addr = "http://localhost:5000"

class client_on_physical_server:
    def __init__(self, rm_address):
        self.rm_addr = rm_address

    def update_resource_info(self, resource):
        # resource is a set of attributes of a physical server, such as id, GPU, etc
        put(self.rm_addr + "/resources/node1", data = {"idle": 0, "id": resource["id"]})

# get resource from this server
def get_resource():
    pass
    return resource

resource_get = get_resource()

# connect to resource manager
rm = client(rm_addr)

# send the resource info to resource manager
rm.update_resource_info(resource_get)



