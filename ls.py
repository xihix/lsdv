# Simulation code for Computer Networking
# The SDN-version implementation of Dijkstra's 
# Algorithm. Employs a global view for all the 
# switches in the network.

import time
import math
import networkx as nx # to simplify the algorithm..
import pox.lib.packet as pkt
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.revent import *
from pox.lib.addresses import EthAddr
# from collections import defaultdict
from pox.openflow.discovery import Discovery

log = core.getLogger()

# set of global variables
class G:
  lset = {} # store all links in the topology
  avail_switches = set() # set of all switches in the network
  hst2swtch = {} # store mapping of: host MAC => dpid (switch 
                 # that directly connects to the host)
  swtch2hst = {}
  routes = {} # all the uni-source shortest paths..
  HOST_PORT = 1
  delays_btwn_cands = {}
  _prev = None
  MONITOR_PERIOD = 5 # SECONDS
  mac2dpid = {}
  RECORD_PERIOD = 2
  start_times = {}
  delays = {}
  glob_view = nx.Graph()
  stable = False

def _handle_ConnectionUp (event):
  log.debug('connection up with ' + str(event.dpid))
  conn = event.connection
  G.mac2dpid[conn.eth_addr] = conn.dpid
  

# Handle link event.. To update new links..  
def _handle_LinkEvent(event):
  if event.removed: return
  # else it is 'added' event; i.e., when links are added to the link
  links = core.openflow_discovery.adjacency
  for l in links:
    lnk = (l[0], l[2])
    lnkr = (l[2], l[0])
    if str(lnk) not in G.lset and str(lnkr) not in G.lset:
      G.lset[str(lnk)] = (l[0], l[1], l[2], l[3])

def _handle_PacketIn(event):
  packet = event.parsed
  packet_in = event.ofp
  if not packet: return

  src = str(packet.src)
  dst = str(packet.dst)

  # If the packet is from host side..
  if packet_in.in_port == G.HOST_PORT:
    # Register the host to dpid mapping
    G.hst2swtch[src] = event.dpid
    G.swtch2hst[event.dpid] = src

  if packet.type == 0x5577:
    from_dpid = G.mac2dpid[packet.src]
    to_dpid   = G.mac2dpid[packet.dst]
    #log.info(packet_in)
    now = time.time()
    then = G.start_times[str((packet.src,packet.dst))]
    G.delays[str((from_dpid,to_dpid))] = 1 #math.log(10*1000*(now - then))
    #math.floor(math.log10(10*1000*(now - then)))
    # log.info(G.delays)
  # elif packet.type == packet.ARP_TYPE:
  else:
    if not G.stable: return
    # log.info('Enter.')
    if dst in G.hst2swtch: #and src in G.hst2swtch:
      dpid = event.dpid
      target_swtch = G.hst2swtch[dst]

      if target_swtch == dpid:
        # send to host..
        # log.info('Sent to host in next hop..')
        event.connection.send( of.ofp_flow_mod(
          action=of.ofp_action_output(port=G.HOST_PORT),
          match=of.ofp_match(dl_dst=packet.dst)
        ))
        # msg = of.ofp_packet_out()
        # msg.data = packet_in
        # msg.match = of.ofp_match( dl_dst=packet.dst )
        # action = of.ofp_action_output(port=G.HOST_PORT)
        # msg.actions.append(action)
        # event.connection.send(msg)
        return
      else:
        # Find the shortest path from current 
        # switch to target switch
        # returns the next-hop switch
        
        route = nx.dijkstra_path(G.glob_view, dpid, target_swtch)
        log.info('#'*20 + 'from %s to %s ' % (dpid, target_swtch) + str(route))
        next_dpid = route[1]

        l = str((next_dpid, event.dpid))
        lr = str((event.dpid, next_dpid))
        target_port = None
        if l in G.lset:
          target_port = G.lset[l][3]
        elif lr in G.lset:
          target_port = G.lset[lr][1]
        else: return

        event.connection.send( of.ofp_flow_mod(
          action=of.ofp_action_output(port=target_port),
          match=of.ofp_match(dl_dst=packet.dst)
        ))
        log.info('From %s to %s: next hop is: %s' % (event.dpid,\
          target_swtch, next_dpid))
        
        # msg = of.ofp_packet_out()
        # msg.data = packet_in
        # msg.match = of.ofp_match(dl_dst=packet.dst)
        # # msg.match = of.ofp_match(dl_dst=EthAddr(dst))
        # action = of.ofp_action_output(port=target_port)
        # log.info('From %s to %s: next hop is: %s' % (event.dpid,\
        #   target_swtch, next_dpid))
        # msg.actions.append(action)
        # event.connection.send(msg)

    else: # unknown dest.
      if dst == 'ff:ff:ff:ff:ff:ff':
        # timestamp = time.time()
        # log.info(str(timestamp) + 'From ARP_TYPE: ' + str(packet))
        # log.info(str(timestamp) + 'From ARP_TYPE:'  + str(packet_in))

        #######################################
        event.connection.send( of.ofp_flow_mod(
          action=of.ofp_action_output(port=of.OFPP_ALL),
          match=of.ofp_match(dl_dst=EthAddr('ff:ff:ff:ff:ff:ff'))
        ))
        # msg = of.ofp_packet_out()
        # msg.data = packet_in
        # action = of.ofp_action_output(port = of.OFPP_ALL)
        # msg.actions.append(action)
        # event.connection.send(msg)
        return  


