# -*- coding: utf-8 -*-
#

import abstractRenderer
import codecs
import datetime

#
#   Renders to ConTeXt so we can make PDF. Main renderer for PDF of OEB
#

class ConTeXtRenderer(abstractRenderer.AbstractRenderer):

    def __init__(self, inputDir, outputFilename):
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilename = outputFilename
        self.inputDir = inputDir
        # Flags
        self.printerState = {u'li': False, u'd': False}
        self.smallCapSections = True  # Sometimes we don't want to do this, like for Psalms
        self.justDidLORD = False
        self.justDidNB = False
        self.doNB = False
        self.narrower = False
        self.doChapterOrVerse = u''
        self.smallcaps = False

    def render(self):
        self.f = codecs.open(self.outputFilename, 'w', 'utf_8_sig')
        self.loadUSFM(self.inputDir)
        self.f.write(u"""
            Document rendered on """ + datetime.date.today().strftime("%F") + r"""
            \par
            \page[right]
            \par ~
            {\midaligned {\tfc{\WORD{Table of Contents}}}}
            \par ~
            \placelist[chapter]
        """)
        self.run()
        self.f.write(self.stopNarrower() + self.closeTeXt)
        self.f.close()

    def writeLog(self, s):
        print s.encode('ascii', 'ignore')


    #
    #   Support
    #

    def startNarrower(self, n):
        s = u'}' if self.narrower else u'\n\\blank[medium] '
        self.narrower = True
        s = s + u'\n\\noindentation \\Q{' + str(n) + u'}{'
        self.doNB = True
        return s

    def stopNarrower(self):
        s = u'}\n\\blank[medium] ' if self.narrower else u''
        self.narrower = False
        return s

    def escapeText(self, s):
        return ( s.replace(u'&', u'\\&').replace(u'%', u'\\%')
                  .replace(u'#', u'\\#').replace(u'$', u'\\$')
                  .replace(u'_', u'\\_').replace(u'{', u'\\{')
                  .replace(u'}', u'\\}') )

    def markForSmallCaps(self):
        if self.smallCapSections:
             self.smallcaps = True

    def renderSmallCaps(self, s):
        if self.smallcaps == True:
            self.smallcaps = False
            return self.smallCapText(s)
        return s

    def smallCapText(self, s):
         i = 0
         while i < len(s):
             if i < 50:  #we are early, look for comma
                 if s[i] == u',' or s[i] == u';' or s[i] == u'(' or s[i:i+3] == u'and':
                     return u'{\sc ' + s[:i+1] + u'}' + s[i+1:]
             else: # look for space
                 if s[i] == ' ':
                     return u'{\sc ' + s[:i] + u'}' + s[i:]
             i = i + 1
         return u'{\sc ' + s + u'}'

    def startLI(self):
        if self.printerState[u'li'] == False:
            self.printerState[u'li'] = True
            #return u'\startitemize \item '
            return ur'\startexdent '
        else:
            #return u'\item '
            return ur'\par '

    def stopLI(self):
        if self.printerState[u'li'] == False:
            return u''
        #elif self.printerState[u'li2'] == False:
            #return u''
        #elif self.printerState[u'li3'] == False:
            #return u''
        else:
            self.printerState[u'li'] = False
            #return u'\stopitemize'
            return ur'\stopexdent '

    def startD(self):
        if self.printerState[u'd'] == False:
            self.printerState[u'd'] = True
        return u'\par {\startalignment[center] \em '

    def stopD(self):
        if self.printerState[u'd'] == False:
            return u''
        else:
            self.printerState[u'd'] = False
            return u'\stopalignment }'

    def newLine(self):
        s = u'\n\par \n'
        if self.doNB:
            self.doNB = False
            self.justDidNB = True
            s = s + ur'\noindentation '
        elif self.justDidNB:
            self.justDidNB = False
            s = s + ur'\indentation '
        return s


    #
    #   Tokens
    #

    def renderID(self, token):      self.f.write( self.stopNarrower() + ur"\marking[RAChapter]{ } \marking[RABook]{ } \marking[RASection]{ }" )
    def renderH(self, token):       self.f.write( u'\n\n\RAHeader{' + self.escapeText(token.value) + u'}\n')
    def renderTOC1(self, token):      self.f.write( self.stopLI() + self.stopNarrower() + u'\n\TOC1{' + token.value + u'}\n')
    def renderTOC2(self, token):      self.f.write( self.stopLI() + self.stopNarrower() + u'\n\TOC2{' + token.value + u'}\n')
    def renderTOC3(self, token):      self.f.write( self.stopLI() + self.stopNarrower() + u'\n\TOC3{' + token.value + u'}\n')
    def renderMT(self, token):      self.f.write( self.stopLI() + self.stopNarrower() + u'\n\MT{' + token.value + u'}\n')
    def renderMT2(self, token):     self.f.write( self.stopLI() + self.stopNarrower() + u'\n\MTT{' + token.value + u'}\n')
    def renderMS(self, token):      self.markForSmallCaps() ; self.f.write(self.stopNarrower() + u'\n\MS{' + self.escapeText(token.value) + u'}\n') ; self.doNB = True
    def renderMS2(self, token):     self.doNB = True; self.markForSmallCaps() ; self.f.write( self.stopNarrower() + u'\n\MSS{' + self.escapeText(token.value) + '}' + self.newLine() )
    def renderP(self, token):       self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + self.newLine() )
    def renderB(self, token):       self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + u'\\blank \n' )
    def renderS(self, token):       self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() +  u'\n\\blank[big] ' + u'\n\MSS{' + self.escapeText(token.value) + '}' + self.newLine() ) ; self.doNB = True
    def renderS2(self, token):      self.doNB = True; self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + u'\n\\blank[big] ' + u'\n\MSS{' + self.escapeText(token.value) + '}' + self.newLine() )
    def renderS5(self, token):      self.doNB = True; self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + u'\n\\blank[big] ' + u'\n\MSS{' + self.escapeText(token.value) + '}' + self.newLine() )
    def renderC(self, token):
        self.doChapterOrVerse = u'\C{' + self.escapeText(token.value) + u'}'
        self.f.write( u' ' )
    def renderV(self, token):
        if not token.value == u'1':
            self.doChapterOrVerse =  u'\V{' + self.escapeText(token.value) + u'}'
        self.f.write( ' ' )
    def renderWJS(self, token):     self.f.write( u" " )
    def renderWJE(self, token):     self.f.write( u" " )
    def renderTEXT(self, token):
        s = self.escapeText(token.value)
        if self.smallcaps and not self.doChapterOrVerse == u'':
            s = self.renderSmallCaps(s)
            s = self.doChapterOrVerse + s
            self.doChapterOrVerse = u''
        elif not self.doChapterOrVerse == u'':
            i = s.find(u' ')
            if i == -1:
                # No space found - try end
                i = len(s)
            s = s[:i] + self.doChapterOrVerse + s[i+1:]
            self.doChapterOrVerse = u''
        elif self.smallcaps:
            s = self.renderSmallCaps(s)
        if self.justDidLORD:
            if s[0].isalpha():
                s = u' ' + s
            self.justDidLORD = False
        self.f.write(s)
        self.f.write(u' ')
    def renderQ(self, token):       self.renderQ1(token)
    def renderQ1(self, token):      self.f.write( self.stopD() + self.stopLI() + self.startNarrower(1) )
    def renderQ2(self, token):      self.f.write( self.stopD() + self.stopLI() + self.startNarrower(2) )
    def renderQ3(self, token):      self.f.write( self.stopD() + self.stopLI() + self.startNarrower(3) )
    def renderNB(self, token):      self.doNB = True ; self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + u'\\blank[medium] ' + self.newLine() )
    def renderFS(self, token):      self.f.write( u'\\footnote{' )
    def renderFE(self, token):      self.f.write( u'} ' )
    def renderIS(self, token):      self.f.write( u'{\em ' )
    def renderIE(self, token):      self.f.write( u'} ' )
    def renderBDS(self, token):     self.f.write( u'{\\bf ')
    def renderBDE(self, token):     self.f.write( u'} ')
    def renderBDITS(self, token):   self.f.write( u'{\\bs ')
    def renderBDITE(self, token):   self.f.write( u'} ')
    def renderADDS(self, token):    self.f.write( u'{\em ' )
    def renderADDE(self, token):    self.f.write( u'} ' )
    def renderNDS(self, token):     self.f.write( u'{\sc ' )
    def renderNDE(self, token):     self.justDidLORD = True; self.f.write( u'}' )
    def renderLI(self, token):      self.f.write( self.startLI() )
    def renderLI1(self, token):      self.f.write( self.startLI() )
    def renderLI2(self, token):      self.f.write( self.startLI() )
    def renderLI3(self, token):      self.f.write( self.startLI() )
    def renderD(self, token):       self.f.write( self.startD() )
    def renderSP(self, token):      self.f.write( self.startD() )
    def renderPBR(self, token):     self.f.write( u' \\\\ ' )
    def renderFR(self, token):      self.f.write( u' ' + self.escapeText(token.value) + u' ' )
    def renderFRE(self, token):     self.f.write( u' ' )
    def renderFK(self, token):      self.f.write( u' ' + self.escapeText(token.value) + u' ' )
    def renderFT(self, token):      self.f.write( u' ' + self.escapeText(token.value) + u' ' )
    def renderPI(self, token):      self.renderQ(token)

    def renderQSS(self, token):      return
    def renderQSE(self, token):      return

    def render_is1(self, token):    self.renderS(token)
    def render_ip(self, token):     self.renderP(token)
    def render_iot(self, token):    self.renderQ(token)
    def render_io1(self, token):    self.renderQ2(token)
    def render_io1(self, token):    self.renderQ2(token)


    closeTeXt = ur"""
    \stoptext
    """
