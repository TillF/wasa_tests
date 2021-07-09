#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 16:10:31 2021

@author: alicelegendre
"""

import subprocess
import os

os.chdir('/Users/alicelegendre/Desktop/WASA/Data/TestInput_version0')

subprocess.call([r'/Users/alicelegendre/Desktop/WASA/Data/TestInput_version0/Run_WASA.bat'])
print('cc')