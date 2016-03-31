from mininet.topo import Topo
from mininet.link import TCLink
import struct

def dpidToStr (dpid, alwaysLong = False):
  """
  Convert a DPID from a long into into the canonical string form.
  """
  if type(dpid) is long or type(dpid) is int:
    # Not sure if this is right
    dpid = struct.pack('!Q', dpid)

  assert len(dpid) == 8

  r = '-'.join(['%02x' % (ord(x),) for x in dpid[2:]])

  if alwaysLong or dpid[0:2] != (b'\x00'*2):
    r += '|' + str(struct.unpack('!H', dpid[0:2])[0])

  return r


class MyTopo( Topo ):
    def lnk(self, stationA, stationB, delay):
   		if str((stationA,stationB)) not in self.connections and \
   		str((stationB, stationA)) not in self.connections:
   			s1 = 's%s' % self.tables[stationA]
   			s2 = 's%s' % self.tables[stationB]
   			self.addLink(s1, s2, delay='%sms' % (10*delay), jitter=0)
   			self.connections.append(str((stationA, stationB)))

    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )

        self.stations = []
        self.tables = {}
        self.connections = []

        # self.addStation('NanJingXiLu')
        # self.addStation('RenMinGuangChang')
        # self.addStation('NanJingDongLu')
        # self.addStation('ShanXiNanLu')
        # self.addStation('JiaShanLu')
        # self.addStation('DaPuQiao')
        # self.addStation('MaDangLu')
        # self.addStation('LuJiaBangLu')
        # self.addStation('LaoXiMen')
        # self.addStation('DaShiJie')
        # self.addStation('YuYuan')
        # self.addStation('HuangPiNanLu')
        # self.addStation('XinTianDi')
        # self.addStation('HuaiHaiZhongLu')


        # self.lnk('NanJingXiLu', 'RenMinGuangChang', 3)
        # self.lnk('RenMinGuangChang', 'NanJingDongLu', 2)
        # self.lnk('NanJingXiLu', 'ShanXiNanLu', 3)
        # self.lnk('ShanXiNanLu', 'JiaShanLu', 3)
        # self.lnk('JiaShanLu', 'DaPuQiao', 1)
        # self.lnk('DaPuQiao', 'MaDangLu', 2)
        # self.lnk('MaDangLu', 'LuJiaBangLu', 1)
        # self.lnk('LuJiaBangLu', 'LaoXiMen', 2)
        # self.lnk('LaoXiMen', 'DaShiJie', 2)
        # self.lnk('DaShiJie', 'RenMinGuangChang', 2)
        # self.lnk('NanJingXiLu', 'HuaiHaiZhongLu', 2)
        # self.lnk('ShanXiNanLu', 'HuangPiNanLu', 2)
        # self.lnk('RenMinGuangChang', 'HuangPiNanLu', 3)
        # self.lnk('HuaiHaiZhongLu', 'XinTianDi', 3)
        # self.lnk('YuYuan', 'LaoXiMen', 3)
        # self.lnk('YuYuan', 'NanJingDongLu', 2)
        # self.lnk('MaDangLu', 'XinTianDi', 2)
        # self.lnk('XinTianDi', 'ShanXiNanLu', 3)
        # self.lnk('XinTianDi', 'LaoXiMen', 2)
        


        lin1 = [
        	'XinZhuang',
        	'WaiHuanLu',
        	'JinJiangLeYuan',
        	'ShangHaiNanZhan',
        	'CaoBaoLu',
        	'ShangHaiTiYuGuan',
        	'XuJiaHui',
        	'HengShanLu',
        	'ChangShuLu',
        	'ShanXiNanLu',
        	'HuangPiNanLu',
        	'RenMinGuangChang',
        	'XinZhaLu',
        	'HanZhongLu',
        	'ShangHaiHuoCheZhan',
        	'ZhongShanBeiLu',
        	'YanChangLu',
        	'ShangHaiMaXiCheng',
        	'WenShuiLu',
        	'PengPuXinChun',
        	'GongKangLu',
        	'TongHeXinChun',
        	'HuLanLu',
        	'GongFuXinChun',
        	'BaoAnGongLu',
        	'YouYiXiLu',
        	'FuJinLu']
        delays = [3, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 3, 2, 2,
        	3, 2, 3, 2, 2, 3, 3, 2, 2, 3, 2, 3]

        for stat in lin1:
        	self.addStation(stat)

        for i in xrange(len(lin1)-1):
        	self.lnk(lin1[i], lin1[i+1], delays[i])

        lin2 = [
        	('XuJingDong',4),
        	('HongQiaoHuoCheZhan',2),
        	('HongQiaoErHaoHangZhanLou',7),
        	('SongHongLu',2),
        	('BeiXinJing',2),
        	('WeiNingLu',3),
        	('LouShanGuanLu',3),
        	('ZhongShanGongYuan',2),
        	('JiangSuLu',3),
        	('JingAnSi',2),
        	('NanJingXiLu',3),
        	('RenMinGuangChang',2),
        	('NanJingDongLu',3),
        	('LuJiaZui',2),
        	('DongChangLu',2),
        	('ShiJiDadao',3),
        	('ShangHaiKeJiGuan',2),
        	('ShiJiGongYuan',2),
        	('LongYangLu',4),
        	('ZhangJiangGaoKe',3),
        	('JinKeLu',3),
        	('GuangLanLu',5),
        	('TangZhen',4),
        	('ChuangXinZhongLu',3),
        	('HuaXiaDongLu',4),
        	('ChuanSha',4),
        	('LingKongLu',5),
        	('YuanDongDaDao',7),
        	('HaiTianSanLu',3),
        	('PuDongGuoJiJiChang',0)
        ]
        for i in xrange(len(lin2)):
        	self.addStation(lin2[i][0])

        for i in xrange(len(lin2)-1):
        	self.lnk(lin2[i][0], lin2[i+1][0], lin2[i][1])

        lin3 = [
        	('ShanHaiNanZhan',3),
        	('ShiLongLu',3),
        	('LongCaoLu',2),
        	('YiShanLu',2),
        	('HongQiaoLu',3),
        	('YanAnXiLu',2),
        	('ZhongShanGongYuan',2),
        	('JinShaJiangLu',2),
        	('CaoYangLu',3),
        	('ZhenPingLu',2),
        	('ZhongTanLu',3),
        	('ShangHaiHuoCheZhan',3),
        	('BaoShanLu',2),
        	('DongBaoXingLu',3),
        	('HongKouZuQiuChang',2),
        	('ChiFengLu',2),
        	('DaBaiShu',3),
        	('JiangWanZhen',2),
        	('YinGaoXiLu',3),
        	('ChangJiangNanLu',2),
        	('SongFaLu',3),
        	('ZhangHuaBang',2),
        	('SongBinLu',2),
        	('ShuiChanLu',3),
        	('BaoYangLu',2),
        	('YouYiLu',2),
        	('TieLiLu',4),
        	('JiangYangBeiLu',0)
        ]

        for i in xrange(len(lin3)):
        	self.addStation(lin3[i][0])

        for i in xrange(len(lin3)-1):
        	self.lnk(lin3[i][0], lin3[i+1][0], lin3[i][1])

        lin4 = [
        	('ShangHaiTiYuGuan', 3),
        	('YiShanLu', 3),
        	('HongQiaoLu', 2),
        	('YanAnXiLu', 2),
        	('ZhongShanGongYuan', 3),
        	('JinShaJiangLu', 2),
        	('CaoYangLu', 2),
        	('ZhenPingLu', 2),
        	('ZhongTanLu', 3),
        	('ShangHaiHuoCheZhan', 4),
        	('BaoShanLu', 2),
        	('HaiLunLu', 2),
        	('LinPingLu', 3),
        	('DaLianLu', 1),
        	('YangShuPuLu',3),
        	('PuDongDaDao',2),
        	('ShiJiDadao', 2),
        	('PuDianLu',2),
        	('LanChunLu',2),
        	('TangQiao',3),
        	('NanPuDaQiao',2),
        	('XiZangNanLu',3),
        	('LuBanLu',2),
        	('DaMuQiaoLu',2),
        	('DongAnLu',3),
        	('ShanghaiTiYuChang',2),
        	('ShangHaiTiYuGuan',0)
        ]


        for i in xrange(len(lin4)):
        	self.addStation(lin4[i][0])

        for i in xrange(len(lin4)-1):
        	self.lnk(lin4[i][0], lin4[i+1][0], lin4[i][1])

        lin5 = [
        	('XinZhuang',3),
        	('ChunShenLu',2),
        	('YinDuLu',4),
        	('XuQiao',3),
        	('BeiQiao',3),
        	('JianChuanLu',2),
        	('DongChuanLu',3),
        	('JinPingLu',2),
        	('HuaNingLu',3),
        	('WenJingLu',3),
        	('MinHangKaiFaQu',0)
        ]


        for i in xrange(len(lin5)):
        	self.addStation(lin5[i][0])

        for i in xrange(len(lin5)-1):
        	self.lnk(lin5[i][0], lin5[i+1][0], lin5[i][1])


        lin6 = [
        	('DongFangTiYuZhongXin',3),
        	('LingYanNanLu',2),
        	('ShangNanLu',2),
        	('HuaXiaXiLu',3),
        	('GaoQingLu',2),
        	('DongMingLu',3),
        	('GaoKeXiLu',2),
        	('LinYiXinChun',3),
        	('ShangHaiErTongYiXueZhongXin',1),
        	('LanChunLu',3),
        	('PuDianLu',3),
        	('ShiJiDadao',2),
        	('YuanShenTiYuZhongXin',2),
        	('MinShengLu',2),
        	('BeiYangTingLu',3),
        	('DePingLu',2),
        	('YunShanLu',2),
        	('JinQiaoLu',3),
        	('BoXingLu',2),
        	('WuLianLu',2),
        	('JuFengLu',3),
        	('DongJingLu',2),
        	('WuZhouDaDao',2),
        	('ZhouHaiLu',3),
        	('WaiGaoQiaoBaoShuiQuNanZhan',3),
        	('HangJinLu',2),
        	('WaiGaoQiaoBaoShuiQuBeiZhan',4),
        	('GangChengLu',0)
        ]

        for i in xrange(len(lin6)):
        	self.addStation(lin6[i][0])

        for i in xrange(len(lin6)-1):
        	self.lnk(lin6[i][0], lin6[i+1][0], lin6[i][1])


        lin7 = [
        	('MeiLanHu',3),
        	('LuoNanXinChun',4),
        	('PanGuangLu',2),
        	('LiuHang',3),
        	('GuChunGongYuan',3),
        	('QiHuaLu',3),
        	('ShangHaiDaXue',2),
        	('NanChenLu',3),
        	('ShangDaLu',2),
        	('ChangZhongLu',2),
        	('DaChangLu',2),
        	('XingZhiLu',3),
        	('DaHuaSanLu',2),
        	('XinChunLu',2),
        	('LangGaoLu',3),
        	('ZhenPingLu',3),
        	('ChangShouLu',2),
        	('ChangPingLu',2),
        	('JingAnSi',3),
        	('ChangShuLu',2),
        	('ZhaoJiaBangLu',3),
        	('DongAnLu',2),
        	('LongHuaZhongLu',3),
        	('HouTan',3),
        	('ChangQingLu',2),
        	('YaoHuaLu',1),
        	('YunTaiLu',3),
        	('GaoKeXiLu',2),
        	('YangGaoNanLu',3),
        	('JinXiuLu',2),
        	('FangHuaLu',4),
        	('LongYangLu',3),
        	('HuaMuLu',0)
        ]

        for i in xrange(len(lin7)):
        	self.addStation(lin7[i][0])

        for i in xrange(len(lin7)-1):
        	self.lnk(lin7[i][0], lin7[i+1][0], lin7[i][1])


        lin8 = [
        	('ShenSheGongLu',3),
        	('LianHangLu',2),
        	('JiangYueLu',2),
        	('PuJiangLu',3),
        	('LuHengLu',4),
        	('LingZhaoXinChun',3),
        	('DongFangTiYuZhongXin',2),
        	('YangSi',2),
        	('ChengShanLu',2),
        	('YaoHuaLu',2),
        	('ZhongHuaYiShuGong',3),
        	('XiZangNanLu',2),
        	('LuJiaBangLu',2),
        	('LaoXiMen',2),
        	('DaShiJie',2),
        	('RenMinGuangChang',2),
        	('QuFuLu',2),
        	('ZhongXingLu',2),
        	('XiZangBeiLu',2),
        	('HongKouZuQiuChang',3),
        	('QuYangLu',2),
        	('SiPingLu',2),
        	('AnShanXinChun',2),
        	('JiangPuLu',2),
        	('HuangXingLu',2),
        	('YanJiZhongLu',2),
        	('YinXiangLu',2),
        	('NenJiangLu',2),
        	('ShiGuangLu',2)
        ]

        for i in xrange(len(lin8)):
        	self.addStation(lin8[i][0])

        for i in xrange(len(lin8)-1):
        	self.lnk(lin8[i][0], lin8[i+1][0], lin8[i][1])


        lin9 = [
        	('SongJiangNanZhan',3),
        	('ZuiBaiChi',2),
        	('SongJiangTiYuZhongXin',2),
        	('SongJiangXinCheng',3),
        	('SongJiangDaXueCheng',4),
        	('DongTing',3),
        	('SheShan',4),
        	('SiTing',6),
        	('JiuTing',3),
        	('ZhongChunLu',2),
        	('QiBao',2),
        	('XingZhongLu',3),
        	('HeChuangLu',1),
        	('CaoHeTingKaiFaQu',3),
        	('GuiLinLu',2),
        	('YiShanLu',2),
        	('XuJiaHui',2),
        	('ZhaoJiaBangLu',2),
        	('JiaShanLu',1),
        	('DaPuQiao',2),
        	('MaDangLu',1),
        	('LuJiaBangLu',2),
        	('XiaoNanMen',3),
        	('ShangChengLu',2),
        	('ShiJiDadao',3),
        	('YangGaoZhongLu',0)
        ]

        for i in xrange(len(lin9)):
        	self.addStation(lin9[i][0])

        for i in xrange(len(lin9)-1):
        	self.lnk(lin9[i][0], lin9[i+1][0], lin9[i][1])


        lin10 = [
        	('HangZhongLu',4),
        	('ZiTengLu',2),
        	('LongBaiXinChun',4),
        	('LongXiLu',3),
        	('ShuiChengLu',2),
        	('YiLiLu',2),
        	('SongYuanLu',3),
        	('HonhQiaoLu',2),
        	('JiangTongDaXue',2),
        	('ShangHaiTuShuGuan',3),
        	('ShanXiNanLu',3),
        	('XinTianDi',2),
        	('LaoXiMen',3),
        	('YuYuan',2),
        	('NanJingDongLu',2),
        	('TianTongLu',3),
        	('SiChuanBeiLu',2),
        	('HaiLunLu',2),
        	('YouDianXinChun',3),
        	('SiPingLu',2),
        	('TongJiDaXue',2),
        	('GuoQuanLu',2),
        	('WuJiaoChang',2),
        	('JiangWanTiYuChang',2),
        	('SanMenLu',2),
        	('YinGaoDongLu',2),
        	('XinJiangWanCheng',0)
        ]

        for i in xrange(len(lin10)):
        	self.addStation(lin10[i][0])

        for i in xrange(len(lin10)-1):
        	self.lnk(lin10[i][0], lin10[i+1][0], lin10[i][1])


        Add hosts and switches
        #IP='10.0.0.%s/23' % i,\
        h = [ self.addHost('h%s' % (i+1), \
        		MAC=dpidToStr(i+1)) for i in xrange(4)]

        s = [ self.addSwitch('s%s' % (i+1)) for i in xrange(4)]
        
        h1 = self.addHost( 'h1', IP='10.0.0.1/23' )
        h2 = self.addHost( 'h2', IP='10.0.0.2/23' )
        h3 = self.addHost( 'h3', IP='10.0.0.3/23' )
        # h4 = self.addHost( 'h4', IP='10.0.0.4/23' )        
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')	

        # Add links
        self.addLink( h1, s1 )
        self.addLink( h2, s2 )
        self.addLink( h3, s3 )
        # self.addLink( h4, s4 )
        l = [ self.addLink(h[k], s[k]) for k in xrange(4)]
        # interconnect for switches 
        pre_config_delays = {
        	'(1, 2)': '2ms',
        	'(1, 3)': '3ms',
        	'(1, 4)': '1ms',
        	'(2, 3)': '2ms',
        	'(2, 4)': '2ms',
        	'(3, 4)': '3ms',
        }

        for i in xrange(len(s)-1):
        	for j in xrange(i+1, len(s)):
        		pair = str((i+1, j+1))
        		l.append(self.addLink(s[i], s[j], max_queue_size=300, \
        			delay=pre_config_delays[pair], jitter=0))
        for i in xrange(len(self.stations)):
        	print('[%s] %s' % (i+1, self.stations[i]))


    def addStation(self, stationName):
    	if stationName not in self.stations:
    		no = len(self.stations) + 1
    		self.tables[stationName] = no
    		s = self.addSwitch('s%s' % no)
        	h = self.addHost('h%s' % no)
        	self.addLink(s, h)
        	self.stations.append(stationName)


topos = { 'mytopo': ( lambda: MyTopo() ) }