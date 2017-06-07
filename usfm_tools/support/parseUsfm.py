# -*- coding: utf-8 -*-
#

from __future__ import print_function, unicode_literals
import sys
from pyparsing import Word, OneOrMore, nums, Literal, White, Group, Suppress, NoMatch, Optional, \
    CharsNotIn, MatchFirst


def usfmToken(key):
    return Group(Suppress(backslash) + Literal(key) + Suppress(White()))


def usfmBackslashToken(key):
    return Group(Literal(key))


def usfmEndToken(key):
    return Group(Suppress(backslash) + Literal(key + "*"))


def usfmTokenValue(key, value):
    return Group(Suppress(backslash) + Literal(key) + Suppress(White()) + Optional(value))


def usfmTokenNumber(key):
    return Group(Suppress(backslash) + Literal(key) + Suppress(White()) + Word(nums + '-()') + Suppress(White()))


# define grammar
# phrase = Word( alphas + "-.,!? —–‘“”’;:()'\"[]/&%=*…{}" + nums )
phrase = CharsNotIn("\n\\")
backslash = Literal("\\")
plus = Literal("+")

textBlock = Group(Optional(NoMatch(), "text") + phrase)
unknown = Group(Optional(NoMatch(), "unknown") + Suppress(backslash) + CharsNotIn(u' \n\t\\'))
escape = usfmTokenValue("\\", phrase)

id_token = usfmTokenValue("id", phrase)
ide = usfmTokenValue("ide", phrase)
sts = usfmTokenValue("sts", phrase)
h = usfmTokenValue("h", phrase)

mt = usfmTokenValue("mt", phrase)
mt1 = usfmTokenValue("mt1", phrase)
mt2 = usfmTokenValue("mt2", phrase)
mt3 = usfmTokenValue("mt3", phrase)
ms = usfmTokenValue("ms", phrase)
ms1 = usfmTokenValue("ms1", phrase)
ms2 = usfmTokenValue("ms2", phrase)
mr = usfmTokenValue("mr", phrase)
s = usfmTokenValue("s", phrase)
s1 = usfmTokenValue("s1", phrase)
s2 = usfmTokenValue("s2", phrase)
s3 = usfmTokenValue("s3", phrase)
s4 = usfmTokenValue("s4", phrase)
s5 = usfmTokenValue("s5", phrase)
r = usfmTokenValue("r", phrase)
p = usfmToken("p")
pi = usfmToken("pi")
pi2 = usfmToken("pi2")
b = usfmToken("b")
c = usfmTokenNumber("c")
cas = usfmToken("ca")
cae = usfmEndToken("ca")
cl = usfmTokenValue("cl", phrase)
v = usfmTokenNumber("v")
wjs = usfmToken("wj")
wje = usfmEndToken("wj")
q = usfmToken("q")
q1 = usfmToken("q1")
q2 = usfmToken("q2")
q3 = usfmToken("q3")
q4 = usfmToken("q4")
qa = usfmToken("qa")
qac = usfmToken("qac")
qc = usfmToken("qc")
qm = usfmToken("qm")
qm1 = usfmToken("qm1")
qm2 = usfmToken("qm2")
qm3 = usfmToken("qm3")
qr = usfmToken("qr")
qss = usfmToken("qs")
qse = usfmEndToken("qs")
qts = usfmToken("qt")
qte = usfmEndToken("qt")
nb = usfmToken("nb")
m = usfmToken("m")

# Footnotes
fs = usfmTokenValue("f", plus)
fr = usfmTokenValue("fr", phrase)
fre = usfmEndToken("fr")
fk = usfmTokenValue("fk", phrase)
ft = usfmTokenValue("ft", phrase)
fq = usfmTokenValue("fq", phrase)
fqa = usfmTokenValue("fqa", phrase)
fqae = usfmEndToken("fqa")
fqb = usfmTokenValue("fqb", phrase)
fe = usfmEndToken("f")
fp = usfmToken("fp")

