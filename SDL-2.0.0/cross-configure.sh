#!/bin/sh

CONFIG_SHELL=/bin/sh
export CONFIG_SHELL
PREFIX=/usr/local/cross-tools
if [ "$TARGET" = "" ]; then
    TARGET=i586-mingw32msvc
fi
PATH="$PREFIX/bin:$PREFIX/$TARGET/bin:$PATH"
export PATH
if [ -f "$PREFIX/$TARGET/bin/$TARGET-sdl-config" ]; then
    SDL_CONFIG="$PREFIX/$TARGET/bin/$TARGET-sdl-config"
    export SDL_CONFIG
fi
cache=cross-config.cache
if [ -f configure ]; then
    CONFIGURE=configure
elif [ -f ../configure ]; then
    CONFIGURE=../configure
else
    echo "Couldn't find configure - aborting!"
    exit 2
fi
sh $CONFIGURE --cache-file="$cache" \
	--target=$TARGET --host=$TARGET --build=i386-linux \
	--prefix=$PREFIX/$TARGET $*
status=$?
rm -f "$cache"
exit $status
