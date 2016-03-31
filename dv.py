import time
import networkx # to simplify the algorithm..
import pox.lib.packet as pkt
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.revent import *
from pox.lib.addresses import EthAddr
import sys
from pox.openflow.discovery import Discovery

log = core.getLogger()
HOST_PORT = 1
lset = {}
sset = {}
hst2swtch = {}
swtch2hst = {}
switches = {}
mac2switches = {}

def _handle_LinkEvent(event):
  if event.removed: return
  # else it is 'added' event; i.e., when links are added to the link
  
  links = core.openflow_discovery.adjacency
  for l in links:
    lnk = (l[0], l[2])
    lnkr = (l[2], l[0])
    if str(lnk) not in lset and str(lnkr) not in lset:
      lset[str(lnk)] = (l[0], l[1], l[2], l[3])

  for dpid in switches:
    switches[dpid].updateNeighbors(lset.copy())

def _flood():
  for dpid in switches:
    switches[dpid].flood_to_neighbors()


class Switch(object):
  def __init__(self, conn):
    self.conn = conn
    self.dpid = conn.dpid
    self.neighbors = {}
    self.dvs = {}

  def updateNeighbors(self, lset):
    for l in lset.values():
      (l1, p1, l2, p2) = l
      if self.dpid == l1:
        self.neighbors[l2] = p1 # port to the neighbor
        self.dvs[l2] = (l2, 1) # (next-hop, default-cost) ..
      elif self.dpid == l2:
        self.neighbors[l1] = p2 # port to the neighbor
        self.dvs[l1] = (l1, 1) # (next-hop, default-cost) ..
      else:
        if l1 not in self.dvs: self.dvs[l1] = (l1, sys.maxint/100) # maxint/100 is Inf.
        if l2 not in self.dvs: self.dvs[l2] = (l2, sys.maxint/100)

  def flood_to_neighbors(self):
    log.info('::Flooding..')
    log.info('neighbors of %s: %s' % (self.dpid, self.neighbors))
    for dpid in self.neighbors:
      switches[dpid].feed(self.dpid, self.dvs.copy())

  def feed(self, frm, dvs):
    NEXT_HOP = 0
    COST = 1
    log.info('dvs:' + str(dvs))
    log.info('dvs-self:' + str(self.dvs))
    # implementation of Bellman-Ford algorithm..
    for other in self.dvs:
      if other != frm:
        if self.dvs[other][COST] > dvs[other][COST] + self.dvs[frm][COST]:
          self.dvs[other] = (frm, dvs[other][COST] + self.dvs[frm][COST])
      

  def goTo(self,target):
    return self.dvs[target][0]


def launch():
  from pox.lib.recoco import Timer
  def _handle_ConnectionUp(event):
    mac2switches[event.connection.eth_addr] = event.dpid
    switches[event.dpid] = Switch(event.connection)

  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  Timer(5, _flood, recurring=True)
  def init():  
    core.openflow_discovery.addListenerByName('LinkEvent', _handle_LinkEvent)
  core.call_when_ready(init, "openflow_discovery")


def _handle_PacketIn(event):
  packet = event.parsed
  packet_in = event.ofp
  if not packet: return
  
  src = str(packet.src)
  dst = str(packet.dst)

  # If the packet is from host side..
  if packet_in.in_port == HOST_PORT:
    # Register the host to dpid mapping
    hst2swtch[src] = event.dpid
    swtch2hst[event.dpid] = src
    # log.info('Record from %s' % event.dpid)

  if dst in hst2swtch:
    target_swtch = hst2swtch[dst]

    if target_swtch == event.dpid:
      event.connection.send( of.ofp_flow_mod(
          action=of.ofp_action_output(port=HOST_PORT),
          match=of.ofp_match(dl_dst=packet.dst)
        ))
      # log.info('from %s to %s' % (event.dpid, str(dst)))
      return
    # Otherwise the packet is sent for next hop
    # Find the shortest path from current 
    # switch to target switch
    # returns the next-hop switch
    next_dpid = switches[event.dpid].goTo(target_swtch)
    log.info('from %s to %s' % (event.dpid, next_dpid))


    # l = str((next_dpid, event.dpid))
    # lr = str((event.dpid, next_dpid))
    # target_port = None
    # if l in lset:
    #   (l1, p1, l2, p2) = lset[l]
    #   target_port = lset[l][3]
    # elif lr in lset:
    #   target = lset[l][1]
    # else: return

    # event.connection.send( of.ofp_flow_mod(
    #       action=of.ofp_action_output(port=target_port),
    #       match=of.ofp_match(dl_dst=packet.dst)
    #     ))
  else:
    if dst == 'ff:ff:ff:ff:ff:ff':
      # timestamp = time.time()
      # log.info(str(timestamp) + 'From ARP_TYPE: ' + str(packet))
      # log.info(str(timestamp) + 'From ARP_TYPE:'  + str(packet_in))

      #######################################
      event.connection.send( of.ofp_flow_mod(
        action=of.ofp_action_output(port=of.OFPP_ALL),
        match=of.ofp_match(dl_dst=EthAddr('ff:ff:ff:ff:ff:ff'))
      ))




