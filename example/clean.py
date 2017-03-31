# cleans up the Kazoo client for testing convenience


from kazoo.client import KazooClient
zk = KazooClient(hosts='192.168.2.202:12181')
zk.start()
zk.delete("/tf/", recursive=True)
zk.stop()