# Cross References
xs = usfmTokenValue("x", plus)
xdcs = usfmToken("xdc")
xdce = usfmEndToken("xdc")
xo = usfmTokenValue("xo", phrase)
xt = usfmTokenValue("xt", phrase)
xe = usfmEndToken("x")

# Transliterated
tls = usfmToken("tl")
tle = usfmEndToken("tl")

# Transliterated
scs = usfmToken("sc")
sce = usfmEndToken("sc")

# Italics
ist = usfmToken("it")
ien = usfmEndToken("it")

# Bold
bds = usfmToken("bd")
bde = usfmEndToken("bd")
bdits = usfmToken("bdit")
bdite = usfmEndToken("bdit")

li = usfmToken("li")
li1 = usfmToken("li1")
li2 = usfmToken("li2")
li3 = usfmToken("li3")
li4 = usfmToken("li4")
d = usfmTokenValue("d", phrase)
sp = usfmToken("sp")
adds = usfmToken("add")
adde = usfmEndToken("add")
nds = usfmToken("nd")
nde = usfmEndToken("nd")
pbr = usfmBackslashToken("\\\\")
mi = usfmToken("mi")

# Comments
rem = usfmTokenValue("rem", phrase)

# Tables
tr = usfmToken("tr")
th1 = usfmToken("th1")
th2 = usfmToken("th2")
th3 = usfmToken("th3")
th4 = usfmToken("th4")
th5 = usfmToken("th5")
th6 = usfmToken("th6")
thr1 = usfmToken("thr1")
thr2 = usfmToken("thr2")
thr3 = usfmToken("thr3")
thr4 = usfmToken("thr4")
thr5 = usfmToken("thr5")
thr6 = usfmToken("thr6")
tc1 = usfmToken("tc1")
tc2 = usfmToken("tc2")
tc3 = usfmToken("tc3")
tc4 = usfmToken("tc4")
tc5 = usfmToken("tc5")
tc6 = usfmToken("tc6")
tcr1 = usfmToken("tcr1")
tcr2 = usfmToken("tcr2")
tcr3 = usfmToken("tcr3")
tcr4 = usfmToken("tcr4")
tcr5 = usfmToken("tcr5")
tcr6 = usfmToken("tcr6")

# Table of Contents
toc = usfmTokenValue("toc", phrase)
toc1 = usfmTokenValue("toc1", phrase)
toc2 = usfmTokenValue("toc2", phrase)
toc3 = usfmTokenValue("toc3", phrase)

# Introductory Materials
is1 = usfmTokenValue("is1", phrase) | usfmTokenValue("is", phrase)
ip = usfmToken("ip")
iot = usfmToken("iot")
io1 = usfmToken("io1") | usfmToken("io")
io2 = usfmToken("io2")
ior_s = usfmToken("ior")
ior_e = usfmEndToken("ior")
imt = usfmTokenValue("imt", phrase)
imt1 = usfmTokenValue("imt1", phrase)
imt2 = usfmTokenValue("imt2", phrase)
imt3 = usfmTokenValue("imt3", phrase)

# Quoted book title
bk_s = usfmToken("bk")
bk_e = usfmEndToken("bk")

