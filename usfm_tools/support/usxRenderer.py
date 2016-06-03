# -*- coding: utf-8 -*-
#

import abstractRenderer
import codecs

#
#   Simplest renderer. Ignores everything except ascii text.
#

class USXRenderer(abstractRenderer.AbstractRenderer):

    def __init__(self, inputDir, outputPath, outputName, byBookFlag):
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilePath = outputPath
        self.outputFileName = outputName
        self.outputFileExt = u'.usx'
        self.inputDir = inputDir
        self.byBook = byBookFlag
        # Position
        self.currentC = 1
        self.currentV = 1
        self.book = u''
        # Flags
        self.printerState = {u'c': False, u'p': False, u'q': False, u'li': False, u'row': False, u'cell': False, u'table': False}
        # Errors
        self.error = u''

    def render(self):
        self.loadUSFM(self.inputDir)
        if self.byBook:
            print u'#### Creating One File Per Book\n'
            for bookName in self.booksUsfm:
                self.f = codecs.open(self.outputFilePath + bookName + self.outputFileExt, 'w', 'utf_8_sig')
                self.renderBook = bookName
                self.run()
                self.f.write( self.stopAll() )
                self.f.close()
        else:
            print u'#### Concatenating Books into ' + self.outputFileName + self.outputFileExt + u'\n'
            self.f = codecs.open(self.outputFilePath + self.outputFileName + self.outputFileExt, 'w', 'utf_8_sig')
            self.run()
            self.f.write( self.stopP() + self.stopQ() + self.stopLI() )
            self.f.close()
        print u''

    def writeLog(self, s):
        print s

    # Support

    def indent(self):
        if self.printerState[u'p'] == True:
          return u'  '
        else:
            return u''

    def startC(self):
        if self.printerState[u'c'] == False:
            self.printerState[u'c'] = True
        return u'\n<chapter number="' + self.currentC + u'"'

    def stopC(self):
        if self.printerState[u'c'] == True:
            self.printerState[u'c'] = False
            return u' style="c" />'
        else:
            return u''

    def startP(self):
        if self.printerState[u'p'] == False:
            self.printerState[u'p'] = True
        return u'\n<para style="p">'

    def stopP(self):
        if self.printerState[u'p'] == True:
            self.printerState[u'p'] = False
            return u'</para>'
        else:
            return u''

    def startQ(self, n):
        if self.printerState[u'q'] == False:
            self.printerState[u'q'] = True
        return u'\n<para style="q' + str(n) + u'">'

    def startQM(self, n):
        if self.printerState[u'q'] == False:
            self.printerState[u'q'] = True
        return u'\n<para style="qm' + str(n) + u'">'

    def stopQ(self):
        if self.printerState[u'q'] == True:
            self.printerState[u'q'] = False
            return u'</para>'
        else:
            return u''

    def startLI(self, n):
        if self.printerState[u'li'] == False:
            self.printerState[u'li'] = True
        return u'\n<para style="li' + str(n) + u'">'

    def stopLI(self):
        if self.printerState[u'li'] == True:
            self.printerState[u'li'] = False
            return u'</para>'
        else:
            return u''

    def startCell(self, style, align):
        if self.printerState[u'cell'] == False:
            self.printerState[u'cell'] = True
            return u'\n    <cell style="' + style + u'" align="' + align + u'">'
        else:
            return u''

    def stopCell(self):
        if self.printerState[u'cell'] == True:
            self.printerState[u'cell'] = False
            return u'</cell>'
        else:
            return u''

    def startRow(self):
        if self.printerState[u'row'] == False:
            self.printerState[u'row'] = True
        return u'\n  <row style="tr">'

    def stopRow(self):
        if self.printerState[u'row'] == True:
            self.printerState[u'row'] = False
            return u'\n  </row>'
        else:
            return u''

    def startTable(self):
        if self.printerState[u'table'] == False:
            self.printerState[u'table'] = True
            return u'\n<table>'
        else:
            return u''

    def stopTable(self):
        if self.printerState[u'table'] == True:
            self.printerState[u'table'] = False
            return u'\n</table>'
        else:
            return u''

    def stopAll(self):
        return self.stopC() + self.stopP() + self.stopQ() + self.stopLI() + self.stopCell() + self.stopRow() + self.stopTable()

    def stopAllToCell(self):
        return self.stopC() + self.stopP() + self.stopQ() + self.stopLI() + self.stopCell()

    def escape(self, s):
        return s

    def renderTEXT(self, token):    self.f.write( self.escape(token.value) )

    def renderH(self, token):       self.book = token.getValue();
    def renderMT(self, token):      self.f.write( self.stopAll() + u'\n<para style="mt">' + token.value.upper() + u'</para>' )
    def renderMT1(self, token):     self.f.write( self.stopAll() + u'\n<para style="mt1">' + token.value.upper() + u'</para>' )
    def renderMT2(self, token):     self.f.write( self.stopAll() + u'\n<para style="mt2">' + token.value.upper() + u'</para>' )
    def renderMT3(self, token):     self.f.write( self.stopAll() + u'\n<para style="mt3">' + token.value.upper() + u'</para>' )
    def renderMT4(self, token):     self.f.write( self.stopAll() + u'\n<para style="mt4">' + token.value.upper() + u'</para>' )
    def renderMT5(self, token):     self.f.write( self.stopAll() + u'\n<para style="mt5">' + token.value.upper() + u'</para>' )
    def renderMS(self, token):      self.f.write( self.stopAll() + u'\n<para style="ms">' + token.value + u'</para>' )
    def renderMS1(self, token):     self.f.write( self.stopAll() + u'\n<para style="ms1">' + token.value + u'</para>' )
    def renderMS2(self, token):     self.f.write( self.stopAll() + u'\n<para style="ms2">' + token.value + u'</para>' )
    def renderMS3(self, token):     self.f.write( self.stopAll() + u'\n<para style="ms3">' + token.value + u'</para>' )
    def renderMS4(self, token):     self.f.write( self.stopAll() + u'\n<para style="ms4">' + token.value + u'</para>' )
    def renderMS5(self, token):     self.f.write( self.stopAll() + u'\n<para style="ms5">' + token.value + u'</para>' )
    def renderP(self, token):       self.f.write( self.stopAll() + self.startP() )
    def renderB(self, token):       self.f.write( self.stopAll() + u'\n<para style="b" />')
    def renderS(self, token):       self.f.write( self.stopAll() + u'\n\n<para style="s">' + token.value + u'</para>' )
    def renderS1(self, token):      self.f.write( self.stopAll() + u'\n\n<para style="s1">' + token.value + u'</para>' )
    def renderS2(self, token):      self.f.write( self.stopAll() + u'\n\n<para style="s2">' + token.value + u'</para>' )
    def renderS3(self, token):      self.f.write( self.stopAll() + u'\n\n<para style="s3">' + token.value + u'</para>' )
    def renderS4(self, token):      self.f.write( self.stopAll() + u'\n\n<para style="s4">' + token.value + u'</para>' )
    def renderS5(self, token):      self.f.write( self.stopC() + u'\n<note caller="u" style="s5"></note>' )
    def renderC(self, token):       self.currentC = token.value; self.currentV = u'0'; self.f.write( self.stopAll() + self.startC() )
    def renderCAS(self, token):     self.f.write( u' altnumber="' )
    def renderCAE(self, token):     self.f.write( u'"' )
    def renderCL(self, token):      self.f.write( self.stopAll() + u'\n\n<para style="cl">' + token.value + u'</para>' )
    def renderV(self, token):       self.currentV = token.value; self.f.write( self.stopC() + u'\n' + self.indent() + u'<verse number="' + token.value + u'" style="v" />' )
    def renderQ(self, token):       self.renderQ1(token)
    def renderQ1(self, token):      self.f.write( self.stopAll() + self.startQ(1) )
    def renderQ2(self, token):      self.f.write( self.stopAll() + self.startQ(2) )
    def renderQ3(self, token):      self.f.write( self.stopAll() + self.startQ(3) )
    def renderQ4(self, token):      self.f.write( self.stopAll() + self.startQ(4) )
    def renderQA(self, token):      self.f.write( self.stopAll() + u'\n<para style="qa">' + token.value + u'</para>' )
    def renderQAC(self, token):     self.f.write( self.stopC() + u'\n<char style="qac">' + self.escape(token.value) + u'</char>' )
    def renderQC(self, token):      self.f.write( self.stopAll() + u'\n<para style="qc">' + token.value + u'</para>' )
    def renderQM(self, token):      self.renderQM1(token)
    def renderQM1(self, token):     self.f.write( self.stopAll() + self.startQM(1) )
    def renderQM2(self, token):     self.f.write( self.stopAll() + self.startQM(2) )
    def renderQM3(self, token):     self.f.write( self.stopAll() + self.startQM(3) )
    def renderQR(self, token):      self.f.write( self.stopAll() + u'\n<para style="qr">' + token.value + u'</para>' )
    def renderQSS(self, token):     self.f.write( self.stopC() + u'\n<char style="qs">' )
    def renderQSE(self, token):     self.f.write( self.stopC() + u'</char>' )
    def renderQTS(self, token):     self.f.write( self.stopC() + u'<char style="qt">' )
    def renderQTE(self, token):     self.f.write( self.stopC() + u'</char>' )
    def renderNB(self, token):      self.f.write( self.stopC() + u'\n<char style="nb">' + self.indent() + u'</char>' )
    def renderLI(self, token):      self.renderLI1(token)
    def renderLI1(self, token):     self.f.write( self.stopAll() + self.startLI(1) )
    def renderLI2(self, token):     self.f.write( self.stopAll() + self.startLI(2) )
    def renderLI3(self, token):     self.f.write( self.stopAll() + self.startLI(3) )
    def renderLI4(self, token):     self.f.write( self.stopAll() + self.startLI(4) )
    def renderPBR(self, token):     self.f.write( self.stopC() + u'\n' )

    def renderBDS(self, token):     self.f.write( self.stopC() + u'<char style="bd">' )
    def renderBDE(self, token):     self.f.write( self.stopC() + u'</char>' )
    def renderBDITS(self, token):   self.f.write( self.stopC() + u'<char style="bdit">' )
    def renderBDITE(self, token):   self.f.write( self.stopC() + u'</char>' )
    def renderEMS(self, token):     self.f.write( self.stopC() + u'<char style="em">' )
    def renderEME(self, token):     self.f.write( self.stopC() + u'</char>' )
    def renderITS(self, token):     self.f.write( self.stopC() + u'<char style="it">' )
    def renderITE(self, token):     self.f.write( self.stopC() + u'</char>' )
    def renderNOS(self, token):     self.f.write( self.stopC() + u'<char style="no">' )
    def renderNOE(self, token):     self.f.write( self.stopC() + u'</char>' )
    def renderSCS(self, token):     self.f.write( self.stopC() + u'<char style="sc">' )
    def renderSCE(self, token):     self.f.write( self.stopC() + u'</char>' )

    def renderFS(self, token):      self.f.write( self.stopC() + u'\n<note caller="+" style="f">' )
    def renderFE(self, token):      self.f.write( self.stopC() + u'\n</note>' )
    def renderFR(self, token):      self.f.write( self.stopC() + u'\n  <char style="fr">' + self.escape(token.value) + u'</char>' )
    def renderFT(self, token):      self.f.write( self.stopC() + u'\n  <char style="ft">' + self.escape(token.value) + u'</char>' )
    def renderFQ(self, token):      self.f.write( self.stopC() + u'\n  <char style="fq">' + self.escape(token.value) + u'</char>' )
    def renderFQA(self, token):     self.f.write( self.stopC() + u'\n  <char style="fqa">' + self.escape(token.value) + u'</char>' )

    def renderXS(self, token):      self.f.write( self.stopC() + u'\n<note caller="-" style="x">' )
    def renderXE(self, token):      self.f.write( self.stopC() + u'\n</note>' )
    def renderXO(self, token):      self.f.write( self.stopC() + u'\n  <char style="xo">' + self.escape(token.value) + u'</char>' )
    def renderXT(self, token):      self.f.write( self.stopC() + u'\n  <char style="xt">' + self.escape(token.value) + u'</char>' )

    def renderTR(self, token):      self.f.write( self.stopAllToCell() + self.stopRow() + self.startTable() + self.startRow() )
    def renderTH1(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'th1', u'start') )
    def renderTH2(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'th2', u'start') )
    def renderTH3(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'th3', u'start') )
    def renderTH4(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'th4', u'start') )
    def renderTH5(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'th5', u'start') )
    def renderTH6(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'th6', u'start') )
    def renderTHR1(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'thr1', u'end') )
    def renderTHR2(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'thr2', u'end') )
    def renderTHR3(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'thr3', u'end') )
    def renderTHR4(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'thr4', u'end') )
    def renderTHR5(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'thr5', u'end') )
    def renderTHR6(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'thr6', u'end') )
    def renderTC1(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'tc1', u'start') )
    def renderTC2(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'tc2', u'start') )
    def renderTC3(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'tc3', u'start') )
    def renderTC4(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'tc4', u'start') )
    def renderTC5(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'tc5', u'start') )
    def renderTC6(self, token):     self.f.write( self.stopAllToCell() + self.startCell(u'tc6', u'start') )
    def renderTCR1(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'tcr1', u'end') )
    def renderTCR2(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'tcr2', u'end') )
    def renderTCR3(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'tcr3', u'end') )
    def renderTCR4(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'tcr4', u'end') )
    def renderTCR5(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'tcr5', u'end') )
    def renderTCR6(self, token):    self.f.write( self.stopAllToCell() + self.startCell(u'tcr6', u'end') )

    def renderUnknown(self, token):
        if token.value == 'v' :
            self.currentV = str(int(self.currentV)+1)
        print u'     Error: ' + self.book + u' ' + self.currentC + u':' + self.currentV + u' - Unknown Token: \\' + self.escape(token.value)