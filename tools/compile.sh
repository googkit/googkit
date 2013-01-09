#!/bin/bash


CLOSUREBUILDER=closure/library/closure/bin/build/closurebuilder.py
COMPILER_FLAGS='--compilation_level=ADVANCED_OPTIMIZATIONS'
COMPILED_JS=script.min.js
NAMESPACE_MAIN=com.mycompany.Main


function setup_release_files() {
	rm -rf release
	mkdir -p release
	cp -R debug/* release

	# Remove lines that requires unneeded scripts
	sed -i '' -e '/closure\/goog\/base\.js/d' release/index.html
	sed -i '' -e '/goog\.require/d' release/index.html

	# Replace deps.js by a compiled script
	sed -i '' -e 's|js_dev/deps.js|'$COMPILED_JS'|g' release/index.html
}


function compile_scripts() {
	rm release/js_dev/deps.js
	python $CLOSUREBUILDER --root=closure/library --root=release/js_dev -n $NAMESPACE_MAIN -o compiled -c closure/compiler/compiler.jar --compiler_flags=$COMPILER_FLAGS --output_file=release/$COMPILED_JS

	rm -rf release/js_dev
}


cd $(dirname $0)/..
setup_release_files
compile_scripts
