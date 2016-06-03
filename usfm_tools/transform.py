from __future__ import print_function, unicode_literals
import getopt
import sys
import os
from subprocess import Popen, PIPE
from usfm_tools.support import loutRenderer, contextRenderer, htmlRenderer, singlehtmlRenderer, csvRenderer, \
    readerise, mdRenderer, asciiRenderer, usxRenderer, mediawikiPrinter


class UsfmTransform(object):

    savedCWD = ''

    @staticmethod
    def runscriptold(c, prefix=''):
        print(prefix + ':: ' + c)
        pp = Popen(c, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        for ln in pp.stdout:
            print(prefix + ln[:-1])

    @staticmethod
    def runscript(c, prefix='', repeatFilter=''):
        print(prefix + ':: ' + c)
        pp = Popen([c], shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        (result, stderrdata) = pp.communicate()
        print(result)
        print(stderrdata)
        if not repeatFilter == '' and not stderrdata.find(repeatFilter) == -1:
            UsfmTransform.runscript(c, prefix, repeatFilter)

    @staticmethod
    def setup():
        c = """
        cd support/thirdparty
        rm -rf context
        mkdir context
        cd context
        curl -o first-setup.sh http://minimals.contextgarden.net/setup/first-setup.sh
        sh ./first-setup.sh
        . ./tex/setuptex
        cd ..
        curl -o usfm2osis.pl http://crosswire.org/ftpmirror/pub/sword/utils/perl/usfm2osis.pl
        """
        UsfmTransform.runscript(c)

    @staticmethod
    def buildLout(usfmDir, builtDir, buildName):
        print('#### Building Lout...')

        # Prepare
        print('     Clean working dir')
        UsfmTransform.runscript('rm "' + builtDir + '/working/lout/*"', '       ')

        # Convert to Lout
        print('     Converting to Lout')
        UsfmTransform.ensureOutputDir(builtDir + '/working/lout')
        c = loutRenderer.LoutRenderer(usfmDir, builtDir + '/working/lout/' + buildName + '.lout')
        c.render()

        # Run Lout
        print('     Copying support files')
        UsfmTransform.runscript('cp support/lout/oebbook working/lout', '       ')
        print('     Running Lout')
        UsfmTransform.runscript('cd "' + builtDir + '/working/lout"; lout "./' + buildName + '.lout" > "' + buildName +
                                '.ps"', '       ',
                                repeatFilter='unresolved cross reference')
        print('     Running ps2pdf')
        UsfmTransform.runscript(
            'cd "' + builtDir + '/working/lout"; ps2pdf -dDEVICEWIDTHPOINTS=432 -dDEVICEHEIGHTPOINTS=648 "' +
            buildName + '.ps" "' + buildName + '.pdf" ',
            '       ')
        print('     Copying into builtDir')
        UsfmTransform.runscript('cp "' + builtDir + '/working/lout/' + buildName + '.pdf" "' + builtDir + '/' +
                                buildName + '.pdf" ', '       ')

    @staticmethod
    def buildConTeXt(usfmDir, builtDir, buildName):
        print('#### Building PDF via ConTeXt...')

        # Convert to ConTeXt
        print('     Converting to ConTeXt...')
        # c = texise.TransformToContext()
        # c.setupAndRun(usfmDir, 'working/tex', buildName)
        UsfmTransform.ensureOutputDir(builtDir + '/working/tex')
        UsfmTransform.ensureOutputDir(builtDir + '/working/tex-working')
        c = contextRenderer.ConTeXtRenderer(usfmDir, builtDir + '/working/tex/bible.tex')
        c.render()

    @staticmethod
    def buildWeb(usfmDir, builtDir, buildName, oebFlag=False):
        # Convert to HTML
        print('#### Building Web HTML...')
        UsfmTransform.ensureOutputDir(builtDir + '/' + buildName + '_html')
        c = htmlRenderer.HTMLRenderer(usfmDir, builtDir + '/' + buildName + '_html', oebFlag)
        c.render()

    @staticmethod
    def buildSingleHtml(usfmDir, builtDir, buildName):
        # Convert to HTML
        print('#### Building Single Page HTML...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = singlehtmlRenderer.SingleHTMLRenderer(usfmDir, builtDir + '/' + buildName + '.html')
        c.render()

    @staticmethod
    def buildCSV(usfmDir, builtDir, buildName):
        # Convert to CSV
        print('#### Building CSV...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = csvRenderer.CSVRenderer(usfmDir, builtDir + '/' + buildName + '.csv')
        c.render()

    @staticmethod
    def buildReader(usfmDir, builtDir, buildName):
        # Convert to HTML for online reader
        print('#### Building for Reader...')
        UsfmTransform.ensureOutputDir(builtDir + 'en_oeb')
        c = readerise.TransformForReader()
        c.setupAndRun(usfmDir, builtDir + 'en_oeb')

    @staticmethod
    def buildMarkdown(usfmDir, builtDir, buildName):
        # Convert to Markdown for Pandoc
        print('#### Building for Markdown...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = mdRenderer.MarkdownRenderer(usfmDir, builtDir + '/' + buildName + '.md')
        c.render()

    @staticmethod
    def buildASCII(usfmDir, builtDir, buildName):
        # Convert to ASCII
        print('#### Building for ASCII...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = asciiRenderer.ASCIIRenderer(usfmDir, builtDir + '/' + buildName + '.txt')
        c.render()

    @staticmethod
    def buildUSX(usfmDir, builtDir, buildName, byBookFlag):
        # Convert to USX
        print('#### Building for USX...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = usxRenderer.USXRenderer(usfmDir, builtDir + '/', buildName, byBookFlag)
        c.render()

    @staticmethod
    def buildMediawiki(usfmDir, builtDir, buildName):
        # Convert to MediaWiki format for Door43
        print('#### Building for Mediawiki...')
        # Check output directory
        UsfmTransform.ensureOutputDir(builtDir + '/mediawiki')
        mediawikiPrinter.Transform().setupAndRun(usfmDir, builtDir + '/mediawiki')

    @staticmethod
    def ensureOutputDir(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    @staticmethod
    def saveCWD():
        global savedCWD
        savedCWD = os.getcwd()
        root_dir_of_tools = os.path.dirname(os.path.abspath(__file__))
        os.chdir(root_dir_of_tools)

    @staticmethod
    def restoreCWD(): os.chdir(savedCWD)

    @staticmethod
    def run(argv):
        UsfmTransform.saveCWD()
        oeb_flag = False
        by_book_flag = False
        targets = ''
        build_dir = ''
        usfm_dir = ''
        build_name = ''

        print('#### Starting Build.')
        try:
            opts, args = getopt.getopt(argv, "sht:u:b:n:o",
                                       ["setup", "help", "target=", "usfmDir=", "builtDir=", "name=", "oeb",
                                        "fileByBook"])
        except getopt.GetoptError:
            UsfmTransform.usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                return UsfmTransform.usage()
            elif opt in ("-s", "--setup"):
                return UsfmTransform.setup()
            elif opt in ("-t", "--target"):
                targets = arg
            elif opt in ("-u", "--usfmDir"):
                usfm_dir = arg
            elif opt in ("-b", "--builtDir"):
                build_dir = arg
            elif opt in ("-n", "--name"):
                build_name = arg
            elif opt in ("-o", "--oeb"):
                oeb_flag = True
            elif opt in ("-f", "--fileByBook"):
                by_book_flag = True
            else:
                UsfmTransform.usage()

        if targets == 'context':
            UsfmTransform.buildConTeXt(usfm_dir, build_dir, build_name)
        elif targets == 'html':
            UsfmTransform.buildWeb(usfm_dir, build_dir, build_name, oeb_flag)
        elif targets == 'singlehtml':
            UsfmTransform.buildSingleHtml(usfm_dir, build_dir, build_name)
        elif targets == 'md':
            UsfmTransform.buildMarkdown(usfm_dir, build_dir, build_name)
        elif targets == 'reader':
            UsfmTransform.buildReader(usfm_dir, build_dir, build_name)
        elif targets == 'mediawiki':
            UsfmTransform.buildMediawiki(usfm_dir, build_dir, build_name)
        elif targets == 'lout':
            UsfmTransform.buildLout(usfm_dir, build_dir, build_name)
        elif targets == 'csv':
            UsfmTransform.buildCSV(usfm_dir, build_dir, build_name)
        elif targets == 'ascii':
            UsfmTransform.buildASCII(usfm_dir, build_dir, build_name)
        elif targets == 'csv':
            UsfmTransform.buildCSV(usfm_dir, build_dir, build_name)
        elif targets == 'usx':
            if by_book_flag:
                build_name = u''
            UsfmTransform.buildUSX(usfm_dir, build_dir, build_name, by_book_flag)
        else:
            UsfmTransform.usage()

        print('#### Finished.')
        UsfmTransform.restoreCWD()

    @staticmethod
    def usage():
        print("""
            USFM-Tools
            ----------

            Build script.  See source for details.

            Setup:
            transform.py --setup

        """)


if __name__ == "__main__":
    UsfmTransform.run(sys.argv[1:])