element = MatchFirst([ide, id_token, sts, h, toc, toc1, toc2, toc3, mt, mt1, mt2, mt3,
                      ms,
                      ms1,
                      ms2,
                      mr,
                      s,
                      s1,
                      s2,
                      s3,
                      s4,
                      s5,
                      r,
                      pi2,
                      pi,
                      p,
                      mi,
                      b,
                      c,
                      cas,
                      cae,
                      cl,
                      v,
                      wjs,
                      wje,
                      nds,
                      nde,
                      q,
                      q1,
                      q2,
                      q3,
                      q4,
                      qa,
                      qac,
                      qc,
                      qm,
                      qm1,
                      qm2,
                      qm3,
                      qr,
                      qss,
                      qse,
                      qts,
                      qte,
                      nb,
                      m,
                      fs,
                      fr,
                      fre,
                      fk,
                      ft,
                      fq,
                      fqa,
                      fqae,
                      fqb,
                      fe,
                      fp,
                      xs,
                      xdcs,
                      xdce,
                      xo,
                      xt,
                      xe,
                      ist,
                      ien,
                      bds,
                      bde,
                      bdits,
                      bdite,
                      li,
                      li1,
                      li2,
                      li3,
                      li4,
                      d,
                      sp,
                      adds,
                      adde,
                      tls,
                      tle,
                      is1,
                      ip,
                      iot,
                      io1,
                      io2,
                      ior_s,
                      ior_e,
                      imt,
                      imt1,
                      imt2,
                      imt3,
                      bk_s,
                      bk_e,
                      scs,
                      sce,
                      pbr,
                      rem,
                      tr,
                      th1,
                      th2,
                      th3,
                      th4,
                      th5,
                      th6,
                      thr1,
                      thr2,
                      thr3,
                      thr4,
                      thr5,
                      thr6,
                      tc1,
                      tc2,
                      tc3,
                      tc4,
                      tc5,
                      tc6,
                      tcr1,
                      tcr2,
                      tcr3,
                      tcr4,
                      tcr5,
                      tcr6,
                      textBlock,
                      escape,
                      unknown])

usfm = OneOrMore(element)


# input string
def parseString(unicodeString):
    try:
        cleaned = clean(unicodeString)
        tokens = usfm.parseString(cleaned, parseAll=True)
    except Exception as e:
        print(e)
        print(repr(unicodeString[:50]))
        sys.exit()
    return [createToken(t) for t in tokens]


def clean(unicodeString):
    # We need to clean the input a bit. For a start, until
    # we work out what to do, non breaking spaces will be ignored
    # ie 0xa0
    ret_value = unicodeString.replace('\xa0', ' ')

    # escape illegal USFM sequences
    ret_value = ret_value.replace('\\ ',  '\\\\ ')
    ret_value = ret_value.replace('\\\n', '\\\\\n')
    ret_value = ret_value.replace('\\\r', '\\\\\r')
    ret_value = ret_value.replace('\\\t', '\\\\\t')
    return ret_value


