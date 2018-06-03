# -*- coding: utf-8 -*-
#

from __future__ import print_function, unicode_literals
import codecs

import usfm_tools.support.abstractRenderer as abstractRenderer

#
#   Simplest renderer. Ignores everything except ascii text.
#

class MarkdownRenderer(abstractRenderer.AbstractRenderer):

    def __init__(self, inputDir, outputFilename):
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilename = outputFilename
        self.inputDir = inputDir
        # Position
        self.currentC = 1
        self.book = ''

    def render(self):
        self.f = codecs.open(self.outputFilename, 'w', 'utf_8_sig')
        self.loadUSFM(self.inputDir)
        self.run()
        self.f.close()

    def writeLog(self, s):
        print(s)

    # Support

    def escape(self, s):
        return s

    def renderTEXT(self, token):    self.f.write(self.escape(token.value))

    def renderH(self, token):       self.book = token.getValue()
    def renderMT(self, token):      self.f.write(u'\n\n# ' + token.value.upper() + '\n\n')
    def renderMT2(self, token):     self.f.write(u'\n\n## ' + token.value.upper() + '\n\n')
    def renderMS(self, token):      self.f.write(u'\n\n' + token.value + '\n' + (u'=' * len(token.value)) + '\n\n')
    def renderMS2(self, token):     self.f.write(u'\n\n' + token.value + '\n' + (u'-' * len(token.value)) + '\n\n')
    def renderP(self, token):       self.f.write(u'\n\n')
    def renderB(self, token):       self.f.write(u'\n\n')
    def renderS(self, token):       self.f.write(u'\n\ \n')
    def renderS2(self, token):      self.f.write(u'\n\ \n')
    def renderC(self, token):       self.currentC = token.value; self.f.write(u'\n\n [' + self.book + ' ' + self.currentC + ' ] \n\n')
    def renderV(self, token):       self.f.write(u' [' + self.currentC + ':' + token.value + '] ')
    def renderQ(self, token):       self.f.write(u'\n|  ')
    def renderQ1(self, token):      self.f.write(u'\n|  ')
    def renderQ2(self, token):      self.f.write(u'\n|    ')
    def renderQ3(self, token):      self.f.write(u'\n|      ')
    def renderNB(self, token):      self.f.write(u'\n|  ')
    def renderLI(self, token):      self.f.write(u'* ')
    def renderPBR(self, token):     self.f.write(u'\n')

    def renderBDS(self, token):     self.f.write( '**')
    def renderBDE(self, token):     self.f.write( '**')
    def renderBDITS(self, token):   pass
    def renderBDITE(self, token):   pass

    def renderFS(self,token):       self.f.write(u'^[')
    def renderFE(self,token):       self.f.write(u']')
    def renderFR(self, token):      self.f.write(self.escape(token.value))
    def renderFT(self, token):      self.f.write(self.escape(token.value))
    def renderFQ(self, token):      self.f.write(self.escape(token.value))
    def renderFP(self,token):       self.f.write(u'\n\n')

    def renderXS(self,token):       self.f.write(u'^[')
    def renderXE(self,token):       self.f.write(u']')
    def renderXO(self, token):      self.f.write(self.escape(token.value))
    def renderXT(self, token):      self.f.write(self.escape(token.value))

    def render_imt1(self, token):   self.f.write(u'\n\n## ' + token.value.upper() + '\n\n')
    def render_imt2(self, token):   self.f.write(u'\n\n### ' + token.value.upper() + '\n\n')
    def render_imt3(self, token):   self.f.write(u'\n\n#### ' + token.value.upper() + '\n\n')
