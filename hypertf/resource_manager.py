#!flask/bin/python

# resource manager, it's a server connecting to cluster runner clients 
# , and resource query clients on physical servers
# , and a client connecting to zookeeper server

from flask import Flask, jsonify, abort, request, make_response, url_for
from kazoo.client import KazooClient
from flask_restful import reqparse, abort, Api, Resource
from requests import put, get
import json

h_list = '192.168.2.200:2181'

app = Flask(__name__)
api = Api(app)

def abort_if_resource_doesnt_exist(resource_id):
    if resource_id not in resource:
        abort(404, message="Resource {} doesn't exist".format(resource_id))

def get_resource(zk):
    resource_dict = {}
    resource_list_unicode = zk.get_children("resources/") 
    resource_list = list(map(lambda x: str(x), resource_list_unicode))
    for i in resource_list:
        resource_node, stat = zk.get('/resources/%s' % i)
        resource_dict[i] = resource_node
    return resource_dict

def get_resource_matrix(zk):
    matrix, stat = zk.get('/usage_matrix') 
    return eval(matrix)

parser = reqparse.RequestParser()
parser.add_argument("idle")
parser.add_argument("id")
parser.add_argument("pss")
parser.add_argument("wks")
parser.add_argument("ip")
#parser.add_argument("gpus")
parser.add_argument("matrix")

# resource schedule
def schedule(ps_num, wk_num):
    resource_offered = []
    ps_offered = []
    wk_offered = []
    res_number = ps_num + wk_num

    # schedule resource according to matrix
    # round robin
    for i in gpu_range:
        for j in xrange(len(server_range)):
            if (matrix[j][i] == 1):
                resource_offered.append([resource[server_range[j]], i])
                matrix[j][i] = 0
                if len(resource_offered) >= res_number:
                    break
        if len(resource_offered) >= res_number:
            break
    print 'resource offered:'
    print resource_offered
    print 'matrix now:'
    print matrix
    #reduce(lambda x,y :x+y ,matrix)

#    if gpu_num > 4:
#        abort(404, message = "a single server has max 4 GPUs")
    if res_number > 16: 
        abort(404, message = "no enough resources") 

#    while (len(resource_offered) < server_num): 
#        i = resource.values()[j]
#        if type(i) is str: 
#            i = eval(i) 
#        if type(i) is dict: 
#            pass
#        if len(i["gpu_avail_list"]) > 1: 
#            resource_offered.append(i) 
#        j = j + 1
    
#    ps_offered = resource_offered[0:ps_num]
#    wk_offered = resource_offered[ps_num:]
    zk.set("/usage_matrix", json.dumps(matrix))
    return resource_offered

class Single_machine(Resource):
    def get(self, resource_id):
        abort_if_resource_doesnt_exist(resource_id)
        return resource[resource_id]    
    '''
    def put(self, resource_id):
        args = parser.parse_args()
        node = {
            "idle": args["idle"],
            "id": args["id"],
            "ip": args["ip"]
            }
        resource[int(resource_id[-1])] = node
        # update resource info in zookeeper
        #zk = KazooClient(hosts=h_list)
        #zk.start()
        zk.ensure_path("/resources/")
        if zk.exists("/resources/" + resource_id):
            zk.set("/resources/" + resource_id, json.dumps(node))
        else:
            zk.create("/resources/" + resource_id, json.dumps(node))
        return
    '''
class ResourceList(Resource):
    def get(self):
        args = parser.parse_args()
        pss = int(args["pss"])
        wks = int(args["wks"])
        #gs = int(args["gpus"])
        return schedule(pss, wks)

class ResourceMatrix(Resource):
    def get(self):
        return matrix
    
    def put(self):
        args = parser.parse_args()
        release_list = args["matrix"]
        release_list = eval(release_list)
        for i in release_list:
            print i
            matrix[server_range.index('node_'+eval(i[0])['eth0'])][i[1]] = 1
        zk.set("usage_matrix", json.dumps(matrix))
        print 'matrix now:'
        print matrix

api.add_resource(ResourceList, '/resources') 
api.add_resource(Single_machine, '/resources/<resource_id>')
api.add_resource(ResourceMatrix, '/matrix')

if __name__ == '__main__':
    
    zk = KazooClient(hosts=h_list)
    zk.start()
    resource = get_resource(zk)
    matrix = get_resource_matrix(zk)
    server_range = resource.keys()
    gpu_range = eval(resource.values()[0])['gpu_avail_list']
    print gpu_range
    print server_range
    #print matrix
    for i in resource:
        print resource[i]
#    print resource
#    schedule(1, 3)
    app.run(debug=True)