def createToken(t):
    options = {
        'id': IDToken,
        'ide': IDEToken,
        'sts': STSToken,
        'h': HToken,
        'mt': MTToken,
        'mt1': MTToken,
        'mt2': MT2Token,
        'mt3': MT3Token,
        'ms': MSToken,
        'ms1': MSToken,
        'ms2': MS2Token,
        'mr': MRToken,
        'p': PToken,
        'pi': PIToken,
        'pi2': PI2Token,
        'b': BToken,
        's': SToken,
        's1': SToken,
        's2': S2Token,
        's3': S3Token,
        's4': S4Token,
        's5': S5Token,
        'mi': MIToken,
        'r': RToken,
        'c': CToken,
        'ca': CASToken,
        'ca*': CAEToken,
        'cl': CLToken,
        'v': VToken,
        'wj': WJSToken,
        'wj*': WJEToken,
        'q': QToken,
        'q1': Q1Token,
        'q2': Q2Token,
        'q3': Q3Token,
        'q4': Q4Token,
        'qa': QAToken,
        'qac': QACToken,
        'qc': QCToken,
        'qm': QMToken,
        'qm1': QM1Token,
        'qm2': QM2Token,
        'qm3': QM3Token,
        'qr': QRToken,
        'qs': QSSToken,
        'qs*': QSEToken,
        'qt': QTSToken,
        'qt*': QTEToken,
        'nb': NBToken,
        'f': FSToken,
        'fr': FRToken,
        'fr*': FREToken,
        'fk': FKToken,
        'ft': FTToken,
        'fq': FQToken,
        'fqa': FQAToken,
        'fqa*': FQAEToken,
        'fqb': FQAEToken,
        'f*': FEToken,
        'fp': FPToken,
        'x': XSToken,
        'xdc': XDCSToken,
        'xdc*': XDCEToken,
        'xo': XOToken,
        'xt': XTToken,
        'x*': XEToken,
        'it': ISToken,
        'it*': IEToken,
        'bd': BDSToken,
        'bd*': BDEToken,
        'bdit': BDITSToken,
        'bdit*': BDITEToken,
        'li': LIToken,
        'li1': LI1Token,
        'li2': LI2Token,
        'li3': LI3Token,
        'li4': LI4Token,
        'd': DToken,
        'sp': SPToken,
        'i*': IEToken,
        'add': ADDSToken,
        'add*': ADDEToken,
        'nd': NDSToken,
        'nd*': NDEToken,
        'sc': SCSToken,
        'sc*': SCEToken,
        'm': MToken,
        'tl': TLSToken,
        'tl*': TLEToken,
        '\\\\': EscapedToken,
        'rem': REMToken,
        'tr': TRToken,
        'th1': TH1Token,
        'th2': TH2Token,
        'th3': TH3Token,
        'th4': TH4Token,
        'th5': TH5Token,
        'th6': TH6Token,
        'thr1': THR1Token,
        'thr2': THR2Token,
        'thr3': THR3Token,
        'thr4': THR4Token,
        'thr5': THR5Token,
        'thr6': THR6Token,
        'tc1': TC1Token,
        'tc2': TC2Token,
        'tc3': TC3Token,
        'tc4': TC4Token,
        'tc5': TC5Token,
        'tc6': TC6Token,
        'tcr1': TCR1Token,
        'tcr2': TCR2Token,
        'tcr3': TCR3Token,
        'tcr4': TCR4Token,
        'tcr5': TCR5Token,
        'tcr6': TCR6Token,
        'toc1': TOC1Token,
        'toc2': TOC2Token,
        'toc3': TOC3Token,
        'is': IS1_Token,
        'is1': IS1_Token,
        'imt': IMT1_Token,
        'imt1': IMT1_Token,
        'imt2': IMT2_Token,
        'imt3': IMT3_Token,
        'ip': IP_Token,
        'iot': IOT_Token,
        'io': IO1_Token,
        'io1': IO1_Token,
        'io2': IO2_Token,
        'ior': IOR_S_Token,
        'ior*': IOR_E_Token,
        'bk': BK_S_Token,
        'bk*': BK_E_Token,
        'text': TEXTToken,
        'unknown': UnknownToken
    }
    for opt_key, opt_val in options.items():
        if t[0] == opt_key:
            if len(t) == 1:
                return opt_val()
            else:
                return opt_val(t[1])
    raise Exception(t[0])


