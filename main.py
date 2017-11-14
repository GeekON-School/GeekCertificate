#!/usr/bin/env python

import certificate

cert = certificate.CertificateCreator('test.json', 'settings.json')

# cert.setSettings('settings.json')
# cert.setData('test.json')

cert.createCertificates()
