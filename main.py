#!/usr/bin/env python
# -*- coding: utf-8 -*-

import certificate

cert = certificate.CertificateCreator('test.json')

# cert.setSettings('settings.json')
# cert.setData('test.json')

cert.createCertificates()
