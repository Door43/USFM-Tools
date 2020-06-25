# -*- coding: utf-8 -*-
#

from .abstractRenderer import AbstractRenderer
import codecs
import datetime
from .books import bookKeyForIdValue

from .parseUsfm import UsfmToken

#
#   Simplest renderer. Ignores everything except ascii text.
#

class SingleHTMLRenderer(AbstractRenderer):
    def __init__(self, inputDir, outputFilename):
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilename = outputFilename
        self.inputDir = inputDir
        # Position
        self.cb = u''       # Current Book
        self.cc = u'001'    # Current Chapter
        self.cv = u'001'    # Current Verse
        self.indentFlag = False
        self.bookName = u''
        self.chapterLabel = u'Chapter'
        self.listItemLevel = 0
        self.footnoteFlag = False
        self.fqaFlag = False
        self.footnotes = {}
        self.footnote_id = u''
        self.footnote_num = 1
        self.footnote_text = u''
        self.paragraphOpen = False

    def render(self):
        self.loadUSFM(self.inputDir)
        self.f = codecs.open(self.outputFilename, 'w', 'utf_8_sig')
        self.writeHeader()
        self.run()
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.write(self.stopP())
        self.writeFootnotes()
        self.writeClosing()
        self.f.close()

    def writeHeader(self):
        h = u"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"></meta>
    <title>Bible</title>
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
"""
        self.write(h)

    def writeClosing(self):
        h = """
        </div>
    </body>
