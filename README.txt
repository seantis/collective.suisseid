suisseID integration for Plone. 

Learn more about suisseID: http://www.suisseid.ch

- Code repository: http://github.com/seantis/collective.suisseid
- Questions and comments to info@seantis.ch
- Report bugs at http://github.com/seantis/collective.suisseid/issues

Installing instructions can be found in docs/INSTALL.txt.

Contact us at:
seantis gmbh
http://www.seantis.ch
info@seantis.ch

Requirements
============

* Xmlsec

  * Debian package 'xmlsec1'
    
  * Build from source on MAC:
    
    ./configure --with-openssl=/usr/local/ --disable-apps-crypto-dl --disable-crypto-dl


* pySAML2

  Download from http://launchpad.net/pysaml2/0.1/0.1/+download/pysaml2.0.1.tgz
    
  Install with python setup.py install