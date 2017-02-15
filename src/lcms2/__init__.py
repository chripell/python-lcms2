# -*- coding: utf-8 -*-
#
# 	lcms2 - package which provides simplified binding to LittleCMS2 library.
# 	Specially created for SwatchBooker.
#
# 	Copyright (C) 2017 by Igor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import types
import _lcms2

TYPE_RGB_8 = "RGBA"
TYPE_RGB_16 = "RGBA;16"
TYPE_RGBA_8 = "RGBA"
TYPE_RGBA_16 = "RGBA;16"
TYPE_CMYK_8 = "CMYK"
TYPE_CMYK_16 = "CMYK;16"
TYPE_GRAY_8 = "L"
TYPE_GRAY_16 = "L;16"
TYPE_Lab_8 = "LAB"
TYPE_Lab_DBL = "LAB;float"
TYPE_XYZ_DBL = "XYZ;float"

INTENT_PERCEPTUAL = 0
INTENT_RELATIVE_COLORIMETRIC = 1
INTENT_SATURATION = 2
INTENT_ABSOLUTE_COLORIMETRIC = 3

cmsFLAGS_NOTPRECALC = 0x0100
cmsFLAGS_GAMUTCHECK = 0x1000
cmsFLAGS_SOFTPROOFING = 0x4000
cmsFLAGS_BLACKPOINTCOMPENSATION = 0x2000
cmsFLAGS_PRESERVEBLACK = 0x8000
cmsFLAGS_NULLTRANSFORM = 0x0200
cmsFLAGS_HIGHRESPRECALC = 0x0400
cmsFLAGS_LOWRESPRECALC = 0x0800

COLOR_BYTE = 0
COLOR_WORD = 1
COLOR_DBL = 2

class CmsError(Exception):
	pass

def COLORB(channel0=0, channel1=0, channel2=0, channel3=0):
	"""
	Emulates COLORB object from python-lcms.
	Actually function returns regular 4-member list.
	"""
	return [channel0, channel1, channel2, channel3, COLOR_BYTE]

def COLORW(channel0=0, channel1=0, channel2=0, channel3=0):
	"""
	Emulates COLORW object from python-lcms.
	Actually function returns regular 4-member list.
	"""
	return [channel0, channel1, channel2, channel3, COLOR_WORD]

def cmsCIEXYZ(channel0=0.0, channel1=0.0, channel2=0.0, channel3=0.0):
	"""
	Emulates cmsCIEXYZ object from python-lcms.
	Actually function returns regular 4-member list.
	"""
	return [channel0, channel1, channel2, channel3, COLOR_DBL]

def cmsCIELab(channel0=0.0, channel1=0.0, channel2=0.0, channel3=0.0):
	"""
	Emulates cmsCIELab object from python-lcms.
	Actually function returns regular 4-member list.
	"""
	return [channel0, channel1, channel2, channel3, COLOR_DBL]

def get_version():
	"""
	Returns LCMS version.
	"""
	ver = str(_lcms2.getVersion())
	return ver[0] + '.' + ver[2]


def cmsOpenProfileFromFile(profileFilename, mode=None):
	"""	
	Returns a handle to lcms2 profile wrapped as a Python object. 
	The handle doesn't require to be closed after usage because
	on object delete operation Python calls native cmsCloseProfile()
	function automatically  

	profileFilename - a valid filename path to the ICC profile
	mode - stub parameter for python-lcms compatibility
	"""
	if not os.path.isfile(profileFilename):
		raise CmsError, 'Invalid profile path provided: %s' % profileFilename

	result = _lcms2.openProfile(profileFilename)

	if result is None:
		msg = 'It seems provided profile is invalid'
		raise CmsError, msg + ': %s' % profileFilename

	return result

def cmsCreate_sRGBProfile():
	"""
	Returns a handle to lcms2 built-in sRGB profile.
	"""
	return _lcms2.createRGBProfile()

def cmsCreateXYZProfile():
	"""
	Returns a handle to lcms2 built-in XYZ profile.
	"""
	return _lcms2.createXYZProfile()

def cmsCreateLabProfile(val=None):
	"""
	Returns a handle to lcms2 built-in Lab profile.
	
	val - stub parameter for python-lcms compatibility
	"""
	return _lcms2.createLabProfile()

def cmsCreateGrayProfile():
	"""
	Returns a handle to lcms2 built-in Gray profile.
	"""
	return _lcms2.createGrayProfile()

def cmsCreateTransform(inputProfile, inMode,
					outputProfile, outMode,
					renderingIntent=INTENT_PERCEPTUAL,
					flags=cmsFLAGS_NOTPRECALC):
	"""
	Returns a handle to lcms2 transformation wrapped as a Python object.
	The handle doesn't require to be closed after usage because
	on object delete operation Python calls native cmsDeleteTransform()
	function automatically 

	inputProfile - a valid lcms profile handle
	inMode - predefined string constant 
			(i.e. TYPE_RGB_8, TYPE_RGBA_8, TYPE_CMYK_8, etc.)	
	outputProfile - a valid lcms profile handle	
	outMode - predefined string constant 
			(i.e. TYPE_RGB_8, TYPE_RGBA_8, TYPE_CMYK_8, etc.)		
	renderingIntent - integer constant (0-3) specifying rendering intent 
			for the transform
	flags - a set of predefined lcms flags
	"""

	if renderingIntent not in (0, 1, 2, 3):
		raise CmsError, 'renderingIntent must be an integer between 0 and 3'

	result = _lcms2.buildTransform(inputProfile, inMode,
								outputProfile, outMode,
								renderingIntent, flags)

	if result is None:
		msg = 'Cannot create requested transform'
		raise CmsError, msg + ": %s %s" % (inMode, outMode)

	return result

def cmsDoTransform(hTransform, inbuff, outbuff, val):
	"""
	Transform color values from inputBuffer to outputBuffer using provided 
	lcms transform handle.
	
	hTransform - a valid lcms transformation handle
	inbuff - 5-member list object.
	outbuff - 5-member list object with any values for recording 
					transformation results. Can be [0,0,0,0,0].
	val - stub parameter for python-lcms compatibility			              
	"""
	pass


def cmsDeleteTransform(transform):
	"""
	This is a function stub for python-lcms compatibility.
	Transform handle will be released automatically.
	"""
	pass


def cmsCloseProfile(profile):
	"""
	This is a function stub for python-lcms compatibility.
	Profile handle will be released automatically.
	"""
	pass