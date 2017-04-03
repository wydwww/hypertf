#!flask/bin/python

# resource manager, it's a server connecting to cluster runner clients and resource query clients on physical servers,
# and a client connecting to zookeeper server

from flask import Flask, jsonify, abort, request, make_response, url_for
from kazoo.client import KazooClient
from flask_restful import reqparse, abort, Api, Resource
from requests import put, get
import json

# h_list = '192.168.2.202:12181'

# test on local
# TODO
h_list = '127.0.0.1:2181'

app = Flask(__name__)
api = Api(app)

def abort_if_resource_doesnt_exist(resource_id):
    if resource_id not in resource:
        abort(404, message="Resource {} doesn't exist".format(resource_id))

def get_resources_from_kz(zk):
    ps_list = zk.get_children('/resources/')
    # wk_list = zk.get_children('/tf/masters/masters1/wk_node/')
    resources_from_kz = []
    j = 1
    for i in ps_list:
        ps_node = {
            "idle": 1,
            "id": j,
            "title": i
            }
        j += 1
        resources_from_kz.append(ps_node)

    # j = 1
    # for i in wk_list:
    #     wk_node = {
    #         "idle": true,
    #         "id": j,
    #         "title": i
    #         }
    #     j += 1
    #     resources_from_kz.append(wk_node)
    return resources_from_kz

parser = reqparse.RequestParser()
parser.add_argument("idle")
parser.add_argument("id")
parser.add_argument("pss")
parser.add_argument("wks")

class Single_machine(Resource):
    def get(self, resource_id):
        abort_if_resource_doesnt_exist(resource_id)
        return resource[resource_id]    
    
    def put(self, resource_id):
        args = parser.parse_args()
        node = {
            "idle": args["idle"],
            "id": args["id"], # TODO: add id argument
            "title": resource_id
            }
        resource[int(resource_id[4])] = node # TODO: id
        # update resource info in zookeeper
        zk = KazooClient(hosts=h_list)
        zk.start()
        zk.ensure_path("/resources/")
        if zk.exists("/resources/" + resource_id):
            zk.set("/resources/" + resource_id, json.dumps(node))
        else:
            zk.create("/resources/" + resource_id, json.dumps(node))
        return

class ResourceList(Resource):
    def get(self):
        args = parser.parse_args()
        resources_idle = []
        j = 0
        while (len(resources_idle) < int(args["pss"])):
            i = resource[j]
            if i["idle"] == 1:
                resources_idle.append(i)
                # put(self.rm_addr + "/resources/node1", data = {"idle": 0})
            j = j + 1
        return resources_idle
        # return resource

api.add_resource(ResourceList, '/resources') 
api.add_resource(Single_machine, '/resources/<resource_id>')

if __name__ == '__main__':
    
    zk = KazooClient(hosts=h_list)
    zk.start()
    resource = get_resources_from_kz(zk)
#    print resource
    app.run(debug=True)