# noinspection PyMethodMayBeStatic
class UsfmToken(object):
    def __init__(self, value=""):
        self.value = value

    def getValue(self): return self.value

    def isUnknown(self): return False

    def isID(self): return False

    def isIDE(self): return False

    def isSTS(self): return False

    def isH(self): return False

    def isTOC1(self): return False

    def isTOC2(self): return False

    def isTOC3(self): return False

    def isMT(self): return False

    def isMT2(self): return False

    def isMT3(self): return False

    def isMS(self): return False

    def isMS2(self): return False

    def isMR(self): return False

    def isR(self): return False

    def isP(self): return False

    def isPI(self): return False

    def isPI2(self): return False

    def isS(self): return False

    def isS2(self): return False

    def isS3(self): return False

    def isS4(self): return False

    def isS5(self): return False

    def isMI(self): return False

    def isC(self): return False

    def isCAS(self): return False

    def isCAE(self): return False

    def isCL(self): return False

    def isV(self): return False

    def isWJS(self): return False

    def isWJE(self): return False

    def isTEXT(self): return False

    def isQ(self): return False

    def isQ1(self): return False

    def isQ2(self): return False

    def isQ3(self): return False

    def isQ4(self): return False

    def isQA(self): return False

    def isQAC(self): return False

    def isQC(self): return False

    def isQM(self): return False

    def isQM1(self): return False

    def isQM2(self): return False

    def isQM3(self): return False

    def isQR(self): return False

    def isQSS(self): return False

    def isQSE(self): return False

    def isQTS(self): return False

    def isQTE(self): return False

    def isNB(self): return False

    def isFS(self): return False

    def isFR(self): return False

    def isFRE(self): return False

    def isFK(self): return False

    def isFT(self): return False

    def isFQ(self): return False

    def isFQA(self): return False

    def isFQAE(self): return False

    def isFQB(self): return False

    def isFE(self): return False

    def isFP(self): return False

    def isXS(self): return False

    def isXDCS(self): return False

    def isXDCE(self): return False

    def isXO(self): return False

    def isXT(self): return False

    def isXE(self): return False

    def isIS(self): return False

    def isIE(self): return False

    def isSCS(self): return False

    def isSCE(self): return False

    def isLI(self): return False

    def isLI1(self): return False

    def isLI2(self): return False

    def isLI3(self): return False

    def isLI4(self): return False

    def isD(self): return False

    def isSP(self): return False

    def isADDS(self): return False

    def isADDE(self): return False

    def isNDS(self): return False

    def isNDE(self): return False

    def isTLS(self): return False

    def isTLE(self): return False

    def isBDS(self): return False

    def isBDE(self): return False

    def isBDITS(self): return False

    def isBDITE(self): return False

    def isPBR(self): return False

    def isM(self): return False

    def isREM(self): return False

    def isTR(self): return False

    def isTH1(self): return False

    def isTH2(self): return False

    def isTH3(self): return False

    def isTH4(self): return False

    def isTH5(self): return False

    def isTH6(self): return False

    def isTHR1(self): return False

    def isTHR2(self): return False

    def isTHR3(self): return False

    def isTHR4(self): return False

    def isTHR5(self): return False

    def isTHR6(self): return False

    def isTC1(self): return False

    def isTC2(self): return False

    def isTC3(self): return False

    def isTC4(self): return False

    def isTC5(self): return False

    def isTC6(self): return False

    def isTCR1(self): return False

    def isTCR2(self): return False

    def isTCR3(self): return False

    def isTCR4(self): return False

    def isTCR5(self): return False

    def isTCR6(self): return False

    def is_toc1(self): return False

    def is_toc2(self): return False

    def is_toc3(self): return False

    def is_is1(self): return False

    def is_imt1(self): return False

    def is_imt2(self): return False

    def is_imt3(self): return False

    def is_ip(self): return False

    def is_iot(self): return False

    def is_io1(self): return False

    def is_io2(self): return False

    def is_ior_s(self): return False

    def is_ior_e(self): return False

    def is_bk_s(self): return False

    def is_bk_e(self): return False


class UnknownToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderUnknown(self)

    def isUnknown(self): return True

class EscapedToken(UsfmToken):
    def renderOn(self, printer):
        self.value = '\\'
        return printer.renderTEXT(self)

    def isUnknown(self): return True


class IDToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderID(self)

    def isID(self): return True


class IDEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderIDE(self)

    def isIDE(self): return True


class STSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderSTS(self)

    def isSTS(self): return True


class HToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderH(self)

    def isH(self): return True


class TOC1Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTOC1(self)

    def isTOC1(self): return True


class TOC2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTOC2(self)

    def isTOC2(self): return True


class TOC3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTOC3(self)

    def isTOC3(self): return True


class MTToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMT(self)

    def isMT(self): return True


class MT2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMT2(self)

    def isMT2(self): return True


