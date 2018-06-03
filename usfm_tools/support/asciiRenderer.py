# -*- coding: utf-8 -*-
#

from __future__ import print_function, unicode_literals
import codecs

import usfm_tools.support.abstractRenderer as abstractRenderer

#
#   Simplest renderer. Ignores everything except ascii text.
#

class ASCIIRenderer(abstractRenderer.AbstractRenderer):

    def __init__(self, inputDir, outputFilename):
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilename = outputFilename
        self.inputDir = inputDir
        # Flags
        self.d = False
        self.narrower = False
        self.inFootnote = False
        self.inX = False

    def render(self):
        self.f = codecs.open(self.outputFilename, 'w', 'ascii')
        self.loadUSFM(self.inputDir)
        self.run()
        self.f.close()

    def writeLog(self, s):
        print(s)

    # Support

    def startNarrower(self, n):
        s = '\n'
        if not self.narrower: s = s + '\n'
        self.narrower = True
        return s + '    ' * n

    def stopNarrower(self):
        self.narrower = False
        return ''

    def startD(self):
        self.d = True
        return ''

    def stopD(self):
        self.d = False
        return ''

    def escape(self, text):
        if self.inX or self.inFootnote:
            return ''
        t = text.replace('‘', "'")
        t = t.replace('’', "'")
        t = t.replace('“', '"')
        t = t.replace('”', '"')
        t = t.encode('ascii', 'ignore')
        return t

    # Tokens

    def renderH(self, token):       self.f.write('\n\n\n### ' + token.value + ' ###\n\n\n')
    def renderMS2(self, token):     self.f.write('\n\n[' + token.value + ']\n\n')
    def renderP(self, token):       self.f.write(self.stopD() + self.stopNarrower() + '\n\n    ')
    def renderB(self, token):       self.f.write(self.stopD() + self.stopNarrower() + '\n\n    ')
    def renderS(self, token):       self.f.write(self.stopD() + self.stopNarrower() + '\n\n    ')
    def renderS2(self, token):      self.f.write(self.stopD() + self.stopNarrower() + '\n\n    ')
    def renderC(self, token):       self.f.write(' ' )
    def renderV(self, token):       self.f.write(' ' )
    def renderTEXT(self, token):    self.f.write(self.escape(token.value))
    def renderQ(self, token):       self.f.write(self.stopD() + self.startNarrower(1))
    def renderQ1(self, token):      self.f.write(self.stopD() + self.startNarrower(1))
    def renderQ2(self, token):      self.f.write(self.stopD() + self.startNarrower(2))
    def renderQ3(self, token):      self.f.write(self.stopD() + self.startNarrower(3))
    def renderNB(self, token):      self.f.write(self.stopD() + self.stopNarrower() + "\n\n")
    def renderLI(self, token):      self.f.write(' ')
    def renderD(self, token):       self.f.write(self.startD())
    def renderSP(self, token):      self.f.write(self.startD())
    def renderNDE(self, token):     self.f.write(' ')
    def renderPBR(self, token):     self.f.write('\n')

    # Ignore...
    def renderXS(self,token):       self.inX = True
    def renderXE(self,token):       self.inX = False
    def renderFS(self,token):       self.inFootnote = True
    def renderFE(self,token):       self.inFootnote = False
