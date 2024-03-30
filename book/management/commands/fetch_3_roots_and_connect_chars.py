from django.core.management.base import BaseCommand
import requests
from book.models import Word, Root, RootChar

class Command(BaseCommand):
    help = 'Kelimelerin ve kök bilgilerinin çekilmesi ve veritabanına kaydedilmesi'

    def handle(self, *args, **options):
        roots = {'Alt', 'nw$', '$rk', 'msd', 'drhm', 'HSHS', 'stt', 'HrS', 'Anv', 'fqd', 'zxrf', 'Ahl', 'ntq', 'gsq', 'jwE', 'jAr', 'Enb', 'TlE', 'zjr', 'whb', '$Hn', 'pnb', 'srd', 'Hrs', 'rkn', 'krb', 'kEb', 'zbd', 'Aty', 'why', 'Hrd', 'EDw', 'ZmA', 'yqn', 'bqy', 'sdy', 'qdm', 'vlv', 'bqr', '$yx', 'HSr', 'rjj', 'qSd', 'Eyy', 'qbs', 'jrd', 'rgb', 'lpp', 'lHn', 'nxl', 'mwl', 'qml', 'dkk', 'qhr', 'zyg', 'wrd', 'wkd', 'xtm', 'xbw', 'rmn', 'sjl', 'jpp', 'tbE', 'nqr', 'jzA', 'Erm', 'smr', 'dhy', 'Afq', 'Hfr', 'nSy', '$An', 'nqS', 'qfw', 'slsl', 'Amr', 'kft', 'Hyv', 'xwD', 'byD', 'gzl', 'xyr', 'Ey$', 'Syr', 'tll', 'jmE', 'jzE', 'vmn', 'fDD', 'nvr', 'prA', 'hdhd', 'mrr', 'Hsd', 'DbH', 'Ekf', 'xrdl', 'xsr', 'xbl', 'Apy', 'lEb', 'HfZ', 'vrb', 'Hnv', 'qdH', 'HrD', 'lbn', 'xSS', 'jwr', 'lqb', 'Abw', 'bxE', 'lbb', 'gwy', 'rEy', 'sdr', 'frE', 'rdA', 'pwd', 'jrr', 'Tbq', 'mtn', 'kwd', 'Erw', 'Dmr', 'SyS', '$wy', 'Sdr', 'kfr', 'qlE', 'wtd', 'Tfq', 'tyn', 'wrv', 'xlw', 'Hlf', 'nmm', 'tsE', 'zhr', 'Sxx', 'dfA', 'mjs', 'lms', 'qlm', 'wjs', 'ndw', 'Asf', 'Ezm', 'qyD', '$Am', 'Evw', 'knd', 'nHb', 'mkr', 'lsn', 'lqm', 'hbw', 'bpr', 'frr', 'Hqq', 'nzf', 'qSr', 'Ewj', 'q$Er', 'qnE', 'ftH', 'Apn', 'dwm', 'xrj', 'zhd', 'sxr', 'krh', 'jbh', 'wEZ', 'lft', 'ZEn', '$hb', 'mtE', 'Ebqr', 'sjd', 'xdd', 'qyl', 'bxl', 'rjz', 'fny', 'swd', 'srf', 'rwg', 'hwr', 'jbn', 'fAd', 'fwt', 'Hyq', 'dnw', 'Sff', 'snn', 'xyb', 'qrD', 'dsw', 'wfd', 'lyl', 'srH', 'wfD', 'dry', 'frg', 'wqt', 'n$T', 'dhq', 'drA', 'shr', 'xft', 'kwn', 'vql', 'nfq', 'ksf', 'Ady', 'mlA', 'SHf', 'Sbb', 'flq', 'wsm', 'hrE', 'Emy', 'phb', 'hbT', 'jnn', 'n$r', 'wsT', 'lbd', 'HSn', '$El', 'kwr', 'wny', 'H$r', 'HbT', 'nwA', 'Swt', 'ESb', '$qw', 'Sxr', 'jpE', 'lqT', 'Etb', 'glq', 'swm', 'gyv', 'hym', 'Tmm', 'hrb', 'Abd', 'phl', 'frD', 'sbt', 'Avm', 'frq', 'ftr', 'hyl', 'wsws', 'byd', 'gwv', 'kll', 'dbb', 'rHq', 'xwr', 'prw', 'qrb', 'zwr', 'Axr', 'Hpr', 'mrH', '$rr', 'vmr', 'nHl', 'nwb', 'fjj', 'bhm', 'xmr', 'sHl', 'xbz', 'wDn', 'flH', 'bkm', 'nfd', 'bdn', '$HH', 'Eml', 'Hwy', 'srE', 'DHw', 'wqy', 'sbg', 'SEq', 'wtr', 'Hmd', 'sbl', 'bT$', '$hq', '$hd', 'mHn', 'vwy', 'smk', 'fyA', 'wTr', 'TfA', 'qTf', 'rjw', 'hzl', 'Hnn', 'Tlb', 'Ebs', 'qwy', 'HmA', 'SbH', 'Thr', 'gsl', 'vqf', 'jfn', 'Hdd', 'gyb', 'hms', 'bwr', 'TmE', 'Eqb', 'qmS', 'rqm', 'Evr', 'Emq', 'Sdq', 'jhr', 'rDw', 'zlq', 'x$E', 'nTq', 'lwm', 'Hrk', 'lZy', 'lEn', 'wdd', 'trq', 'fDl', 'nfl', 'brA', 'mTw', 'hTE', 'lff', 'kyn', 'Swb', 'shm', 'shw', 'kdH', 'x$b', '$mx', 'sTr', 'hlE', 'mSr', 'TEn', 'SmE', 'syl', 'Tms', 'ASr', '$hw', 'Trf', 'nDd', 'Esr', 'lTf', 'jld', 'pwq', 'dAb', 'frH', 'Hmm', 'lgb', 'qds', 'fSH', 'xTb', 'fDH', 'mry', 'dss', 'nfr', '$tt', 'nSH', 'tlw', 'Sly', 'jfw', 'nml', 'Hrv', 'Sfn', 'Elq', 'Alw', 'mHl', 'mwh', 'wdE', 'zbn', '$wr', 'wqr', 'lyn', 'rss', 'qTmr', 'qnT', 'fwz', 'nDr', 'kbkb', 'jrm', 'gSS', 'hmd', 'jHm', 'sjw', 'mqt', 'fEl', 'bss', 'nyl', 'gbr', 'lzb', 'Dyz', 'kAs', 'THw', 'Hml', 'Hnp', 'jnH', 'kbt', 'qsw', 'qDy', 'bqE', 'tjr', 'njd', 'dxl', 'gwr', 'dmr', 'pAb', 'mDy', 'xnzr', 'mrA', 'swA', 'rjm', 'smw', 'wsE', 'bkr', 'EDd', 'srbl', 'vry', 'Ehd', 'Ezz', 'sAm', 'xsA', 'Znn', 'ErD', 'Ery', 'jny', 'Etw', 'mlq', 'swy', 'bsq', 'wSd', '$yb', 'nHs', 'DfdE', 'TwE', 'Dyq', 'smd', 'ftn', 'qSS', 'mnE', 'lfZ', 'rhw', 'Etl', 'nEm', 'SbA', 'kdr', 'Hss', 'bny', 'bEvr', 'sbb', 'pbH', 'sHt', 'xTw', 'mzq', 'whj', 'mnn', 'rHb', 'bEl', 'wvq', 'bdA', 'nfx', 'lHy', 'smm', 'xTT', 'x$y', 'Hsb', 'tbr', 'HZr', 'nHt', 'snm', 'grf', 'kfA', 'Aml', 'DrE', 'Hbk', 'xTA', 'Twy', 'Trq', 'bTn', 'SlH', 'qEd', 'jlw', 'fhm', 'gTw', 'lgw', 'ksw', 'npr', '$wb', 'ryn', 'xyl', 'wpr', 'rkm', 'zqm', '$rH', 'rdm', 'Aby', 'dvr', 'kyl', 'zml', 'wbq', 'gnm', 'Enkb', 'snd', 'slq', 'jww', 'hwy', 'Edw', 'grb', 'Eqr', 'qwE', '$gf', 'kpb', 'zlf', 'lmm', '$dd', 'sfl', '$Tn', 'Amn', 'nHr', 'DyE', 'sjn', '$fw', 'Erf', 'Er$', 'Avr', 'byt', 'msk', 'xmd', 'ryE', 'rzq', 'wSy', 'Sdd', 'Ewr', 'kdy', 'bsT', 'brq', 'hzm', 'klb', 'Awl', 'wsq', 'nbt', '$bh', 'jzy', 'qHm', 'Emd', 'ftA', 'rTb', 'HZZ', 'Axw', 'dxn', '$nA', 'fwq', 'Elm', 'vbT', 'kml', 'Dmm', 'bhj', 'Ayy', 'rAy', 'Ebr', 'dHD', 'qSw', 'twb', 'gny', 'klf', 'msH', 'xrTm', 'nEl', '$yd', 'pEn', 'Eff', 'ybs', 'Slb', 'krs', 'Erb', 'rDE', 'wkz', 'glm', 'wTn', '$kl', 'sHq', 'sdd', 'xrS', 'ArD', 'fsH', 'Sgw', 'Ejm', 'ldd', 'jEl', 'sfh', 'qll', 'knn', 'Hdq', 'sll', 'Twr', 'gDb', 'gll', 'fkk', 'vEb', 'swT', 'SHb', 'tHt', 'rkE', 'blg', 'Swr', 'vjj', 'nbE', 'HDD', 'xym', 'nkb', 'srmd', 'ksl', '$kk', 'Add', 'nSf', 'Alf', 'wkl', '$ml', 'sgb', 'mlw', 'gDD', 'jry', 'Hnjr', 'fqh', 'dmw', 'ESf', 'rtl', 'nsk', 'rEb', 'Ewd', 'wrq', 'bky', 'qTT', 'xbt', 'jbr', 'ywm', 'dHr', 'kwy', 'hyj', 'Abl', 'ftq', 'bdw', 'vxn', 'Tff', 'frh', 'lwH', 'Hzn', 'syr', 'tmm', 'nSt', 'njw', 'fln', 'trk', 'xfD', 'xsf', 'SrT', 'vwr', 'qwt', 'Hjr', 'nbz', 'mll', 'qDD', 'skr', 'gdr', 'Ass', 'fTr', 'Hdb', 'zbr', 'Hbr', 'bht', 'ryb', 'Hjj', 'jwd', 'wEd', 'kmm', 'grr', 'm$j', 'xyT', 'xzn', 'jhz', 'nhy', 'Sbg', 'Hsn', 'bEv', 'gdq', 'drs', 'wqf', 'Esy', 'Ayd', 'lwn', 'gyr', '$rpm', 'fwj', 'kwkb', 'nkd', 'sHb', 'Hbs', 'qld', 'dsr', 'fnd', 'qmE', 'SnE', '$yE', '$Eb', 'nwS', 'lqH', 'hmr', 'rbS', 'hdy', 'Snw', 'slT', '$ms', 'tbb', 'jls', 'Ark', 'mzn', 'qly', 'xtr', 'nqD', 'Dgv', 'wfq', 'rxw', 'wSf', 'Sbr', 'fry', 'qwl', 'mHw', 'jyb', 'SwE', 'mkv', 'whn', 'Azr', 'wbl', 'mAy', 'xdE', 'dhn', 'Enw', 'Efw', 'gvw', 'Asn', 'xlT', 'Amd', 'hlk', 'gmm', 'A$r', 'Swf', 'msx', 'prr', 'bwl', 'Eln', 'Azf', 'gbn', 'nsx', 'mEy', 'k$T', 'fyl', 'xbr', 'Amw', 'sbH', 'khf', 'fkr', 'wkA', 'bEd', 'Sfd', 'dwr', 'ftl', '$wk', 'Hfd', 'TrH', 'lAlA', 'lbv', 'njs', 'Hry', 'Dyr', 'vll', 'Akl', 'Sdf', 'wTA', 'Srr', 'wfr', 'r$d', 'Ewq', 'bgt', 'dwn', 'lfw', 'bdE', 'HyD', 'wqE', 'srq', 'xld', 'bHr', 'jsd', 'dmE', 'kyf', 'lHq', 'mEn', 'Amt', 'jrH', 'Ebd', 'prE', 'skt', 'rhb', 'drj', 'frT', 'Hrr', 'xTf', 'vwb', 'zmhr', 'qmTr', 'rjf', 'hmz', 'swr', 'mxr', 'jss', 'fyD', 'Asw', 'dEw', 'AHd', 'bSr', 'mlH', 'lhw', 'sTw', 'End', 'hyt', 'zrE', 'Tyn', 'fsq', 'wzE', 'qdd', 'lmH', 'nwq', 'Anf', 'jmm', 'Ajl', 'xlE', 'Hyn', 'wSl', 'Hrb', 'nwm', 'trf', 'Hmr', 'Ebv', 'twr', 'jws', 'sqT', 'qsT', 'EsEs', 'Zll', 'Hbl', 'dll', 'ESr', 'Avv', 'bwA', 'lhb', 'hjE', 'mDg', 'xrb', 'btr', 'rbb', 'klA', 'fjr', 'rHm', 'Eqm', 'Drr', 'wH$', 'dEE', 'mss', 'glb', 'qrn', 'zfr', 'Alm', 'Hyf', 'jHd', 'ljA', 'srdq', 'vbt', 'Awb', 'fzE', 'Hdv', '$hr', 'pqn', 'grm', 'rmy', 'fAy', 'nfE', 'smE', 'qsm', 'brr', 'Elw', 'rkD', 'rsl', 'Emh', 'jdd', 'jyd', 'bgl', 'Hfw', 'jhl', 'lhv', 'rgd', 'ry$', 'gdw', 'zEm', 'xlf', 'Arb', 'sAl', 'msw', 'fSl', '$gl', 'qtr', 'nsf', 'nf$', 'fjw', 'Hrj', 'Edl', 'rmd', 'zwl', 'brm', 'lmz', 'jlb', 'dbr', 'Hly', 'HTT', 'jbl', 'qTr', 'zjj', 'nEj', 'sjr', 'rHl', 'tqn', 'n$A', 'pbb', 'rAf', 'Hjz', 'xwf', 'qEr', 'nfv', 'jnb', 'rdy', 'fwr', 'Efr', 'xrr', 'nSb', 'Twd', 'mjd', 'SEr', 'Hkm', 'qTE', 'E$w', 'Hzb', 'mrj', 'wDE', 'Erjn', 'ksd', 'bvv', '$ks', 'g$w', 'slk', 'qry', 'rwE', 'gmz', 'sfE', 'nsb', 'nks', 'brz', 'xlS', 'myr', 'SrSr', 'jdl', 'rbE', 'wAl', 'rmm', 'wjf', 'DjE', '$fq', 'tEs', 'Hwt', 'jfA', 'vyb', 'Avl', 'SlSl', 'hll', '$fh', 'EDD', 'Ezb', 'All', 'TlH', 'HyS', 'swE', 'rbw', 'pmm', 'lwp', 'wly', 'hjr', 'Dnn', 'ngD', 'rjs', 'xns', 'kff', 'Ezr', 'Srm', 'slx', 'jml', 'rdd', 'Ans', 'jsm', 'pll', 'Hwr', 'srr', 'hnA', 'syH', 'lfH', 'mrD', 'rkd', 'Axp', 'Hwz', 'gly', 'rbT', 'Aff', 'ktm', 'Eyb', '$rE', 'Hw$', 'Hyy', 'dmg', 'glZ', 'f$l', 'lHd', 'knz', 'mTr', 'm$y', 'rSS', 'qbl', 'slb', 'h$m', 'nkS', 'zff', 'Htm', '$rb', 'kfy', 'rfq', 'xSf', 'tfv', 'gfr', 'DwA', 'Syf', 'Hqf', 'nkH', 'Zlm', 'dlk', 'Tlq', 'ndm', 'Any', 'kvr', 'smn', 'jvm', 'Hwp', 'nhr', 'nzg', 'nfH', 'dHw', 'xbv', 'xSm', 'HSy', 'Ehn', 'blE', 'rtq', 'kbr', 'swg', 'frd', 'rhT', 'Awh', 'rfE', 'SfH', 'krm', 'klm', 'fty', 'Tyb', 'kns', 'xwn', 'hwn', 'SEd', 'qpf', 'lhm', 'rSd', 'Hlm', 'nsA', 'jll', 'rwd', 'qsr', 'str', '$kw', 'Dyf', 'rAs', 'fdy', 'dfq', 'bwb', 'byn', 'Hll', 'rwD', 'wzr', 'qdw', 'wry', 'klH', 'Hbb', 'rjl', 'lyt', 'Etd', '$yA', 'Hff', 'vbr', 'xwy', '$rq', 'qSf', 'gyZ', 'qmH', 'zjw', 'zry', 'fwD', 'Esl', 'Drb', 'ktb', 'Ezl', '$fE', 'HSd', 'wSb', 'Sfr', 'rEd', '$fy', 'Twl', 'ldn', 'brH', 'Ejz', 'sds', 'kZm', 'Eql', 'bld', 'Awy', 'Sdy', 'bAs', 'dyn', 'mny', 'SrE', 'bxs', 'snbl', 'zll', 'jbb', 'rqd', 'fkh', 'jrf', 'xms', 'Hwj', 'Alh', 'blw', 'jdv', 'Abb', 'sry', 'lwt', 'mhl', 'Hyd', 'Ezw', 'xDd', 'hjd', 'TEm', 'qbr', 'SdE', 'TbE', 'mkw', 'zwj', 'bdl', '$rT', 'rhq', 'swH', 'slw', 'Zhr', 'jrz', 'ASl', 'ETf', 'Epb', 'rkb', 'qbD', 'bEr', 'DhA', '$TT', 'nqm', 'hDm', 'Smt', 'hzA', 'fr$', 'jwz', 'n$z', 'Snm', 'Smd', 'xll', 'hmn', 'wHy', 'HTm', 'mxD', '$wZ', 'HSl', 'jhd', 'wsl', 'qrd', 'Tgy', 'zyd', '$ry', 'nbp', 'sqy', 'vny', 'Skk', 'Ewp', 'nsy', 'gT$', 'ndd', 'Twf', 'ljj', 'Hrq', 'gmr', 'qtl', 'Tmv', 'rqq', 'bDE', '$jr', 'kwb', 'lqy', 'nwr', 'grw', 'Trw', 'Sbw', 'ydy', 'wHd', 'nws', 'fzz', 'dmdm', 'mvl', 'qws', 'rpl', 'ETw', 'vqb', 'Hnf', 'Dgn', 'Hjb', 'jrE', 'shl', 'wjl', 'fnn', 'lHm', 'kfl', 'wjh', 'bAr', 'ysr', 'bls', 'mrd', 'srb', 'xmS', 'nqp', 'snw', 'sqm', 'lwy', 'rqb', 'Shr', 'DEf', 'khn', 'xwl', 'bTr', 'zyl', 'pAm', 'xDE', 'yAs', 'pkr', 'Emm', 'zhq', 'nEs', 'bED', 'sbE', 'nZr', 'kbd', 'Sfw', 'DHk', 'Srf', 'lqf', 'mhd', 'Smm', 'Hrm', 'E$r', 'Hsm', 'bnn', 'sbT', 'nsl', 'sEy', 'fH$', 'wzn', 'Epr', 'Trd', 'Enq', 'hyA', 'qDb', 'Sgr', 'Afk', 'wld', 'HSb', 'nsr', 'hwd', 'bTl', 'HDr', 'kbb', 'mzj', 'Zfr', 'Hlq', '$tw', 'gwS', 'Hnk', 'rkz', 'rfrf', 'SbE', 'nkl', 'qrA', 'flk', 'mkn', '$rd', 'ksb', 'mwt', 'Eyl', 'qwm', 'drr', 'nzE', 'Ewn', 'xpl', 'bgy', 'Azz', 'brk', 'Ejb', 'dlw', 'Srx', 'Amm', 'bjs', 'nzl', 'nSr', 'Hmy', 'sbq', 'gSb', 'Etq', 'sqf', 'jvv', 'rtE', 'Hwl', 'ESm', 'dhr', 'nkv', 'wqb', 'ymm', 'k$f', 'lzm', 'skb', 'Ajr', 'wlj', 'qlb', 'wqd', 'Abq', 'lbs', 'rdf', 'h$$', 'brd', 'myd', 'Anm', 'sfr', 'krr', 'bsr', 'qdr', 'nqb', 'jnd', 'zny', 'Tfl', 'zyn', 'Ent', 'slm', 'Hrf', 'ETl', 'ESy', 'Aym', 'xfy', 'Hqb', 'qnt', 'dhm', 'Erj', 'Slw', 'dfE', 'wdy', 'qmr', 'xzy', 'nDx', 'rfd', 'sHr', 'Asr', 'xlq', 'grq', 'rqy', 'fqr', 'wdq', 'brhn', 'skn', 'sxT', 'nfs', 'frj', 'swl', '$Er', 'Emr', 'jmH', '$mz', 'qny', 'ytm', 'qrr', 'Eqd', 'njm', 'fwh', 'dxr', 'qwb', 'Eyr', 'yqZ', 'qrf', 'qSm', 'Ddd', 'mwj', 'jwb', 'SyH', 'hdm', 'rft', 'kvb', 'nxr', 'Eyn', '$TA', 'frt', '$kr', 'hmm', 'wvn', 'gwl', 'znm', 'sEd', 'xDr', 'qsTs', 'zmr', 'kyd', 'wjd', 'gfl', 'Edd', 'jyA', 'hAt', 'byE', 'Dnk', '$qq', 'qbH', 'jpw', 'nfp', 'jmd', 'fsr', 'wEy', 'EbA', 'btl', 'zkw', 'lys', 'rwH', 'myz', 'nwn', 'jdr', 'Tmn', 'fxr', 'Ewm', 'SrH', 'frv', 'sTH', 'drk', 'nqE', 'Hvv', 'sEr', 'wfy', 'dwl', 'zlzl', 'hzz', 'slf', 'zHf', 'HTb', 'bgD', 'Tyr', 'jby', 'zrq', 'Ejf', 'EZm', 'mdn', 'mlk', 'Dll', 'nbA', 'nAy', 'rhn', 'ESw', 'wtn', 'mdd', 'mhn', 'xbA', 'srj', 'gyD', 'qrE', '$xS', 'ymn', 'HwT', 'fsd', 'nTf', 'bsm', 'b$r', 'Err', 'jvw', 'rjE', 'xrq', 'wbr', 'SfSf', 'nsw', 'qfl', 'Swm', 'zyt', 'xff', 'swq', 'Ajj', 'rsw', 'Ejl', 'jwf', 'sfn', '$mt', 'hdd', 'Hsr', 'trb', 'xmT', 'brj', 'klw', 'nkr', 'mwr', 'wjb', 'sAl', 'brr', 'hmn', 'mwt', 'zlm', 'Hyq', 'phb', 'mlk', 'ESw', 'Hsr', 'SbE', 'SEd', 'wdd', 'qwl', 'grf', 'Avm', 'hjr', 'glf', 'jwE', 'rzq', 'nTH', 'dmE', 'HbT', 'Tms', 'Hyy', 'kbr', 'qsw', 'qSS', 'Amw', 'kff', 'HwT', 'qtr', 'Emy', 'khl', 'pbpb', 'njm', 'dlw', 'ksw', 'sfH', 'pbH', 'qvA', 'jld', 'slw', 'wdy', 'Syd', 'xll', 'Hbr', 'frH', 'xlf', 'Evw', 'TwE', 'Tlq', 'fqr', 'qSd', 'Hwr', 'xbT', 'Dyq', 'swy', 'wEZ', 'npr', 'rhn', 'Evr', 'Esy', 'rmz', 'mSr', 'Hmy', 'EDD', 'rEb', 'nml', 'jrH', 'n$A', 'ftl', 'gmr', 'Abl', 'bqy', 'ybs', 'Alf', 'xrb', 'ksl', 'bTn', 'qnTr', 'fr$', 'xmS', 'rDE', 'vql', 'wlj', 'fsd', 'gnm', 'wqt', 'bSr', 'End', 'bsl', 'wqd', 'Sdr', 'x$y', 'prr', 'n$z', 'ESm', 'Hbb', 'slm', 'xfy', 'Hmr', 'DAn', 'xTf', 'xmr', 'Ent', 'bHv', 'qrTs', '$jr', 'ESr', 'mdd', 'nsw', 'nbt', 'Amd', 'fZZ', 'fTr', 'xlq', 'ArD', 'Srf', 'Hwb', 'Hkm', 'byn', 'bkr', 'Trq', 'gsl', 'Sdq', 'zrE', 'Esr', 'bhm', '$kr', 'bSl', 'Ajl', 'zyg', 'bdE', 'HSn', 'jHd', 'zxrf', 'skr', 'bEd', 'xyT', '$yA', 'Edd', 'TEn', 'mvl', 'nqD', 'Avr', 'fyD', 'xTA', 'DjE', 'lmm', 'xwf', 'mqt', 'HfZ', 'mwh', 'sEr', 'jby', 'gfl', 'Twl', 'Abw', 'byE', 'kyn', 'mTr', 'swE', 'qrb', '$Tr', 'Drb', 'Amr', 'wld', 'kwd', 'nwm', 'Sly', 'lbs', 'rqb', 'nws', 'fwm', 'rmn', 'Swb', 'qsT', 'slT', 'rbH', 'wqy', 'xyr', 'hAt', 'ndd', 'bTA', 'kwn', 'bht', 'Ehd', 'jHm', 'sHb', 'Tmn', 'HyS', 'xff', 'bxs', 'hwd', 'Ejl', 'rbS', 'sHt', 'dbb', 'dnr', 'nbT', 'dxl', 'wzr', 'Slb', 'Srr', 'Asr', 'Swr', 'wbl', 'rwH', 'hdy', 'xwy', 'smE', 'wSy', 'pkw', 'vmn', 'xbr', '$nA', 'Zlm', 'rmH', 'DEf', 'Ezz', 'grq', 'rEy', 'kmh', 'Twq', 'Hll', 'sbE', 'Ewj', 'ysr', 'bwA', 'g$w', 'Amn', 'kyl', 'mnE', 'HSr', 'wrv', 'wpr', 'sds', 'SEq', 'Hwp', 'lsn', 'rfv', 'dbr', 'gmm', 'fty', 'klm', 'Sgr', 'krs', 'sEy', 'xlS', 'glm', 'syb', 'nsk', 'drk', 'gzw', 'Ans', 'sbt', 'xSm', 'pwq', 'fwz', 'fwr', 'fEl', 'whb', 'SbA', 'Elw', 'Tll', 'btk', 'nzl', 'jbl', 'lbv', 'Hlf', 'hll', 'zll', 'rdy', 'rks', '$Tn', 'bTl', 'zyn', 'Hrq', 'Hfr', 'drs', 'wsT', 'rdd', 'Hlq', 'Sfr', 'Ewn', 'wfq', 'bls', 'Ebr', 'knn', 'srq', 'sbl', 'wjh', 'frq', 'rfE', 'Erf', 'gyb', 'Anf', 'slf', 'TfA', 'TEm', 'Hrb', 'zwj', 'qnw', 'qss', 'Tyb', 'mny', '$ml', 'frg', 'brS', 'vlv', 'qmr', 'drA', 'xlw', 'mrA', 'wfy', 'vqf', 'frd', '$Hm', 'sqy', 'xld', 'jyA', 'Tyn', 'nhy', 'nsl', 'nfr', 'wrq', 'wqE', 'Snm', 'rbw', 'rDw', 'kml', 'bEv', 'qSr', 'wqp', 'bwb', 'HTT', 'qsm', 'zEm', 'vwr', 'rjs', 'zlzl', '$fw', 'Trf', 'tlw', 'qTE', 'whn', 'm$y', 'vmr', 'wHd', 'vby', 'Hyr', 'lHq', 'hwy', 'Ady', 'jhr', 'glb', 'dAb', 'grb', 'jwr', 'Slw', 'bqr', 'brhn', 'Awd', 'ASr', 'lEn', 'sbT', 'bEl', 'Dll', 'Ewm', 'byt', 'ytm', 'SrT', 'zkw', 'Eql', 'Eqr', 'lwy', 'klb', 'myd', 'kpb', 'x$E', 'nAy', 'bql', 'zyd', 'srE', 'Eyn', 'nbA', 'flH', 'jbt', 'nfy', 'fqh', 'lEb', 'krb', 'xrq', 'dfE', 'Drr', 'nhr', 'Sld', 'fyA', 'qwy', 'nsx', 'nqm', 'w$y', 'trb', 'glw', 'drr', 'Hnf', 'rsx', 'bld', 'Ekf', 'xdE', 'Syr', 'lgw', 'mwl', 'qbD', 'qnt', 'qry', 'DyE', 'Hzn', 'snbl', 'Eds', 'bvv', 'nwy', 'Erw', 'dwm', 'mrr', 'hbT', 'jzy', 'xlT', 'Trd', 'xrj', 'snh', 'ldn', 'ndw', 'rhb', 'qrd', 'ftH', 'Ezm', 'gll', 'nxl', 'rHm', 'brk', 'Er$', 'srH', 'krm', 'jdl', 'gwT', 'byD', 'mhd', 'Hqq', 'Abd', 'xsr', 'fH$', 'lys', 'H$r', 'HDr', 'fkr', 'rkb', 'HyD', 'nyl', 'sxr', 'fjr', 'kfl', 'jhd', 'Ejz', 'rbT', 'qds', 'mry', 'nwr', 'gny', 'rAf', 'vwb', 'ktm', 'Sbr', 'r$d', 'nEs', 'wSf', 'drj', 'ryb', 'rgb', 'Hdv', 'xyl', 'Afl', 'mlq', 'kyd', 'wdE', 'xrS', 'fwt', 'mrd', 'tbE', 'qrr', 'Sfw', 'EZm', 'grr', 'krr', 'jry', 'fry', 'blg', 'nkH', 'sbb', 'wHy', 'rgd', 'wvq', 'bgD', 'bdr', 'flk', 'xyb', 'nsy', 'xnq', 'Hsb', 'frD', 'swd', 'fSm', '$bh', 'f$l', 'rTb', 'Eqd', 'lms', 'qlm', 'ErD', '$fE', 'Akl', 'fDl', 'fDD', 'smw', 'mrD', 'dyn', 'Hrj', 'k$f', 'nzE', 'Edw', 'srr', 'Tyr', 'Ewd', 'bsT', 'fdy', 'ywm', 'mnn', 'b$r', 'jEl', 'ydy', 'jnf', 'jmE', 'wDE', 'HZZ', 'Eqb', 'sxT', 'bhl', 'Aty', 'pkr', 'Sbg', 'Hjj', 'pnb', 'blw', 'nqS', 'mkr', 'mll', 'myl', 'nkr', 'kwkb', 'jwb', 'fsq', 'rkE', 'qDy', 'sfr', 'rEd', 'qdr', 'Hmm', 'Zhr', 'xSS', 'fxr', 'Hzb', 'Hpr', 'bzg', 'Ezr', 'nhj', '$kk', 'Alm', 'Eff', 'nkf', 'prA', 'xsA', 'fSl', 'qEd', 'jnH', 'Awb', 'fDw', 'frT', 'bdl', 'jrm', 'qwm', 'nqb', 'Epb', 'ldd', 'nfs', 'myz', 'kvr', 'Tgy', 'lfw', 'DwA', 'Afk', 'ksb', 'dnw', 'Ajr', 'wSl', 'Emr', 'jsm', 'qhr', 'Hjr', 'Axp', 'Eml', 'Hwy', 'flq', 'Ayd', 'Amm', 'bgt', 'kfy', 'hwn', 'Hlm', 'jwz', 'TlE', 'brj', 'Thr', 'qll', 'mEz', 'nqp', 'brz', 'wsl', '$yd', 'njw', 'Hss', 'sfl', 'jzA', 'Hyn', 'wry', 'Alh', 'xnzr', 'nHl', 'snn', 'lwm', 'dwr', 'hzA', 'rgm', 'hyA', 'Sdf', 'nSf', 'skn', 'Ejb', 'rsl', 'Smm', 'sbH', '$qq', 'tyh', 'Any', 'sjd', '$hd', 'Sgw', 'Hml', 'Ewp', 'jnn', 'Etd', 'kfr', 'lyl', '$rq', 'Emd', 'Alw', 'rjz', 'vny', 'rjE', 'Ayy', 'Ebd', 'rjw', 'zbr', 'qwt', 'tjr', 'Hyv', 'Hrf', 'Hrv', '$rr', 'Emm', '$HH', 'TbE', 'DrE', 'xtm', 'Hwl', 'gDb', 'zHzH', 'gwy', 'nSb', 'gfr', 'yAs', 'sTr', 'ktb', '$rk', 'Hrr', 'ftr', 'Hdd', 'EDl', 'wqf', 'Sdd', 'ymm', 'bAs', 'Hmd', 'bdw', 'Twf', 'bkm', 'rAs', 'vwy', 'ynE', 'glZ', 'snw', 'jnd', 'Enb', 'qbl', 'kZm', 'sAm', 'mlw', 'tHt', 'Elm', 'lqy', '$rE', 'xDr', 'syr', 'sqT', 'dmw', 'xpl', 'mtE', 'fAy', 'Asw', 'qrn', 'pxr', 'Hsn', 'mss', 'ymn', 'SbH', 'Efw', 'Zll', 'SfH', 'gmD', '$hr', 'Anv', 'bHr', 'qlb', 'msH', 'krh', 'kEb', 'nqr', 'nbp', 'Axw', 'wly', 'bny', '$dd', 'Awy', 'sfh', 'rAy', 'ftn', 'bED', 'nkl', 'qld', 'SHb', 'Hbl', 'nEm', '$Er', '$rb', 'xTw', 'Hrm', 'gyr', 'ESy', 'kll', 'xTb', 'srf', 'rfq', 'pll', 'rbE', 'qtl', 'wsn', 'fwq', 'grw', 'Axr', 'vbt', '$wr', 'dwl', 'lyn', 'zyl', 'fqE', 'xwn', 'Ezl', 'zwd', 'sHr', 'swm', 'nfq', 'AHd', 'Swm', 'Znn', 'xzy', '$ry', 'msk', 'kbt', 'wjd', 'fAd', 'hlk', 'Apn', 'Awl', 'tmm', 'sfk', 'Hsd', 'nfx', 'Eln', '$yE', 'nSr', 'ndm', 'trk', 'Ahl', 'bxl', 'xbv', 'xwl', 'HrS', 'jhl', 'E$r', 'wsE', 'zyt', 'hnA', 'wkl', 'qdw', 'swA', 'qrD', 'nfE', 'rjm', '$hw', 'HrD', 'dEw', 'bgy', 'mHS', 'Ewl', 'nEq', 'HSd', 'qdm', 'pyE', 'qfw', 'xzn', 'rwd', 'Edl', 'qrH', 'brq', 'xwD', 'kyf', 'qrf', 'mlA', 'dry', 'Apy', 'Zfr', 'Twr', 'fwh', 'brA', 'lHm', 'wEd', 'SlH', 'sbq', 'mHq', 'rmy', 'Hbs', 'lTf', 'yqn', 'mAy', 'slH', 'wzn', 'rbb', 'sdd', 'qrA', 'xbl', '$rH', 'lHf', 'dwn', 'lwn', 'hmm', 'mkn', 'lhw', 'SnE', 'Aby', 'Emh', 'hzm', 'E$w', 'TmE', 'rjl', 'klf', 'jnb', 'wqr', 'xdn', 'nDj', 'gdw', 'jbr', 'xms', 'twb', 'gyZ', 'swr', 'lbb', 'nZr', 'Elq', '$ms'}
        total_root = len(roots)
        for r in roots:
            root_url = f"https://api.acikkuran.com/root/latin/{r}"
            root_response = requests.get(root_url)

            
            if root_response.status_code == 200:
                root_data = root_response.json()['data']
                root, created = Root.objects.get_or_create(
                    latin=root_data["latin"],
                    defaults={
                        'arabic': root_data['arabic'],
                        'transcription': root_data.get('transcription', ''),
                        'transcription_en': root_data.get('transcription_en', ''),
                        'mean': root_data.get('mean', ''),
                        'mean_en': root_data.get('mean_en', ''),
                        'char': RootChar.objects.get(id=root_data['rootchar_id'])
                    }
                )
                total_root-=1
                self.stdout.write(self.style.SUCCESS(f'{root_data["latin"]} kök verisi kaydedildi. kalan: {total_root}'))

            else:
                self.stdout.write(self.style.ERROR(f'{root_url} adresinden kök verisi çekilemedi.'))