</html>
"""
        self.write(h)

    def startLI(self, level=1):
        if self.listItemLevel:
            self.stopLI()
        ret = u''
        self.listItemLevel = 0
        while self.listItemLevel < level:
            ret += u'<ul>'
            self.listItemLevel += 1 
        return ret

    def stopLI(self):
        ret = u''
        while self.listItemLevel > 0:
            ret += u'</ul>'
            self.listItemLevel -= 1
        return ret

    def stopP(self):
        if self.paragraphOpen:
            self.paragraphOpen = False
            return u'\n</p>\n\n'
        return u''

    def escape(self, s):
        return s.replace(u'~',u'&nbsp;')

    def write(self, unicodeString):
        self.f.write(unicodeString.replace(u'~', u' '))

    def writeIndent(self, level):
        if self.indentFlag:
            self.write(self.stopIndent())  # always close the last indent before starting a new one
        if level > 0:
            self.indentFlag = True
            self.write(self.stopP())
            self.write(u'\n<p class="indent-' + str(level) + u'">\n')
            self.write(u'&nbsp;' * (level * 4))  # spaces for PDF since we can't style margin with css

    def stopIndent(self):
        if self.indentFlag:
            self.indentFlag = False
            return u'\n</p>\n'
        else:
            return u''

    def renderID(self, token):
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.write(self.stopP())
        self.writeFootnotes()
        if self.cb:
            self.write('</div>\n\n');
        self.bookName = None
        self.cb = bookKeyForIdValue(token.value)
        self.chapterLabel = u'Chapter'
        self.write('<div id="bible-book-'+self.cb+'" class="bible-book-text">\n')

    def renderH(self, token):
        self.bookName = token.value
        self.write('<h1>' + self.bookName + u'</h1>\n')

    def renderTOC2(self, token):
        if not self.bookName:
            self.renderH(token)

    def renderMT(self, token):
        return  #self.write(u'\n\n<h1>' + token.value + u'</h1>') # removed to use TOC2

    def renderMT2(self, token):
        self.write(u'\n\n<h2>' + token.value + u'</h2>\n')

    def renderMT3(self, token):
        self.write(u'\n\n<h2>' + token.value + u'</h2>\n')

    def renderMS1(self, token):
        self.write(u'\n\n<h3>' + token.value + u'</h3>\n')

    def renderMS2(self, token):
        self.write(u'\n\n<h4>' + token.value + u'</h4>\n')

    def renderP(self, token):
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.write(self.stopP())
        self.write(u'\n\n<p>\n')
        self.paragraphOpen = True

    def renderPI(self, token):
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.write(self.stopP())
        self.writeIndent(2)

    def renderM(self, token):
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.write(self.stopP())
        self.write(u'\n\n<p>\n')
        self.paragraphOpen = True

    def renderS1(self, token):
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.write(u'\n\n<h4 style="text-align:center">' + token.getValue() + u'</h4>')

    def renderS2(self, token):
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.write(u'\n\n<h5 style="text-align:center">' + token.getValue() + u'</h5>')

    def renderS3(self, token):
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.write(u'\n\n<h5">' + token.getValue() + u'</h5>')

    def renderC(self, token):
        self.closeFootnote()
        self.write(self.stopIndent())
        self.write(self.stopLI())
        self.write(self.stopP())
        self.writeFootnotes()
        self.footnote_num = 1
        self.cc = token.value.zfill(3)
        self.write(u'\n\n<h2 id="{0}-ch-{1}" class="c-num">{2} {3}</h2>'
            .format(self.cb, self.cc, self.chapterLabel, token.value))

    def renderSP(self, token):
        self.write(u'</p><p class="s-who"><i>')
    def renderSPA(self, token):
        self.write(u'</i></p>')

    def renderV(self, token):
        self.closeFootnote()
        self.cv = token.value.zfill(3)
        self.write(self.stopLI())
        self.write(u' <span id="{0}-ch-{1}-v-{2}" class="v-num"><sup><b>{3}</b></sup></span>'
            .format(self.cb, self.cc, self.cv, token.value))

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
        self.write(self.stopLI())
        self.write(u'\n\n<p class="indent-0">&nbsp;</p>')

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
        self.write(u'<i class="quote selah" style="float:right;">')

    def renderQSE(self, token):
        self.write(u'</i>')

    def renderEMS(self, token):
        self.write(u'<i class="emphasis">')

    def renderEME(self, token):
        self.write(u'</i>')

    def renderE(self, token):
        self.write(self.stopIndent())
        self.write(self.stopP())
        self.write(u'\n\n<p>' + token.value + '</p>')

    def renderPB(self, token):
        pass

    def renderPERIPH(self, token):
        pass

    def renderLI(self, token):
        self.renderLI1(token)

    def renderLI1(self, token):
        self.write(self.startLI(1))

    def renderLI2(self, token):
        self.write(self.startLI(2))

    def renderLI3(self, token):
        self.write(self.startLI(3))

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
        self.write(u'<i class="quote right" style="display:block;float:right;">'+token.value+'</i>')

    def renderFQA(self, token):
        self.footnote_text += u'<i>'+token.value
        self.fqaFlag = True

    def renderFQAE(self, token):
        if self.fqaFlag:
            self.footnote_text += u'</i>'+token.value
        self.fqaFlag = False

    def closeFootnote(self):
        if self.footnoteFlag:
            self.footnoteFlag = False
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
            self.write(u'<hr class="footnotes-hr"/>')
            for fkey in sorted(fkeys):
                footnote = self.footnotes[fkey]
                self.write(u'<div id="{0}" class="footnote">{1}:{2} <sup><i>[<a href="#ref-{0}">{5}</a>]</i></sup><span class="text">{6}</span></div>'
                    .format(fkey, footnote['chapter'].lstrip('0'), footnote['verse'].lstrip('0'), footnote['chapter'], footnote['verse'], footnote['footnote'], footnote['text']))
            self.write(u'</div>')
        self.footnotes = {}

    def renderQA(self, token):
        self.write(u'<p class="quote acrostic heading" style="text-align:center;text-style:italic;">'+token.value+u'</p>')

    def renderQAC(self, token):
        self.write(u'<i class="quote acrostic character">')

    def renderQACE(self,token):
        self.write(u'</i>')

