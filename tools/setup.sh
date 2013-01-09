#!/bin/bash


function setup_closure_library() {
	mkdir -p closure

	if which svn > /dev/null; then
		svn checkout http://closure-library.googlecode.com/svn/trunk closure/library
	elif which git > /dev/null; then
		git clone https://github.com/jarib/google-closure-library closure/library
	else
		echo '[Error] Git or Subversion not found.'
		echo 'Please install one of them to download Closure Library.'
	fi
}


function setup_closure_compiler() {
	mkdir -p tmp

	if which curl > /dev/null; then
		export ALL_PROXY=$HTTP_PROXY
		curl http://closure-compiler.googlecode.com/files/compiler-latest.zip > tmp/compiler.zip
	else
		echo '[Error] Curl not found.'
		echo 'Please install it to download Closure Compiler.'
		exit 1
	fi

	mkdir -p closure/compiler
	unzip  tmp/compiler.zip -d closure/compiler

	rm -rf tmp
}


cd $(dirname $0)/..

echo 'Downloading Closure Library...'
setup_closure_library

echo 'Downloading Closure Compiler...'
setup_closure_compiler
