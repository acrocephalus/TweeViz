#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: TwitterLogin.py
#insert your Twitter keys here
import config

def login():
    if(config.api.verify_credentials):
        print '-------------------------\n\
        *** You are logged in ***\n\
        -------------------------'
version = '0.1'
#End of TwitterLogin.py