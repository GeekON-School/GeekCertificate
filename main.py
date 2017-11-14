#!/usr/bin/env python

import certificate

cert = certificate.CertificateCreator()

cert.setSettings('settings.json')
cert.setData('test.json')
cert.setQr(True)

cert.createCertificates()
