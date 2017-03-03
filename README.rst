USFM Tools
==========

This project comprises a framework for transforming .usfm files into specified targets.

It is primarily used for the Open English Bible, and may need adjustment if used for other purposes.

This fork of USFM-Tools includes basic support for conversion to USX.

Prerequisites
*************

::

    sudo easy_install pyparsing

Get code
********

::

    git clone https://github.com/kbuildsyourdotcom/USX.git
    cd USX
    python transform.py --setup

(This downloads ConTeXt and may take a while.)

Font Setup
**********

After getting the Noto fonts installed on the system, the following can be run to get the Noto fonts into ConTeXt:

::

    . /opt/context/tex/setuptex
    export OSFONTDIR="/usr/local/share/fonts;$HOME/.fonts"
    mtxrun --script fonts --reload
    context --generate

Running ``mtxrun --script fonts --list --all --pattern=*oto*`` should now list a bunch of the Noto fonts.  More information at http://wiki.contextgarden.net/Fonts_in_LuaTeX.

Running
*******

When running the conversion, you may split the results by book (currently only supported for USX):

::

    python transform.py --target=usx --usfmDir=./docs/source/ --builtDir=./docs/translation/ --fileByBook

To output the results to single file (supported by all output formats):

::

    python transform.py --target=usx --usfmDir=./docs/source/ --builtDir=./docs/translation/ --name=MyTranslation

Production Use
**************

This script will be used in the process of converting USFM text from Etherpad into USX format. The text in Etherpad will first be combined using this script https://github.com/Door43/tools/blob/master/uwb/ep_export.py. The output of the afor mentioned script will then be processed by the script in this repository to transform the USFM to USX. This USX output will at some point become available in the translationStudio api under the Bible translation projects.

Submitting to pypi
******************

**Add the library to pypi if you haven't already.**

1. Run ``python setup.py sdist bdist_wheel``.
2. Go to https://pypi.python.org/pypi?%3Aaction=submit_form
3. Click "Choose File" and pick ``usfm_tools.egg-info/PKG-INFO``, then click "Add Package Info."

**Install twine**

::

    sudo pip install twine

**Create settings file ``~/.pypirc`` with these contents:**

::

    [distutils]
    index-servers=pypi

    [pypi]
    repository = https://upload.pypi.org/legacy/
    username = <USER-NAME>
    password = <PASSWORD>

**Generate the packages and upload**

::

    python setup.py sdist bdist_wheel
    twine upload dist/*

