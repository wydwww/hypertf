import netifaces as ni
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE

network_interface = ni.interfaces()

eth0 = ni.ifaddresses('eth0')[AF_INET][0]['addr']
eth2 = ni.ifaddresses('eth2')[AF_INET][0]['addr']
eth2.199 = ni.ifaddresses('eth2.199')[AF_INET][0]['addr']
eth3 = ni.ifaddresses('eth3')[AF_INET][0]['addr']
eth3.198 = ni.ifaddresses('eth3.198')[AF_INET][0]['addr']