class MT3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMT3(self)

    def isMT3(self): return True


class MSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMS(self)

    def isMS(self): return True


class MS2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMS2(self)

    def isMS2(self): return True


class MRToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMR(self)

    def isMR(self): return True


class MIToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderMI(self)

    def isMI(self): return True


class RToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderR(self)

    def isR(self): return True


class PToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderP(self)

    def isP(self): return True


# noinspection PyMethodMayBeStatic
class BToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderB(self)

    def isB(self): return True


class CToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderC(self)

    def isC(self): return True


class CASToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderCAS(self)

    def isCAS(self): return True


class CAEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderCAE(self)

    def isCAE(self): return True


class CLToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderCL(self)

    def isCL(self): return True


class VToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderV(self)

    def isV(self): return True


class TEXTToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTEXT(self)

    def isTEXT(self): return True


class WJSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderWJS(self)

    def isWJS(self): return True


class WJEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderWJE(self)

    def isWJE(self): return True


class SToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderS(self)

    def isS(self): return True


class S2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderS2(self)

    def isS2(self): return True


class S3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderS3(self)

    def isS3(self): return True


class S4Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderS4(self)

    def isS4(self): return True


class S5Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderS5(self)

    def isS5(self): return True


class QToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQ(self)

    def isQ(self): return True


class Q1Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQ1(self)

    def isQ1(self): return True


class Q2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQ2(self)

    def isQ2(self): return True


class Q3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQ3(self)

    def isQ3(self): return True


class Q4Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQ4(self)

    def isQ4(self): return True


class QAToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQA(self)

    def isQA(self): return True


class QACToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQAC(self)

    def isQAC(self): return True


class QCToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQC(self)

    def isQC(self): return True


class QMToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQM(self)

    def isQM(self): return True


class QM1Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQM1(self)

    def isQM1(self): return True


class QM2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQM2(self)

    def isQM2(self): return True


class QM3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQM3(self)

    def isQM3(self): return True


class QRToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQR(self)

    def isQR(self): return True


class QSSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQSS(self)

    def isQSS(self): return True


class QSEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQSE(self)

    def isQSE(self): return True


class QTSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQTS(self)

    def isQTS(self): return True


class QTEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderQTE(self)

    def isQTE(self): return True


class NBToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderNB(self)

    def isNB(self): return True


class FSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFS(self)

    def isFS(self): return True


class FRToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFR(self)

    def isFR(self): return True


class FREToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFRE(self)

    def isFRE(self): return True


class FKToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFK(self)

    def isFK(self): return True


class FTToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFT(self)

    def isFT(self): return True


class FQToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFQ(self)

    def isFQ(self): return True


class FQAToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFQA(self)

    def isFQA(self): return True


class FQAEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFQAE(self)

    def isFQAE(self): return True


class FQBToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFQAE(self)

    def isFQB(self): return True


class FEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFE(self)

    def isFE(self): return True


class FPToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderFP(self)

    def isFP(self): return True


class ISToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderIS(self)

    def isIS(self): return True


class IEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderIE(self)

    def isIE(self): return True


class BDSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderBDS(self)

    def isBDS(self): return True


class BDEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderBDE(self)

    def isBDE(self): return True


class BDITSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderBDITS(self)

    def isBDITS(self): return True


class BDITEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderBDITE(self)

    def isBDITE(self): return True


class LIToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderLI(self)

    def isLI(self): return True


class LI1Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderLI1(self)

    def isLI1(self): return True


class LI2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderLI2(self)

    def isLI1(self): return True


class LI3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderLI3(self)

    def isLI1(self): return True


class LI4Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderLI4(self)

    def isLI1(self): return True


class DToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderD(self)

    def isD(self): return True


class SPToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderSP(self)

    def isSP(self): return True


class ADDSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderADDS(self)

    def isADDS(self): return True


class ADDEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderADDE(self)

    def isADDE(self): return True


class NDSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderNDS(self)

    def isNDS(self): return True


class NDEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderNDE(self)

    def isNDE(self): return True


class PBRToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderPBR(self)

    def isPBR(self): return True


# Cross References
class XSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderXS(self)

    def isXS(self): return True


class XDCSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderXDCS(self)

    def isXDCS(self): return True


class XDCEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderXDCE(self)

    def isXDCE(self): return True


class XOToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderXO(self)

    def isXO(self): return True


class XTToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderXT(self)

    def isXT(self): return True


class XEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderXE(self)

    def isXE(self): return True


class MToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderM(self)

    def isM(self): return True


# Transliterated Words
class TLSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTLS(self)

    def isTLS(self): return True


class TLEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTLE(self)

    def isTLE(self): return True


# Indenting paragraphs
class PIToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderPI(self)

    def isPI(self): return True


class PI2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderPI2(self)

    def isPI2(self): return True


# Small caps
class SCSToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderSCS(self)

    def isSCS(self): return True


class SCEToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderSCE(self)

    def isSCE(self): return True


# REMarks
class REMToken(UsfmToken):
    def renderOn(self, printer): return printer.renderREM(self)

    def isREM(self): return True


# Tables
class TRToken(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTR(self)

    def isTR(self): return True


class TH1Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTH1(self)

    def isTH1(self): return True


class TH2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTH2(self)

    def isTH2(self): return True


class TH3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTH3(self)

    def isTH3(self): return True


class TH4Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTH4(self)

    def isTH4(self): return True


class TH5Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTH5(self)

    def isTH5(self): return True


class TH6Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTH6(self)

    def isTH6(self): return True


class THR1Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTHR1(self)

    def isTHR1(self): return True


class THR2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTHR2(self)

    def isTHR2(self): return True


class THR3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTHR3(self)

    def isTHR3(self): return True


class THR4Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTHR4(self)

    def isTHR4(self): return True


class THR5Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTHR5(self)

    def isTHR5(self): return True


class THR6Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTHR6(self)

    def isTHR6(self): return True


class TC1Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTC1(self)

    def isTC1(self): return True


class TC2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTC2(self)

    def isTC2(self): return True


class TC3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTC3(self)

    def isTC3(self): return True


class TC4Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTC4(self)

    def isTC4(self): return True


class TC5Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTC5(self)

    def isTC5(self): return True


class TC6Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTC6(self)

    def isTC6(self): return True


class TCR1Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTCR1(self)

    def isTCR1(self): return True


class TCR2Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTCR2(self)

    def isTCR2(self): return True


class TCR3Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTCR3(self)

    def isTCR3(self): return True


class TCR4Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTCR4(self)

    def isTCR4(self): return True


class TCR5Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTCR5(self)

    def isTCR5(self): return True


class TCR6Token(UsfmToken):
    def renderOn(self, printer):
        return printer.renderTCR6(self)

    def isTCR6(self): return True


# Introductions
class IS1_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_is1(self)

    def is_is1(self): return True


class IMT1_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_imt1(self)

    def is_imt1(self): return True


class IMT2_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_imt2(self)

    def is_imt2(self): return True


class IMT3_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_imt3(self)

    def is_imt3(self): return True


class IP_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_ip(self)

    def is_ip(self): return True


class IOT_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_iot(self)

    def is_iot(self): return True


class IO1_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_io1(self)

    def is_io1(self): return True


class IO2_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_io2(self)

    def is_io2(self): return True


class IOR_S_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_ior_s(self)

    def is_ior_s(self): return True


class IOR_E_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_ior_e(self)

    def is_ior_e(self): return True


# Quoted book title
class BK_S_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_bk_s(self)

    def is_bk_s(self): return True


class BK_E_Token(UsfmToken):
    def renderOn(self, printer): return printer.render_bk_e(self)

    def is_bk_e(self): return True
