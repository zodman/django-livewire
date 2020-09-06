set -x 
TMPDIR=$(mktemp -d )
DESTDIR=livewire/static/livewire
wget https://github.com/livewire/livewire/archive/1.x.zip -O $TMPDIR/master.zip

7z x $TMPDIR/master.zip -o$TMPDIR
rm -rf $DESTDIR/src/*
cp -rf $TMPDIR/livewire-1.x/js/* $DESTDIR/src
mkdir -p $DESTDIR/dist/
npm run build
