from __future__ import print_function, unicode_literals
import getopt
import sys
import os
import logging
from subprocess import Popen, PIPE
from usfm_tools.support import loutRenderer, contextRenderer, htmlRenderer, singlehtmlRenderer, csvRenderer, \
    readerise, mdRenderer, asciiRenderer, usxRenderer, mediawikiPrinter


class UsfmTransform(object):

    savedCWD = ''
    __logger = logging.getLogger('usfm_tools')

    @staticmethod
    def runscriptold(c, prefix=''):
        UsfmTransform.__logger.info(prefix + ':: ' + c)
        pp = Popen(c, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        for ln in pp.stdout:
            UsfmTransform.__logger.info(prefix + ln[:-1])

    @staticmethod
    def runscript(c, prefix='', repeatFilter=''):
        UsfmTransform.__logger.info(prefix + ':: ' + c)
        pp = Popen([c], shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        (result, stderrdata) = pp.communicate()
        UsfmTransform.__logger.info(result)
        UsfmTransform.__logger.info(stderrdata)
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
        UsfmTransform.__logger.info('Building Lout...')

        # Prepare
        UsfmTransform.__logger.info('Clean working dir')
        UsfmTransform.runscript('rm "' + builtDir + '/working/lout/*"', '       ')

        # Convert to Lout
        UsfmTransform.__logger.info('Converting to Lout')
        UsfmTransform.ensureOutputDir(builtDir + '/working/lout')
        c = loutRenderer.LoutRenderer(usfmDir, builtDir + '/working/lout/' + buildName + '.lout')
        c.render()

        # Run Lout
        UsfmTransform.__logger.info('Copying support files')
        UsfmTransform.runscript('cp support/lout/oebbook working/lout', '       ')
        UsfmTransform.__logger.info('Running Lout')
        UsfmTransform.runscript('cd "' + builtDir + '/working/lout"; lout "./' + buildName + '.lout" > "' + buildName +
                                '.ps"', '       ',
                                repeatFilter='unresolved cross reference')
        UsfmTransform.__logger.info('Running ps2pdf')
        UsfmTransform.runscript(
            'cd "' + builtDir + '/working/lout"; ps2pdf -dDEVICEWIDTHPOINTS=432 -dDEVICEHEIGHTPOINTS=648 "' +
            buildName + '.ps" "' + buildName + '.pdf" ',
            '       ')
        UsfmTransform.__logger.info('Copying into builtDir')
        UsfmTransform.runscript('cp "' + builtDir + '/working/lout/' + buildName + '.pdf" "' + builtDir + '/' +
                                buildName + '.pdf" ', '       ')

    @staticmethod
    def buildConTeXt(usfmDir, builtDir, buildName):
        UsfmTransform.__logger.info('Building PDF via ConTeXt...')

        # Convert to ConTeXt
        UsfmTransform.__logger.info('Converting to ConTeXt...')
        # c = texise.TransformToContext()
        # c.setupAndRun(usfmDir, 'working/tex', buildName)
        UsfmTransform.ensureOutputDir(builtDir + '/working/tex')
        UsfmTransform.ensureOutputDir(builtDir + '/working/tex-working')
        c = contextRenderer.ConTeXtRenderer(usfmDir, builtDir + '/working/tex/bible.tex')
        c.render()

    @staticmethod
    def buildWeb(usfmDir, builtDir, buildName, oebFlag=False):
        # Convert to HTML
        UsfmTransform.__logger.info('Building Web HTML...')
        UsfmTransform.ensureOutputDir(builtDir + '/' + buildName + '_html')
        c = htmlRenderer.HTMLRenderer(usfmDir, builtDir + '/' + buildName + '_html', oebFlag)
        c.render()

    @staticmethod
    def buildSingleHtml(usfmDir, builtDir, buildName):
        # Convert to HTML
        UsfmTransform.__logger.info('Building Single Page HTML...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = singlehtmlRenderer.SingleHTMLRenderer(usfmDir, builtDir + '/' + buildName + '.html')
        c.render()

    @staticmethod
    def buildCSV(usfmDir, builtDir, buildName):
        # Convert to CSV
        UsfmTransform.__logger.info('Building CSV...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = csvRenderer.CSVRenderer(usfmDir, builtDir + '/' + buildName + '.csv')
        c.render()

    @staticmethod
    def buildReader(usfmDir, builtDir, buildName):
        # Convert to HTML for online reader
        UsfmTransform.__logger.info('Building for Reader...')
        UsfmTransform.ensureOutputDir(builtDir + 'en_oeb')
        c = readerise.TransformForReader()
        c.setupAndRun(usfmDir, builtDir + 'en_oeb')

    @staticmethod
    def buildMarkdown(usfmDir, builtDir, buildName):
        # Convert to Markdown for Pandoc
        UsfmTransform.__logger.info('Building for Markdown...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = mdRenderer.MarkdownRenderer(usfmDir, builtDir + '/' + buildName + '.md')
        c.render()

    @staticmethod
    def buildASCII(usfmDir, builtDir, buildName):
        # Convert to ASCII
        UsfmTransform.__logger.info('Building for ASCII...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = asciiRenderer.ASCIIRenderer(usfmDir, builtDir + '/' + buildName + '.txt')
        c.render()

    @staticmethod
    def buildUSX(usfmDir, builtDir, buildName, byBookFlag):
        # Convert to USX
        UsfmTransform.__logger.info('Building for USX...')
        UsfmTransform.ensureOutputDir(builtDir)
        c = usxRenderer.USXRenderer(usfmDir, builtDir + '/', buildName, byBookFlag)
        c.render()

    @staticmethod
    def buildMediawiki(usfmDir, builtDir, buildName):
        # Convert to MediaWiki format for Door43
        UsfmTransform.__logger.info('Building for Mediawiki...')
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

        UsfmTransform.__logger.info('Starting Build.')
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

            UsfmTransform.__logger.info('Finished.')
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