# def _handle_PortStats(event):
#   log.info('>>>>from '+str(event.dpid) + ' stats:' + str(dir(event.stats[0])))
#   global delays_btwn_cands, sent_times
#   now = time.time()
#   delays_btwn_cands[event.dpid] = time.time() - sent_times[event.dpid]

def _measure_delay ():
  if len(core.openflow._connections) == 0: return True
  
  for l in G.lset:
    (l1, p1, l2, p2) = G.lset[l]
    s1 = core.openflow._connections[l1]
    s2 = core.openflow._connections[l2]
    e = pkt.ethernet()
    e.src = s1.eth_addr
    e.dst = s2.eth_addr
    e.type = 0x5577 # self-defined ..
    e.payload = 'for measurement.' 
    msg = of.ofp_packet_out()
    msg.data = e.pack()
    msg.actions.append(of.ofp_action_output(port=p1))
    core.openflow.getConnection(l1).send(msg) 
    G.start_times[str((e.src, e.dst))] = time.time()

  return False 
  
def _create_glob_view():
  for l in G.lset:
    (l1, p1, l2, p2) = G.lset[l]
    G.glob_view.add_edge(l1, l2, weight=G.delays[l])
  log.info('The graph:' + '>'*20)
  log.info(G.glob_view.edges(data=True))

def monit_topo():
  if G._prev is None: G._prev = G.lset
  else: 
    if len(G.lset) > 0 and \
    len(set(G._prev).difference(set(G.lset))) == 0 and \
    len(set(G.lset).difference(set(G._prev))) == 0:

      # Implies that the link set is stable in the last period
      # Calculate the Dijkstra's Algorithm..
      # Code here: use networkx library.
      if len(G.lset) == len(G.delays): 
        _create_glob_view()
        G.stable = True
      # Otherwise: there are ongoing measurement still for some
      # connetions.
      return False
    else: G._prev = G.lset
    return True


def launch():
  from pox.lib.recoco import Timer
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  # core.openflow.addListenerByName("PortStatsReceived", _handle_PortStats)
  Timer(G.MONITOR_PERIOD, monit_topo, recurring=True, \
    selfStoppable=True)
  Timer(G.MONITOR_PERIOD, _measure_delay, recurring=True, \
    selfStoppable=True)
  def init():  
    core.openflow_discovery.addListenerByName('LinkEvent', \
      _handle_LinkEvent)
    
  core.call_when_ready(init, "openflow_discovery")
