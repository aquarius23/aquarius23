#!/bin/sh

PREFIX=/usr/local/cross-tools
if [ "$TARGET" = "" ]; then
    TARGET=i586-mingw32msvc
fi
PATH="$PREFIX/bin:$PREFIX/$TARGET/bin:$PATH"
export PATH
exec make $*
