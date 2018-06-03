# -*- coding: utf-8 -*-
#

from __future__ import print_function, unicode_literals
import codecs
import datetime

import usfm_tools.support.abstractRenderer as abstractRenderer
import usfm_tools.support.books

#
#   Renders using Lout (TeX alternative)
#

class LoutRenderer(abstractRenderer.AbstractRenderer):

    def __init__(self, inputDir, outputFilename):
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilename = outputFilename
        self.inputDir = inputDir
        # Position
        self.cb = ''    # Current Book
        self.cc = '001'    # Current Chapter
        self.cv = '001'    # Currrent Verse
        self.indentFlag = False
        self.bookName = ''
        self.inChapter = False
        self.inSections = False
        self.inSection = False
        self.startTextType = 'drop' # Or nomal or smallcaps
        self.inDropCap = False
        self.inPoetry = False
        self.registerForNextText = ''
        self.inD = False
        self.afterLord = False

    def render(self):
        self.f = codecs.open(self.outputFilename, 'w', 'utf_8_sig')
        self.f.write(r"""@Include { oebbook }
@Book
    @Title {}
    @Author {}
    @Edition {}
    @Publisher {}
    @BeforeTitlePage {}
    @OnTitlePage {}
    @AfterTitlePage {}
    @AtEnd {}
    @InitialLanguage { English }
    @PageOrientation { Portrait }
    @PageHeaders { Titles }
    @ColumnNumber { 1 }
    @FirstPageNumber { 1 }
    @IntroFirstPageNumber { 1 }
    @OptimizePages { No }
    @GlossaryText { @Null }
    @IndexText { @Null }
    @IndexAText { @Null }
    @IndexBText { @Null }
//

""".encode('utf-8'))
        self.loadUSFM(self.inputDir)
        self.run()
        self.f.close()

    def writeLog(self, s):
        print(s)

    def write(self, unicodeString):
        self.f.write(unicodeString + '\n')

    #   SUPPORT
    #
    #
    def escape(self, s, upper=False):
        if upper:
            t = s.upper()
        else:
            t = s
        t = t.replace(u'“', '{@Char quotedblleft}').replace(u'”', '{@Char quotedblright}').replace(u'—', '{@Char emdash}').replace(u'‘', '{@Char quoteleft}').replace(u'’', '{@Char quoteright}').replace(u'"', '{@Char quotedbl}')
        #t = t.replace(u'"', '{@Char quotedbl}')
        #t = t.replace(u'’', '{@Char quoteright}')
        return t

    def close(self):
        self.closeChapter()

    def closeChapter(self):
        self.closeSections()
        if self.inChapter:          # We need to close previous chapter (ie Book)
            self.inChapter = False
            self.write(u'\n@End @Chapter\n')

    def closeSections(self):
        self.closeSection()
        if self.inSections:          # We need to close previous section
            self.inSections = False
            self.write(u'\n@EndSections\n')

    def closeSection(self):
        self.closeDropCap()
        self.closePoetry()
        if self.inSection:          # We need to close previous section
            self.inSection = False
            self.write(u'\n@End @Section\n')

    def closeDropCap(self):
        if self.inDropCap:          # We need to close previous section
            self.inDropCap = False
            self.write(u'}')

    def closeD(self):
        if self.inD:          # We need to close the D
            self.inD = False
            self.write(u'}}')

    def closePoetry(self):
        if self.inPoetry:
            self.inPoetry = False

    def writeIndent(self, level):
        self.closeD()
        self.closeDropCap()
        if not self.inPoetry:
            self.write(u'\n@DP ')
            self.inPoetry = True
        else:
            self.write(u'\n@LLP ')
        self.write(u'~ ~ ~ ~' * level)

    def formatText(self, text):
        t = text
        if len(t) < 60: self.startTextType = 'normal'  # Don't do funky things with short first lines.

        # Handle poetry lines that want to wrap
        if self.inPoetry and len(t) > 60:
            n = t.find(u' ', 50) # Give us buffer
            t = t[:n] + '\n@LLP ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ' + t[n:]

        if self.cb == '019': self.startTextType = 'normal'  # Don't do funky things with Psalms.
        if self.startTextType == 'drop':
            self.inDropCap = True
            self.write(t[0] + ' @DropCapTwo {')
            self.write(self.escape(self.smallCapText(t[1:])))
        elif self.startTextType == 'smallcaps':
            self.write(self.escape(self.smallCapText(t)))
        else:
            if self.afterLord and not (t[0] == "'" or t[0] == ',' or t[0] == '?'):
                self.afterLord = False
                t = ' ' + t
            self.write(self.escape(self.addNextText(t)))
        self.write(u' ')
        self.startTextType = 'normal'

    def addNextText(self, text):
        t = text
        if not self.registerForNextText == '':
            try:
                i = t.index(u' ')
                t = t[:i] + self.registerForNextText + ' ' + t[i+1:]
            except Exception:
                t = self.registerForNextText + t
            self.registerForNextText = ''
        return t

    def smallCapText(self, s):
         i = 0
         while i < len(s):
             if i < 60:  #we are early, look for comma
                 if s[i] == ',' or s[i] == ';' or s[i] == '.' or s[i] == '—':
                     return '{@S {' + self.addNextText(s[:i+1]) + '}} ' + s[i+1:]
                 i = i + 1
             else: # look for space
                 if s[i] == ' ':
                     return '{@S {' + self.addNextText(s[:i]) + '}}' + s[i:]
                 i = i + 1
         return self.addNextText(s)

    def newPara(self, indent = True, outdent=False):
        # Don't indent at start of books
        if self.startTextType == 'drop': indent = False
        if self.startTextType == 'smallcaps': indent = False

        self.closeDropCap()
        if self.inPoetry:
            self.closePoetry()
            self.write(u'\n\n@DP ~\n')
        else:
            if outdent:
                self.write(u'\n\noutdent @Break { @PP }\n')
            elif indent:
                self.write(u'\n\n@PP\n')
            else:
                self.write(u'\n\n@LP\n')

    #   TOKENS
    #
    #
    def renderID(self, token):
        self.cb = books.bookKeyForIdValue(token.value)
        self.indentFlag = False
        self.closeChapter()
    def renderIDE(self, token):
        pass
    def renderSTS(self, token):
        pass
    def renderH(self, token):
        self.close()
        self.bookname = token.value
        self.write(u'\n@Chapter @Title { ' + self.escape(token.value) + ' } @RunningTitle { ' + self.bookname + ' } @Begin')
        self.inChapter = True
    def renderMT(self, token):
        self.write(u'\n@Display  { 21p } @Font { ' + self.escape(token.value, upper=True) + '}')
        self.startTextType = 'drop'
    def renderMT2(self, token):
        self.write(u'\n@Display  { 13p } @Font { ' + self.escape(token.value, upper=True) + '}')
    def renderMT3(self, token):
        self.write(u'\n@Display  { 13p } @Font { ' + self.escape(token.value, upper=True) + '}')
    def renderMS(self, token):
        self.closeSection()
        if not self.inSections: self.write(u'@BeginSections '); self.inSections = True
        self.write(u'\n@Section @Title {' + self.escape(token.value) + '} @Begin @LP\n')
        self.inSection = True
        if self.startTextType == 'normal': self.startTextType = 'smallcaps'
    def renderMS2(self, token):
        self.write(u'\n@Display @Heading {' + self.escape(token.value) + '}\n')
    def renderP(self, token):
        self.newPara()
    def renderPI(self, token):
        self.newPara(outdent = True)
    def renderS(self, token):
        self.closePoetry();
        self.closeDropCap();
        self.write(u'\n@DP @CNP @Display @Heading {' + self.escape(token.value) + '}\n')
    def renderS2(self, token):
        self.closeDropCap();
        self.write(u'\n\n@DP\n')
    def renderC(self, token):
        self.cc = token.value.zfill(3)
        self.registerForNextText = ' {@OuterNote { 10.5p @Font {@B ' + token.value + '}}}'
    def renderV(self, token):
        self.cv = token.value.zfill(3)
        if not self.cv == '001':   self.registerForNextText = ' {@OuterNote { 8p @Font {' + token.value + '}}}'
    def renderTEXT(self, token):    self.formatText(token.value)
    def renderQ(self, token):       self.writeIndent(1)
    def renderQ1(self, token):      self.writeIndent(1)
    def renderQ2(self, token):      self.writeIndent(2)
    def renderQ3(self, token):      self.writeIndent(3)
    def renderNB(self, token):      self.newPara(indent = False)
    def renderB(self, token):       self.newPara(indent = False); self.inPoetry = True
    def renderFS(self, token):      self.write(u'@FootNote { ')
    def renderFE(self, token):      self.write(u' }')
    def renderFP(self, token):      self.newPara(indent = False)
    def renderIS(self, token):      self.write(u'{@I {')
    def renderIE(self, token):      self.write(u'}}')
    def renderNDS(self, token):     self.write(u'{@S {')
    def renderNDE(self, token):     self.write(u'}}'); self.afterLord = True
    def renderPBR(self, token):     self.write(u'@LLP ')
    def renderSCS(self, token):     self.write(u'{@B {')
    def renderSCE(self, token):     self.write(u'}}')
    def renderD(self, token):       self.write(u'{@I {'); self.inD = True
