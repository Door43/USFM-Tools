# -*- coding: utf-8 -*-
#

from __future__ import print_function, unicode_literals
import abstractRenderer
import codecs
import logging

#
#   Simplest renderer. Ignores everything except ascii text.
#


# noinspection PyPep8Naming,PyUnusedLocal
class USXRenderer(abstractRenderer.AbstractRenderer):
    def __init__(self, input_dir, output_path, output_name, by_book_flag):
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilePath = output_path
        self.outputFileName = output_name
        self.outputFileExt = '.usx'
        self.inputDir = input_dir
        self.byBook = by_book_flag
        # Position
        self.currentC = 1
        self.currentV = 1
        self.book = ''        # book id
        self.renderBook = ''  # book name
        # Flags
        self.printerState = {'c': False, 'p': False, 'pi': False, 'pi2': False, 'q': False, 'li': False, 'row': False,
                             'cell': False, 'table': False}
        # Errors
        self.error = ''
        self.__logger = logging.getLogger('usfm_tools')

    def render(self):
        self.loadUSFM(self.inputDir)
        if self.byBook:
            self.__logger.info('Creating One File Per Book\n')
            for bookName in self.booksUsfm:
                self.f = codecs.open(self.outputFilePath + bookName + self.outputFileExt, 'w', 'utf_8_sig')
                self.renderBook = bookName
                self.run()
                self.f.write(self.stop_all())
                self.f.close()
        else:
            self.__logger.info('Concatenating Books into ' + self.outputFileName + self.outputFileExt + '\n')
            self.f = codecs.open(self.outputFilePath + self.outputFileName + self.outputFileExt, 'w', 'utf_8_sig')
            self.run()
            self.f.write(self.stop_p() + self.stop_pi() + self.stop_pi2() + self.stop_q() + self.stop_li())
            self.f.close()
        self.__logger.info('')

    def writeLog(self, s):
        self.__logger.info(s)

    # Support

    def indent(self):
        if self.printerState['p']:
            return '  '
        else:
            return ''

    def start_c(self):
        if not self.printerState['c']:
            self.printerState['c'] = True
        return '\n<chapter number="' + str(self.currentC) + '"'

    def stop_c(self):
        if self.printerState['c']:
            self.printerState['c'] = False
            return ' style="c" />'
        else:
            return ''

    def start_p(self):
        if not self.printerState['p']:
            self.printerState['p'] = True
        return '\n<para style="p">'

    def stop_p(self):
        if self.printerState['p']:
            self.printerState['p'] = False
            return '</para>'
        else:
            return ''

    def start_pi(self):
        if not self.printerState['pi']:
            self.printerState['pi'] = True
        return '\n<para style="pi">'

    def stop_pi(self):
        if self.printerState['pi']:
            self.printerState['pi'] = False
            return '</para>'
        else:
            return ''

    def start_pi2(self):
        if not self.printerState['pi2']:
            self.printerState['pi2'] = True
        return '\n<para style="pi2">'

    def stop_pi2(self):
        if self.printerState['pi2']:
            self.printerState['pi2'] = False
            return '</para>'
        else:
            return ''

    def start_q(self, n):
        if not self.printerState['q']:
            self.printerState['q'] = True
        return '\n<para style="q' + str(n) + '">'

    def start_qm(self, n):
        if not self.printerState['q']:
            self.printerState['q'] = True
        return '\n<para style="qm' + str(n) + '">'

    def stop_q(self):
        if self.printerState['q']:
            self.printerState['q'] = False
            return '</para>'
        else:
            return ''

    def start_li(self, n):
        if not self.printerState['li']:
            self.printerState['li'] = True
        return '\n<para style="li' + str(n) + '">'

    def stop_li(self):
        if self.printerState['li']:
            self.printerState['li'] = False
            return '</para>'
        else:
            return ''

    def start_cell(self, style, align):
        if not self.printerState['cell']:
            self.printerState['cell'] = True
            return '\n    <cell style="' + style + '" align="' + align + '">'
        else:
            return ''

    def stop_cell(self):
        if self.printerState['cell']:
            self.printerState['cell'] = False
            return '</cell>'
        else:
            return ''

    def start_row(self):
        if not self.printerState['row']:
            self.printerState['row'] = True
        return '\n  <row style="tr">'

    def stop_row(self):
        if self.printerState['row']:
            self.printerState['row'] = False
            return '\n  </row>'
        else:
            return ''

    def start_table(self):
        if not self.printerState['table']:
            self.printerState['table'] = True
            return '\n<table>'
        else:
            return ''

    def stop_table(self):
        if self.printerState['table']:
            self.printerState['table'] = False
            return '\n</table>'
        else:
            return ''

    def stop_all(self):
        return self.stop_c() + self.stop_p() + self.stop_pi() + self.stop_pi2() + self.stop_q() + self.stop_li() + \
               self.stop_cell() + self.stop_row() + self.stop_table()

    def stop_all_to_cell(self):
        return self.stop_c() + self.stop_p() + self.stop_pi() + self.stop_pi2() + self.stop_q() + self.stop_li() + \
               self.stop_cell()

    # noinspection PyMethodMayBeStatic
    def escape(self, s):
        return s

    def renderTEXT(self, token):
        self.f.write(self.escape(token.value))

    def renderH(self, token):
        self.book = token.getValue()

    def renderMT(self, token):
        self.f.write(self.stop_all() + '\n<para style="mt">' + token.value.upper() + '</para>')

    def renderMT1(self, token):
        self.f.write(self.stop_all() + '\n<para style="mt1">' + token.value.upper() + '</para>')

    def renderMT2(self, token):
        self.f.write(self.stop_all() + '\n<para style="mt2">' + token.value.upper() + '</para>')

    def renderMT3(self, token):
        self.f.write(self.stop_all() + '\n<para style="mt3">' + token.value.upper() + '</para>')

    def renderMT4(self, token):
        self.f.write(self.stop_all() + '\n<para style="mt4">' + token.value.upper() + '</para>')

    def renderMT5(self, token):
        self.f.write(self.stop_all() + '\n<para style="mt5">' + token.value.upper() + '</para>')

    def renderMS(self, token):
        self.f.write(self.stop_all() + '\n<para style="ms">' + token.value + '</para>')

    def renderMS1(self, token):
        self.f.write(self.stop_all() + '\n<para style="ms1">' + token.value + '</para>')

    def renderMS2(self, token):
        self.f.write(self.stop_all() + '\n<para style="ms2">' + token.value + '</para>')

    def renderMS3(self, token):
        self.f.write(self.stop_all() + '\n<para style="ms3">' + token.value + '</para>')

    def renderMS4(self, token):
        self.f.write(self.stop_all() + '\n<para style="ms4">' + token.value + '</para>')

    def renderMS5(self, token):
        self.f.write(self.stop_all() + '\n<para style="ms5">' + token.value + '</para>')

    def renderP(self, token):
        self.f.write(self.stop_all() + self.start_p())

    def renderPI(self, token):
        self.f.write(self.stop_all() + self.start_pi())

    def renderPI2(self, token):
        self.f.write(self.stop_all() + self.start_pi2())

    def renderB(self, token):
        self.f.write(self.stop_all() + '\n<para style="b" />')

    def renderS(self, token):
        self.f.write(self.stop_all() + '\n\n<para style="s">' + token.value + '</para>')

    def renderS1(self, token):
        self.f.write(self.stop_all() + '\n\n<para style="s1">' + token.value + '</para>')

    def renderS2(self, token):
        self.f.write(self.stop_all() + '\n\n<para style="s2">' + token.value + '</para>')

    def renderS3(self, token):
        self.f.write(self.stop_all() + '\n\n<para style="s3">' + token.value + '</para>')

    def renderS4(self, token):
        self.f.write(self.stop_all() + '\n\n<para style="s4">' + token.value + '</para>')

    def renderS5(self, token):
        self.f.write(self.stop_c() + '\n<note caller="u" style="s5"></note>')

    def renderC(self, token):
        self.currentC = token.value
        self.currentV = '0'
        self.f.write(self.stop_all() + self.start_c())

    def renderCAS(self, token):
        self.f.write(' altnumber="')

    # noinspection PyUnusedLocal
    def renderCAE(self, token):
        self.f.write('"')

    def renderCL(self, token):
        self.f.write(self.stop_all() + '\n\n<para style="cl">' + token.value + '</para>')

    def renderV(self, token):
        self.currentV = token.value
        self.f.write(
            self.stop_c() + '\n' + self.indent() + '<verse number="' + token.value + '" style="v" />')

    def renderQ(self, token):
        self.renderQ1(token)

    def renderQ1(self, token):
        self.f.write(self.stop_all() + self.start_q(1))

    def renderQ2(self, token):
        self.f.write(self.stop_all() + self.start_q(2))

    def renderQ3(self, token):
        self.f.write(self.stop_all() + self.start_q(3))

    def renderQ4(self, token):
        self.f.write(self.stop_all() + self.start_q(4))

    def renderQA(self, token):
        self.f.write(self.stop_all() + '\n<para style="qa">' + token.value + '</para>')

    def renderQAC(self, token):
        self.f.write(self.stop_c() + '\n<char style="qac">' + self.escape(token.value) + '</char>')

    def renderQC(self, token):
        self.f.write(self.stop_all() + '\n<para style="qc">' + token.value + '</para>')

    def renderQM(self, token):
        self.renderQM1(token)

    def renderQM1(self, token):
        self.f.write(self.stop_all() + self.start_qm(1))

    def renderQM2(self, token):
        self.f.write(self.stop_all() + self.start_qm(2))

    def renderQM3(self, token):
        self.f.write(self.stop_all() + self.start_qm(3))

    def renderQR(self, token):
        self.f.write(self.stop_all() + '\n<para style="qr">' + token.value + '</para>')

    def renderQSS(self, token):
        self.f.write(self.stop_c() + '\n<char style="qs">')

    def renderQSE(self, token):
        self.f.write(self.stop_c() + '</char>')

    def renderQTS(self, token):
        self.f.write(self.stop_c() + '<char style="qt">')

    def renderQTE(self, token):
        self.f.write(self.stop_c() + '</char>')

    def renderNB(self, token):
        self.f.write(self.stop_c() + '\n<char style="nb">' + self.indent() + '</char>')

    def renderLI(self, token):
        self.renderLI1(token)

    def renderLI1(self, token):
        self.f.write(self.stop_all() + self.start_li(1))

    def renderLI2(self, token):
        self.f.write(self.stop_all() + self.start_li(2))

    def renderLI3(self, token):
        self.f.write(self.stop_all() + self.start_li(3))

    def renderLI4(self, token):
        self.f.write(self.stop_all() + self.start_li(4))

    def renderPBR(self, token):
        self.f.write(self.stop_c() + '\n')

    def renderBDS(self, token):
        self.f.write(self.stop_c() + '<char style="bd">')

    def renderBDE(self, token):
        self.f.write(self.stop_c() + '</char>')

    def renderBDITS(self, token):
        # noinspection SpellCheckingInspection
        self.f.write(self.stop_c() + '<char style="bdit">')

    def renderBDITE(self, token):
        self.f.write(self.stop_c() + '</char>')

    def renderEMS(self, token):
        self.f.write(self.stop_c() + '<char style="em">')

    def renderEME(self, token):
        self.f.write(self.stop_c() + '</char>')

    def renderITS(self, token):
        self.f.write(self.stop_c() + '<char style="it">')

    def renderITE(self, token):
        self.f.write(self.stop_c() + '</char>')

    def renderNOS(self, token):
        self.f.write(self.stop_c() + '<char style="no">')

    def renderNOE(self, token):
        self.f.write(self.stop_c() + '</char>')

    def renderSCS(self, token):
        self.f.write(self.stop_c() + '<char style="sc">')

    def renderSCE(self, token):
        self.f.write(self.stop_c() + '</char>')

    def renderFS(self, token):
        self.f.write(self.stop_c() + '\n<note caller="+" style="f">')

    def renderFE(self, token):
        self.f.write(self.stop_c() + '\n</note>')

    def renderFR(self, token):
        self.f.write(self.stop_c() + '\n  <char style="fr">' + self.escape(token.value) + '</char>')

    def renderFT(self, token):
        self.f.write(self.stop_c() + '\n  <char style="ft">' + self.escape(token.value) + '</char>')

    def renderFQ(self, token):
        self.f.write(self.stop_c() + '\n  <char style="fq">' + self.escape(token.value) + '</char>')

    def renderFQA(self, token):
        self.f.write(self.stop_c() + '\n  <char style="fqa">' + self.escape(token.value) + '</char>')

    def renderFP(self, token):
        self.f.write(self.stop_c() + '\n')

    def renderFQAE(self, token):
        pass

    def renderFQB(self, token):
        pass

    def renderXS(self, token):
        self.f.write(self.stop_c() + '\n<note caller="-" style="x">')

    def renderXE(self, token):
        self.f.write(self.stop_c() + '\n</note>')

    def renderXO(self, token):
        self.f.write(self.stop_c() + '\n  <char style="xo">' + self.escape(token.value) + '</char>')

    def renderXT(self, token):
        self.f.write(self.stop_c() + '\n  <char style="xt">' + self.escape(token.value) + '</char>')

    def renderTR(self, token):
        self.f.write(self.stop_all_to_cell() + self.stop_row() + self.start_table() + self.start_row())

    def renderTH1(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('th1', 'start'))

    def renderTH2(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('th2', 'start'))

    def renderTH3(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('th3', 'start'))

    def renderTH4(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('th4', 'start'))

    def renderTH5(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('th5', 'start'))

    def renderTH6(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('th6', 'start'))

    def renderTHR1(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('thr1', 'end'))

    def renderTHR2(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('thr2', 'end'))

    def renderTHR3(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('thr3', 'end'))

    def renderTHR4(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('thr4', 'end'))

    def renderTHR5(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('thr5', 'end'))

    def renderTHR6(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('thr6', 'end'))

    def renderTC1(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tc1', 'start'))

    def renderTC2(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tc2', 'start'))

    def renderTC3(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tc3', 'start'))

    def renderTC4(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tc4', 'start'))

    def renderTC5(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tc5', 'start'))

    def renderTC6(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tc6', 'start'))

    def renderTCR1(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tcr1', 'end'))

    def renderTCR2(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tcr2', 'end'))

    def renderTCR3(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tcr3', 'end'))

    def renderTCR4(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tcr4', 'end'))

    def renderTCR5(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tcr5', 'end'))

    def renderTCR6(self, token):
        self.f.write(self.stop_all_to_cell() + self.start_cell('tcr6', 'end'))

    def render_imt1(self, token):
        self.f.write(self.stop_all() + '\n<para style="imt1">' + token.value.upper() + '</para>')

    def render_imt2(self, token):
        self.f.write(self.stop_all() + '\n<para style="imt2">' + token.value.upper() + '</para>')

    def render_imt3(self, token):
        self.f.write(self.stop_all() + '\n<para style="imt3">' + token.value.upper() + '</para>')

    def renderD(self, token):
        self.f.write(self.stop_all() + '\n<para style="d">' + token.value + '</para>')

    def renderUnknown(self, token):
        if token.value == 'v':
            self.currentV = int(self.currentV) + 1
        self.__logger.error(self.renderBook + ' ' + str(self.currentC) + ':' + str(self.currentV) +
              ' - Unknown Token: \\' + self.escape(token.value))
