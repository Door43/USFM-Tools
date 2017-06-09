# -*- coding: utf-8 -*-
#

import abstractRenderer
import codecs
import datetime
import books

from parseUsfm import UsfmToken

#
#   Simplest renderer. Ignores everything except ascii text.
#

class SingleHTMLRenderer(abstractRenderer.AbstractRenderer):
    def __init__(self, inputDir, outputFilename):
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilename = outputFilename
        self.inputDir = inputDir
        # Position
        self.cb = u''    # Current Book
        self.cc = u'001'    # Current Chapter
        self.cv = u'001'    # Current Verse
        self.indentFlag = False
        self.bookName = u''
        self.chapterLabel = u'Chapter'
        self.lineIndent = 0
        self.footnoteFlag = False
        self.fqaFlag = False
        self.footnotes = {}
        self.footnote_id = u''
        self.footnote_num = 1
        self.footnote_text = u''

    def render(self):
        self.loadUSFM(self.inputDir)
        self.f = codecs.open(self.outputFilename, 'w', 'utf_8_sig')
        self.run()
        self.writeFootnotes()
        self.f.write('</body></html>')
        self.f.close()

    def writeHeader(self):
        h = u"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8"></meta>
            <title>""" + self.bookName + u"""</title>
            <style media="all" type="text/css">
            .indent-0 {
                margin-left:0em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .indent-1 {
                margin-left:0em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .indent-2 {
                margin-left:1em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .indent-3 {
                margin-left:2em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .c-num {
                color:gray;
            }
            .v-num {
                color:gray;
            }
            .tetragrammaton {
                font-variant: small-caps;
            }
            .footnotes {
                font-size: 0.8em;
            }
            .footnotes-hr {
                width: 90%;
            }
            </style>

        </head>
        <body>
        <h1>""" + self.bookName + u"""</h1>
        """
        self.f.write(h.encode('utf-8'))

    def startLI(self):
        self.lineIndent += 1
        return ur'<ul> '

    def stopLI(self):
        if self.lineIndent < 1:
            return u''
        else:
            self.lineIndent -= 1
            return ur'</ul>'

    def escape(self, s):
        return s.replace(u'~',u'&nbsp;')

    def write(self, unicodeString):
        self.f.write(unicodeString.replace(u'~', u' '))

    def writeIndent(self, level):
        if self.indentFlag:
            self.write(self.stopIndent())  # always close the last indent before starting a new one
        if level > 0:
            self.indentFlag = True
            self.write(u'\n<p class="indent-' + str(level) + u'">\n')
            self.write(u'&nbsp;' * (level * 4))  # spaces for PDF since we can't style margin with css

    def stopIndent(self):
        if self.indentFlag:
            self.indentFlag = False
            return u'\n</p>\n'
        else:
            return u''

    def renderID(self, token):
        self.writeFootnotes()
        self.cb = books.bookKeyForIdValue(token.value)
        self.chapterLabel = u'Chapter'
        self.write(self.stopIndent())
        #self.write(u'\n\n<span id="' + self.cb + u'"></span>\n')

    def renderH(self, token):
        self.bookName = token.value
        self.writeHeader()

    def renderTOC2(self, token):
        if not self.bookName:
            self.bookName = token.value
            self.writeHeader()

    def renderMT(self, token):
        return  #self.write(u'\n\n<h1>' + token.value + u'</h1>') # removed to use TOC2

    def renderMT2(self, token):
        self.write(u'\n\n<h2>' + token.value + u'</h2>')

    def renderMT3(self, token):
        self.write(u'\n\n<h2>' + token.value + u'</h2>')

    def renderMS1(self, token):
        self.write(u'\n\n<h3>' + token.value + u'</h3>')

    def renderMS2(self, token):
        self.write(u'\n\n<h4>' + token.value + u'</h4>')

    def renderP(self, token):
        self.write(self.stopIndent())
        self.write(self.stopLI() + u'\n\n<p>')

    def renderPI(self, token):
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.writeIndent(2)

    def renderM(self, token):
        self.write(self.stopIndent())
        self.write(u'\n\n<p>')

    def renderS1(self, token):
        self.write(self.stopIndent())
        self.write(u'\n\n<h5>' + token.getValue() + u'</h5>')

    def renderS2(self, token):
        self.write(self.stopIndent())
        self.write(u'\n\n<p align="center">----</p>')

    def renderC(self, token):
        self.write(self.stopIndent())
        self.closeFootnote()
        self.writeFootnotes()
        self.footnote_num = 1
        self.cc = token.value.zfill(3)
        self.write(self.stopLI() + u'\n\n<h2 id="{0}-ch-{1}" class="c-num">{2} {3}</h2>'
                   .format(self.cb, self.cc, self.chapterLabel, token.value))

    def renderV(self, token):
        self.closeFootnote()
        self.cv = token.value.zfill(3)
        self.write(u' <span id="{0}-ch-{1}-v-{2}" class="v-num"><sup><b>{3}</b></sup></span>'.
                   format(self.cb, self.cc, self.cv, token.value))

    def renderWJS(self, token):
        self.write(u'<span class="woc">')

    def renderWJE(self, token):
        self.write(u'</span>')

    def renderTEXT(self, token):
        self.write(u" " + self.escape(token.value) + u" ")

    def renderQ(self, token):
        self.writeIndent(1)

    def renderQ1(self, token):
        self.writeIndent(1)

    def renderQ2(self, token):
        self.writeIndent(2)

    def renderQ3(self, token):
        self.writeIndent(3)

    def renderNB(self, token):
        self.write(self.stopIndent())

    def renderB(self, token):
        self.write(self.stopLI() + u'\n\n<p class="indent-0">&nbsp;</p>')

    def renderIS(self, token):
        self.write(u'<i>')

    def renderIE(self, token):
        self.write(u'</i>')

    def renderNDS(self, token):
        self.write(u'<span class="tetragrammaton">')

    def renderNDE(self, token):
        self.write(u'</span>')

    def renderPBR(self, token):
        self.write(u'<br></br>')

    def renderSCS(self, token):
        self.write(u'<b>')

    def renderSCE(self, token):
        self.write(u'</b>')

    def renderFS(self, token):
        self.closeFootnote()
        self.footnote_id = u'fn-{0}-{1}-{2}-{3}'.format(self.cb, self.cc, self.cv, self.footnote_num)
        self.write(u'<span id="ref-{0}"><sup><i>[<a href="#{0}">{1}</a>]</i></sup></span>'.format(self.footnote_id, self.footnote_num))
        self.footnoteFlag = True
        text = token.value
        if text.startswith(u'+ '):
            text = text[2:]
        elif text.startswith(u'+'):
            text = text[1:]
        self.footnote_text = text

    def renderFT(self, token):
        self.footnote_text += token.value

    def renderFE(self, token):
        self.closeFootnote()

    def renderFP(self, token):
        self.write(u'<br />')

    def renderQSS(self, token):
        self.write(u'<i>')

    def renderQSE(self, token):
        self.write(u'</i>')

    def renderEMS(self, token):
        self.write(u'<i>')

    def renderEME(self, token):
        self.write(u'</i>')

    def renderE(self, token):
        self.write(self.stopIndent())
        self.write(u'\n\n<p>' + token.value + '</p>')

    def renderPB(self, token):
        pass

    def renderPERIPH(self, token):
        pass

    def renderLI(self, token):
        self.f.write( self.startLI() )

    def renderLI1(self, token):
        self.f.write( self.startLI() )

    def renderLI2(self, token):
        self.f.write( self.startLI() )

    def renderLI3(self, token):
        self.f.write( self.startLI() )

    def renderS5(self, token):
        self.write(u'\n<span class="chunk-break"></span>\n')

    def render_imt1(self, token):
        self.write(u'\n\n<h2>' + token.value + u'</h2>')

    def render_imt2(self, token):
        self.write(u'\n\n<h3>' + token.value + u'</h3>')

    def render_imt3(self, token):
        self.write(u'\n\n<h4>' + token.value + u'</h4>')

    def renderCL(self, token):
        self.chapterLabel = token.value

    def renderQR(self, token):
        self.write(u'')

    def renderFQA(self, token):
        self.footnote_text += u'<i>'+token.value
        self.fqaFlag = True

    def renderFQAE(self, token):
        self.footnote_text += u'</i>'+token.value
        self.fqaFlag = False

    def closeFootnote(self):
        if self.footnoteFlag:
            self.footnoteFlag = False
            if self.fqaFlag:
                self.renderFQAE(UsfmToken(u''))
            self.footnotes[self.footnote_id] = {
                'text': self.footnote_text,
                'book': self.cb,
                'chapter': self.cc,
                'verse': self.cv,
                'footnote': self.footnote_num
            }
            self.footnote_num += 1
            self.footnote_text = u''
            self.footnote_id = u''

    def writeFootnotes(self):
        fkeys = self.footnotes.keys()
        if len(fkeys) > 0:
            self.write(u'<div class="footnotes">')
            self.write(u'<hr class="footnotes-hr"></hr>')
            for fkey in sorted(fkeys):
                footnote = self.footnotes[fkey]
                self.write(u'<div id="{0}" class="footnote">{1}:{2} <sup><i>[<a href="#ref-{0}">{5}</a>]</i></sup><span class="text">{6}</span></div>'.
                           format(fkey, footnote['chapter'].lstrip('0'), footnote['verse'].lstrip('0'), footnote['chapter'], footnote['verse'],\
                                  footnote['footnote'], footnote['text']))
            self.write(u'</div>')
        self.footnotes = {}

