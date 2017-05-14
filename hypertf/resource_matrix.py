from kazoo.client import KazooClient 
import json
from resource_manager import get_resource

def build_matrix(resource):
    print resource
    # server index 
    server_range = resource.keys()
    # gpu index
    #gpu_range = eval(resource.values()[0])['gpu_avail_list']
    gpu_range = xrange(eval(resource.values()[0])['gpu']) 

    # matrix is a two-dimensional array, x for server, y for gpu
    matrix = [[0 for x in server_range] for y in gpu_range]
    for i in xrange(len(server_range)):
        for j in eval(resource.values()[i])['gpu_avail_list']:    
            print 'set ' + server_range[i] + ' gpu ' + str(j) + ' to 1'
            matrix[server_range.index(server_range[i])][j] = 1
 
    return matrix

def print_matrix(matrix):
    for i in matrix:
        for j in i:
            print j,
        print 

def get_node_usage(host, gpu_index, Matrix):
    return Matrix[server_range.index(host)][gpu_index]

def save_matrix(matrix, name):
    if zk.exists(name): 
        zk.set(name, json.dumps(matrix)) 
    else: 
        zk.create(name, json.dumps(matrix))

def print_node_usage(host, gpu_index, Matrix):
    if get_node_usage(host, gpu_index, Matrix) == 1:
        ans = True
    else: 
        ans = False

    print 'Is {} GPU No.{} idle? {}'.format(host, gpu_index, ans)

if __name__ == '__main__':

    zk = KazooClient(hosts='192.168.2.200:2181') 
    zk.start() 
    resource = get_resource(zk)
    server_range = resource.keys()
    node_name = "usage_matrix"
    matrix = build_matrix(resource)    
    save_matrix(matrix, node_name)

    # test
    print_node_usage('node_192.168.2.202', 2, matrix)
    print_node_usage('node_192.168.2.200', 3, matrix)

    print 'node order: '
    for i in server_range:
        print i,
    print

    print_matrix(matrix)

