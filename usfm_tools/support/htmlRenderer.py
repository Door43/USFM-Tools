# -*- coding: utf-8 -*-
#

import abstractRenderer
import codecs
import books

#
#   Renders as set of web pages
#

class DummyFile(object):
    def close(self):
        pass
    def write(self, str):
        pass

class HTMLRenderer(abstractRenderer.AbstractRenderer):
    
    def __init__(self, inputDir, outputDir, oebFlag=False):
        # Unset
        self.f = DummyFile()  # output file stream
        self.ft = [] # array of text to write to file
        # IO
        self.outputDir = outputDir
        self.inputDir = inputDir
        # Caches
        self.cachedChapterMarker = u''
        self.cachedBookname = u''
        # Position
        self.cb = u''    # Current Book
        self.cc = u'001'    # Current Chapter
        self.cv = u'001'    # Currrent Verse
        # Flags
        self.indentFlag = False
        self.oebFlag = oebFlag
        self.fileCounter = 0
        self.secondaryCounter = 0
        
    def render(self):
        self.f = DummyFile()
        # Write pages
        self.loadUSFM(self.inputDir)
        self.run()
        self.close()
        
    def writeLog(self, s):
        print s
        
    # File handling    
        
    def openFile(self, bookID):
        self.f = open(self.outputDir + u'/b' + bookID + u'_' + str(self.fileCounter) + u'.html', 'w')
        self.bookID = bookID
        self.ft = []
        
    def close(self): 
        t = u''.join(self.ft)
        self.f.write(self.cleanHTML(t).encode('utf-8'))
        self.f.close()
 
    def write(self, unicodeString):
        self.ft.append(unicodeString)
        
    def cleanHTML(self, t):
        c = t
        c = t.replace(u'<p><br /><br />', u'<p>')
        c = c.replace(ur'~', u'&nbsp;')
        if self.oebFlag:
            c = c.replace(ur'%navmarker%', u'OEB')
            c = c.replace(ur'%linkToWebsite%',u'<tr><td colspan = "2"><a href="http://openenglishbible.org">OpenEnglishBible.org</a></td></tr>')
        else:
            c = c.replace(ur'%navmarker%', u'<div style="font-size:200%;color:green;">✝</div>')
            c = c.replace(ur'%linkToWebsite%',u'')
        return c
        
    # Support
    def incrementFile(self):
        self.ft.append(footer)
        self.ft.append(u'</html>')
        self.close()
        self.ft = []
        self.ft.append(header)
        self.ft.append("<p>")
        self.fileCounter +=1
        self.f = open(self.outputDir + u'/b' + self.bookID + u'_' + str(self.fileCounter) + u'.html', 'w')

    def writeChapterMarker(self):
        self.write(self.cachedChapterMarker)
        self.cachedChapterMarker = u''

    def writeIndent(self, level):
        if level == 0:
            self.indentFlag = False
            self.write(u'<br /><br />')
            return 
        if not self.indentFlag:
            self.indentFlag = True
            self.write(u'<br />')
        self.write(u'<br />')
        self.write(u'&nbsp;&nbsp;' * level)
        self.writeChapterMarker()

    def renderID(self, token): 
        self.write(footer)
        self.close()
        self.cb = books.bookKeyForIdValue(token.value)
        self.openFile(self.cb)
        self.write(header)
        self.indentFlag = False
    def renderTOC2(self, token):      self.write(u'</p><h2>' + token.value + u'</h2><p>')
    def renderMT(self, token):      self.write(u'</p><h1>' + token.value + u'</h1><p>')
    def renderMT2(self, token):      self.write(u'</p><h2>' + token.value + u'</h2><p>')
    def renderMS(self, token):      self.write(u'</p><h4>' + token.value + u'</h4><p>')
    def renderMS2(self, token):     self.write(u'</p><h5>' + token.value + u'</h5><p>')
    def renderP(self, token):
        self.indentFlag = False
        self.write(u'<br /><br />')
        self.writeChapterMarker()
    def renderS(self, token):
        self.indentFlag = False
        if token.value == u'~':
            self.write(u'<p>&nbsp;</p><p>')
        else:
            self.write(u'</p><h6>' + token.value + u'</h6><p>')
    def renderS2(self, token):
        self.indentFlag = False
        self.write(u'</p><h7>' + token.value + u'</h7><p>')
    def renderS5(self,token):
        if (self.secondaryCounter>=5):
            self.secondaryCounter = 1
            self.incrementFile()
        else:
            self.secondaryCounter+=1
    def renderC(self, token):
        self.cc = token.value.zfill(3)
        self.cachedChapterMarker = u'<span class="chapter">' + token.value + u'</span>'
        # if self.cb==u'019': self.write(u'<p><em>Psalm ' + token.value + u'</em></p>')
    def renderV(self, token):
        self.cv = token.value.zfill(3)
        if self.cv == u'001':
            pass
        else:
            self.write(u'\n<span class="verse" rel="v' + self.cb + self.cc + self.cv + u'">' + token.value + u'</span>\n')
    def renderWJS(self, token):     self.write(u'<span class="woc">')
    def renderWJE(self, token):     self.write(u'</span>')

    def renderNDS(self, token):     self.write(u'<span class="nd">')
    def renderNDE(self, token):     self.write(u'</span>')

    def renderTEXT(self, token):    self.write(u" " + token.value + u" ")
    def renderQ(self, token):       self.writeIndent(1)
    def renderQ1(self, token):      self.writeIndent(1)
    def renderQ2(self, token):      self.writeIndent(2)
    def renderQ3(self, token):      self.writeIndent(3)
    def renderNB(self, token):      self.writeIndent(0)
    def renderB(self, token):       self.write(u'<br />')
    def renderIS(self, token):      self.write(u'<i>')
    def renderIE(self, token):      self.write(u'</i>')
    def renderBDS(self, token):     self.f.write(u'<b>')
    def renderBDE(self, token):     self.f.write(u'</b>')
    def renderBDITS(self, token):   self.f.write(u'<b><i>')
    def renderBDITE(self, token):   self.f.write(u'</b></i>')
    def renderPBR(self, token):     self.write(u'<br />')

    #handle tables
    def renderTR(self,token):
        self.write(u'<tr>' + token.value + '</tr>')
    def renderTHR1(self,token):
        self.write(u'<th class="align-right">' + token.value + '</th>')
    def renderTHR2(self,token):
        self.write(u'<th class="align-right">' + token.value + '</th>')
    def renderTHR3(self,token):
        self.write(u'<th class="align-right">' + token.value + '</th>')
    def renderTHR4(self,token):
        self.write(u'<th class="align-right">' + token.value + '</th>')
    def renderTHR5(self,token):
        self.write(u'<th class="align-right">' + token.value + '</th>')
    def renderTHR6(self,token):
        self.write(u'<th class="align-right">' + token.value + '</th>')

    def renderTH1(self,token):
        self.write(u'<th>' + token.value + '</th>')
    def renderTH2(self,token):
        self.write(u'<th>' + token.value + '</th>')
    def renderTH3(self,token):
        self.write(u'<th>' + token.value + '</th>')
    def renderTH4(self,token):
        self.write(u'<th>' + token.value + '</th>')
    def renderTH5(self,token):
        self.write(u'<th>' + token.value + '</th>')
    def renderTH6(self,token):
        self.write(u'<th>' + token.value + '</th>')
    #table column right aligned
    def renderTCR1(self,token):
        self.write(u'<td class="align-right">' + token.value + '</td>')
    def renderTCR2(self,token):
        self.write(u'<td class="align-right">' + token.value + '</td>')
    def renderTCR3(self,token):
        self.write(u'<td class="align-right">' + token.value + '</td>')
    def renderTCR4(self,token):
        self.write(u'<td class="align-right">' + token.value + '</td>')
    def renderTCR5(self,token):
        self.write(u'<td class="align-right">' + token.value + '</td>')
    def renderTCR6(self,token):
        self.write(u'<td class="align-right">' + token.value + '</td>')

    #table column
    def renderTC1(self,token):
        self.write(u'<td>' + token.value + '</td>')
    def renderTC2(self,token):
        self.write(u'<td>' + token.value + '</td>')
    def renderTC3(self,token):
        self.write(u'<td>' + token.value + '</td>')
    def renderTC4(self,token):
        self.write(u'<td>' + token.value + '</td>')
    def renderTC5(self,token):
        self.write(u'<td>' + token.value + '</td>')
    def renderTC6(self,token):
        self.write(u'<td>' + token.value + '</td>')

    def renderD(self, token):       self.writeChapterMarker()

    def render_is1(self, token):    self.renderS(token)
    def render_ip(self, token):     self.renderP(token)
    def render_iot(self, token):    self.renderQ(token)
    def render_io1(self, token):    self.renderQ2(token)
    
    def renderFS(self, token):      self.write(u'<span class="rightnotemarker">*</span><span class="rightnote">')
    def renderFE(self, token):      self.write(u'</span>')
    

