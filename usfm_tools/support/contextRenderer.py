# -*- coding: utf-8 -*-
#

from __future__ import print_function, unicode_literals
import codecs
import datetime

import usfm_tools.support.abstractRenderer as abstractRenderer

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
        self.printerState = {'li': False, 'd': False}
        self.smallCapSections = True  # Sometimes we don't want to do this, like for Psalms
        self.justDidLORD = False
        self.justDidNB = False
        self.doNB = False
        self.narrower = False
        self.doChapterOrVerse = ''
        self.smallcaps = False

    def render(self):
        self.f = codecs.open(self.outputFilename, 'w', 'utf_8_sig')
        self.loadUSFM(self.inputDir)
        self.f.write(r"""
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
        print(s.encode('ascii', 'ignore'))


    #
    #   Support
    #

    def startNarrower(self, n):
        s = '}' if self.narrower else '\n\\blank[medium] '
        self.narrower = True
        s = s + '\n\\noindentation \\Q{' + str(n) + '}{'
        self.doNB = True
        return s

    def stopNarrower(self):
        s = '}\n\\blank[medium] ' if self.narrower else ''
        self.narrower = False
        return s

    def escapeText(self, s):
        return ( s.replace('&', '\\&').replace('%', '\\%')
                  .replace('#', '\\#').replace('$', '\\$')
                  .replace('_', '\\_').replace('{', '\\{')
                  .replace('}', '\\}') )

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
                 if s[i] == ',' or s[i] == ';' or s[i] == '(' or s[i:i+3] == 'and':
                     return '{\sc ' + s[:i+1] + '}' + s[i+1:]
             else: # look for space
                 if s[i] == ' ':
                     return '{\sc ' + s[:i] + '}' + s[i:]
             i = i + 1
         return '{\sc ' + s + '}'

    def startLI(self):
        if self.printerState['li'] == False:
            self.printerState['li'] = True
            #return '\startitemize \item '
            return r'\startexdent '
        else:
            #return '\item '
            return r'\par '

    def stopLI(self):
        if self.printerState['li'] == False:
            return ''
        #elif self.printerState['li2'] == False:
            #return ''
        #elif self.printerState['li3'] == False:
            #return ''
        else:
            self.printerState['li'] = False
            #return '\stopitemize'
            return r'\stopexdent '

    def startD(self):
        if self.printerState['d'] == False:
            self.printerState['d'] = True
        return r'\par {\startalignment[center] \em '

    def stopD(self):
        if self.printerState['d'] == False:
            return ''
        else:
            self.printerState['d'] = False
            return r'\stopalignment }'

    def newLine(self):
        s = '\n\\par \n'
        if self.doNB:
            self.doNB = False
            self.justDidNB = True
            s = s + r'\noindentation '
        elif self.justDidNB:
            self.justDidNB = False
            s = s + r'\indentation '
        return s


    #
    #   Tokens
    #

    def renderID(self, token):      self.f.write( self.stopNarrower() + r"\marking[RAChapter]{ } \marking[RABook]{ } \marking[RASection]{ }" )
    def renderH(self, token):       self.f.write( '\n\n\\RAHeader{' + self.escapeText(token.value) + '}\n')
    def renderTOC1(self, token):      self.f.write( self.stopLI() + self.stopNarrower() + '\n\\TOC1{' + token.value + '}\n')
    def renderTOC2(self, token):      self.f.write( self.stopLI() + self.stopNarrower() + '\n\\TOC2{' + token.value + '}\n')
    def renderTOC3(self, token):      self.f.write( self.stopLI() + self.stopNarrower() + '\n\\TOC3{' + token.value + '}\n')
    def renderMT(self, token):      self.f.write( self.stopLI() + self.stopNarrower() + '\n\\MT{' + token.value + '}\n')
    def renderMT2(self, token):     self.f.write( self.stopLI() + self.stopNarrower() + '\n\\MTT{' + token.value + '}\n')
    def renderMS(self, token):      self.markForSmallCaps() ; self.f.write(self.stopNarrower() + '\n\\MS{' + self.escapeText(token.value) + '}\n') ; self.doNB = True
    def renderMS2(self, token):     self.doNB = True; self.markForSmallCaps() ; self.f.write( self.stopNarrower() + '\n\\MSS{' + self.escapeText(token.value) + '}' + self.newLine() )
    def renderP(self, token):       self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + self.newLine() )
    def renderB(self, token):       self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + '\\blank \n' )
    def renderS(self, token):       self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() +  '\n\\blank[big] ' + '\n\\MSS{' + self.escapeText(token.value) + '}' + self.newLine() ) ; self.doNB = True
    def renderS2(self, token):      self.doNB = True; self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + '\n\\blank[big] ' + '\n\\MSS{' + self.escapeText(token.value) + '}' + self.newLine() )
    def renderS5(self, token):      self.doNB = True; self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + '\n\\blank[big] ' + '\n\\MSS{' + self.escapeText(token.value) + '}' + self.newLine() )
    def renderC(self, token):
        self.doChapterOrVerse = r'\C{' + self.escapeText(token.value) + '}'
        self.f.write( ' ' )
    def renderV(self, token):
        if not token.value == '1':
            self.doChapterOrVerse =  r'\V{' + self.escapeText(token.value) + '}'
        self.f.write( ' ' )
    def renderWJS(self, token):     self.f.write( " " )
    def renderWJE(self, token):     self.f.write( " " )
    def renderTEXT(self, token):
        s = self.escapeText(token.value)
        if self.smallcaps and not self.doChapterOrVerse == '':
            s = self.renderSmallCaps(s)
            s = self.doChapterOrVerse + s
            self.doChapterOrVerse = ''
        elif not self.doChapterOrVerse == '':
            i = s.find(' ')
            if i == -1:
                # No space found - try end
                i = len(s)
            s = s[:i] + self.doChapterOrVerse + s[i+1:]
            self.doChapterOrVerse = ''
        elif self.smallcaps:
            s = self.renderSmallCaps(s)
        if self.justDidLORD:
            if s[0].isalpha():
                s = ' ' + s
            self.justDidLORD = False
        self.f.write(s)
        self.f.write(' ')
    def renderQ(self, token):       self.renderQ1(token)
    def renderQ1(self, token):      self.f.write( self.stopD() + self.stopLI() + self.startNarrower(1) )
    def renderQ2(self, token):      self.f.write( self.stopD() + self.stopLI() + self.startNarrower(2) )
    def renderQ3(self, token):      self.f.write( self.stopD() + self.stopLI() + self.startNarrower(3) )
    def renderNB(self, token):      self.doNB = True ; self.f.write( self.stopD() + self.stopLI() + self.stopNarrower() + '\\blank[medium] ' + self.newLine() )
    def renderFS(self, token):      self.f.write( r'\footnote{' )
    def renderFE(self, token):      self.f.write( '} ' )
    def renderFP(self, token):      self.f.write( self.newLine() )
    def renderIS(self, token):      self.f.write( r'{\em ' )
    def renderIE(self, token):      self.f.write( '} ' )
    def renderBDS(self, token):     self.f.write( r'{\bf ')
    def renderBDE(self, token):     self.f.write( '} ')
    def renderBDITS(self, token):   self.f.write( r'{\bs ')
    def renderBDITE(self, token):   self.f.write( '} ')
    def renderADDS(self, token):    self.f.write( r'{\em ' )
    def renderADDE(self, token):    self.f.write( '} ' )
    def renderNDS(self, token):     self.f.write( r'{\sc ' )
    def renderNDE(self, token):     self.justDidLORD = True; self.f.write( '}' )
    def renderLI(self, token):      self.f.write( self.startLI() )
    def renderLI1(self, token):      self.f.write( self.startLI() )
    def renderLI2(self, token):      self.f.write( self.startLI() )
    def renderLI3(self, token):      self.f.write( self.startLI() )
    def renderD(self, token):       self.f.write( self.startD() )
    def renderSP(self, token):      self.f.write( self.startD() )
    def renderPBR(self, token):     self.f.write( ' \\\\ ' )
    def renderFR(self, token):      self.f.write( ' ' + self.escapeText(token.value) + ' ' )
    def renderFRE(self, token):     self.f.write( ' ' )
    def renderFK(self, token):      self.f.write( ' ' + self.escapeText(token.value) + ' ' )
    def renderFT(self, token):      self.f.write( ' ' + self.escapeText(token.value) + ' ' )
    def renderPI(self, token):      self.renderQ(token)

    def renderQSS(self, token):      return
    def renderQSE(self, token):      return

    def render_is1(self, token):    self.renderS(token)
    def render_imt1(self, token):   self.f.write( self.stopLI() + self.stopNarrower() + '\n\\IMT1{' + token.value + '}\n')
    def render_imt2(self, token):   self.f.write( self.stopLI() + self.stopNarrower() + '\n\\IMT2{' + token.value + '}\n')
    def render_imt3(self, token):   self.f.write( self.stopLI() + self.stopNarrower() + '\n\\IMT3{' + token.value + '}\n')
    def render_ip(self, token):     self.renderP(token)
    def render_iot(self, token):    self.renderQ(token)
    def render_io1(self, token):    self.renderQ2(token)
    def render_io2(self, token):    self.renderQ2(token)

    closeTeXt = r"""
    \stoptext
    """
