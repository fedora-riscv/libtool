# Makefile for source rpm: libtool
# $Id$
NAME := libtool
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