#
#  Structure
#

header = ur"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Open English Bible</title>
    <meta charset='utf-8'>
    <style type="text/css">
    @media all {
        html {font-size: 19px;} 
        body {
            padding: 0rem 0em 0rem 0em;
            margin-left:auto;
            margin-right:auto;
            width:100%;
            min-height: 100%;
            position: relative; 
        }
        body > * {
            font-size: 100%;
            line-height: 135%;
            text-rendering: optimizeLegibility;
            margin-left: 7rem; 
            margin-right: 7rem;
        }
        .chapter{
        	position: absolute;
        	left: 0rem;
        	width: 6rem;
        	text-align: right;
        	font-size: 120%;
        	color: #202020;
        }
        .verse{
        	width: 6rem;
        	text-align: right;
        	font-size: 80%;
        	color: gray;
        }
        .rightnotemarker{
            color: gray;
        }
        .rightnote{
        	position: absolute;
        	right: 0rem;
        	width: 6rem;
        	text-align: left;	
        	color: gray;
        	font-size: 80%;
        }
        h1{
        	font-family: 'Verdana', sans-serif;
        	font-size: 180%;
        	color: #202020;
        }
        h2{
        	font-family: 'Verdana', sans-serif;
        	font-size: 140%;
        	color: #202020;
        }
        h3{
        	font-family: 'Verdana', sans-serif;
        	font-size: 120%;
        	color: #202020;
        }
        h4{
        	font-family: 'Verdana', sans-serif;
        	font-size: 100%;
        	color: #202020;
            padding-top:2em;
        }
        h5{
        	font-family: 'Verdana', sans-serif;
        	font-size: 100%;
        	color: #202020;
            padding-top:2em;
        }
        h6{
        	font-family: 'Verdana', sans-serif;
        	font-size: 100%;
        	color: #202020;
            padding-top:0em;
        }
        h7{
        	font-family: 'Verdana', sans-serif;
        	font-size: 100%;
        	color: #202020;
            padding-top:0em;
        }
        p{
        	-webkit-hyphens: auto;
        	-moz-hyphens: auto;
        	-ms-hyphens: auto;
        	-o-hyphens: auto;
        	hyphens: auto;
        	font-family: 'Verdana', sans-serif;
        	color: #202020;
            -moz-font-feature-settings: "liga=1, dlig=1", "onum=1";
            -ms-font-feature-settings: "liga", "dlig","onum";
            -webkit-font-feature-settings: "liga", "dlig","onum";
            -o-font-feature-settings: "liga", "dlig","onum";
            font-feature-settings: "liga", "dlig","onum";
        }
        .align-right {
            align:right;
        }
        .nd { /* Lord */
            font-variant:small-caps;
        }
        .vspacer{
            height:1em;
        }
    }
    @media all and (max-width:800px){html {font-size: 19px;}}
    @media all and (max-width:760px){html {font-size: 18px;}}
    @media all and (max-width:720px){html {font-size: 17px;}}
    @media all and (max-width:680px){html {font-size: 16px;}}
    @media all and (max-width:640px){html {font-size: 14px;}}
    @media all and (max-width:600px){html {font-size: 12px;}}
    
    /* iPhone 2 - 4 */
    @media only screen 
    and (min-device-width : 320px) 
    and (max-device-width : 480px) 
    and (orientation : portrait) {
        html {font-size: 58px;}
        body {
            margin:0;
            padding:0;
        } 
        body > * { margin-left:100px; margin-right:0px; width:100%; }
        .chapter{
        	position: absolute;
        	left: 20px;
        	width: 60px;
        	text-align: left;
        	font-size: 100%;
        	color: green;
        }
        .verse{
        	position: absolute;
        	left: 20px;
        	width: 60px;
        	text-align: left;
        	font-size: 80%;
        	color: green;
        }
        .navbar {
            position:relative;
        }
    }
    </style>
    </head>

    <body>
        """

footer = ur"""
        </p></body>   
        """

indexPage = header + ur"""<h1>Bible</h1>""" + footer
