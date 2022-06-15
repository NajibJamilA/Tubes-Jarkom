#!/usr/bin/env python
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel
import time
import os

#NAJIB JAMIL ABDURRAHMAN - 1301204250

if '__main__' == __name__:
	os.system('mn -c')
	setLogLevel('info')
	net = Mininet(link=TCLink)
	key = "net.mptcp.mptcp_enabled"
	value = 0
	p = Popen("sysctl -w %s=%s" %(key,value), shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	print("stdout=",stdout,"stderr=",stderr)

	#Membuat Host
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')

	#Membuat Router
	r1 = net.addHost('r1')
	r2 = net.addHost('r2')
	r3 = net.addHost('r3')
	r4 = net.addHost('r4')

	#Set bandwith 1Mbps dan 500Kb
	bw1={'bw':1}
	bw2={'bw':0.5}

	#Membuat link 
	net.addLink(r1, h1, intfName1 = 'r1-eth0', intfName2 = 'h1-eth0', cls=TCLink, **bw1)
	net.addLink(r2, h1, intfName1 = 'r2-eth0', intfName2 = 'h1-eth1', cls=TCLink, **bw1)
	net.addLink(r3, h2, intfName1 = 'r3-eth0', intfName2 = 'h2-eth0', cls=TCLink, **bw1)
	net.addLink(r4, h2, intfName1 = 'r4-eth0', intfName2 = 'h2-eth1', cls=TCLink, **bw1)
	net.addLink(r1, r3, intfName1 = 'r1-eth2', intfName2 = 'r3-eth2', cls=TCLink, **bw2)
	net.addLink(r1, r4, intfName1 = 'r1-eth1', intfName2 = 'r4-eth1', cls=TCLink, **bw1)
	net.addLink(r2, r4, intfName1 = 'r2-eth2', intfName2 = 'r4-eth2', cls=TCLink, **bw1)
	net.addLink(r2, r3, intfName1 = 'r2-eth1', intfName2 = 'r3-eth1', cls=TCLink, **bw2)
	net.build()

	#Konfigurasi Host
	h1.cmd("ifconfig h1-eth0 0")
	h1.cmd("ifconfig h1-eth1 0")
	h2.cmd("ifconfig h2-eth0 0")
	h2.cmd("ifconfig h2-eht1 0")
	
	h1.cmd("ifconfig h1-eth0 192.168.10.2 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 192.168.11.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth0 192.168.16.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 192.168.17.2 netmask 255.255.255.0") 
	
	#Konfigurasi Router
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 2 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 3 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 4 > /proc/sys/net/ipv4/ip_forward")
	
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	
	#Set IP address
	r1.cmd("ifconfig r1-eth0 192.168.10.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.14.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.12.1 netmask 255.255.255.0")

	r2.cmd("ifconfig r2-eth0 192.168.11.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.15.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.13.1 netmask 255.255.255.0")

	r3.cmd("ifconfig r3-eth0 192.168.16.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.15.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.12.2 netmask 255.255.255.0")

	r4.cmd("ifconfig r4-eth0 192.168.17.1 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.14.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.13.2 netmask 255.255.255.0")
	
	#Routing Host
	h1.cmd("ip rule add from 192.168.10.2 table 1")
	h1.cmd("ip rule add from 192.168.11.2 table 2")
	h1.cmd("ip route add 192.168.10.0/24 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 192.168.10.1 dev h1-eth0 table 1")
	h1.cmd("ip route add 192.168.11.0/24 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 192.168.11.1 dev h1-eth1 table 2")
	h1.cmd("ip route add default scope global nexthop via 192.168.10.1 dev h1-eth0")
	h1.cmd("ip route add default scope global nexthop via 192.168.11.1 dev h1-eth1")
	
	h2.cmd("ip rule add from 192.168.16.2 table 1")
	h2.cmd("ip rule add from 192.168.17.2 table 2")
	h2.cmd("ip route add 192.168.16.0/24 dev h2-eth0 scope link table 1")
	h2.cmd("ip route add default via 192.168.16.1 dev h2-eth0 table 1")
	h2.cmd("ip route add 192.168.17.0/24 dev h2-eth1 scope link table 2")
	h2.cmd("ip route add default via 192.168.17.1 dev h2-eth1 table 2")
	h2.cmd("ip route add default scope global nexthop via 192.168.16.1 dev h2-eth0")
	h2.cmd("ip route add default scope global nexthop via 192.168.17.1 dev h2-eth1")
	
	#Routing Router
	r1.cmd("route add -net 192.168.13.0/24 gw 192.168.14.2")
	r1.cmd("route add -net 192.168.15.0/24 gw 192.168.12.2")
	r1.cmd("route add -net 192.168.16.0/24 gw 192.168.12.2")
	r1.cmd("route add -net 192.168.17.0/24 gw 192.168.14.2")
	r1.cmd("route add -net 192.168.11.0/24 gw 192.168.12.2")

	r2.cmd("route add -net 192.168.10.0/24 gw 192.168.15.2")
	r2.cmd("route add -net 192.168.12.0/24 gw 192.168.15.2")
	r2.cmd("route add -net 192.168.16.0/24 gw 192.168.15.2")
	r2.cmd("route add -net 192.168.17.0/24 gw 192.168.13.2")
	r2.cmd("route add -net 192.168.14.0/24 gw 192.168.13.2")

	r3.cmd("route add -net 192.168.10.0/24 gw 192.168.12.1")
	r3.cmd("route add -net 192.168.11.0/24 gw 192.168.15.1")
	r3.cmd("route add -net 192.168.13.0/24 gw 192.168.15.1")
	r3.cmd("route add -net 192.168.14.0/24 gw 192.168.12.1")
	r3.cmd("route add -net 192.168.17.0/24 gw 192.168.15.1")

	r4.cmd("route add -net 192.168.10.0/24 gw 192.168.14.1")
	r4.cmd("route add -net 192.168.11.0/24 gw 192.168.13.1")
	r4.cmd("route add -net 192.168.12.0/24 gw 192.168.14.1")
	r4.cmd("route add -net 192.168.15.0/24 gw 192.168.13.1")
	r4.cmd("route add -net 192.168.16.0/24 gw 192.168.14.1")
	
	r1.cmdPrint("tc qdisc del dev r1-eth0 root")
	r1.cmdPrint("tc qdisc add dev r1-eth0 root netem delay 100ms")
	time.sleep(2)
	
	#TCP
	h2.cmd("iperf -s &") 
	#h2.cmd("tcpdump -w test.pcap &") 
	h1.cmd("iperf -c 192.168.16.2 -t 20 &") 
	time.sleep(2)
	#h1.cmd("iperf -t 20 -c 192.168.16.2 &") 
	
	
	CLI(net)
	net.stop()
