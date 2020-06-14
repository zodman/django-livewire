set -x 
TMPDIR=$(mktemp -d )
DESTDIR=livewire/static/livewire
wget https://github.com/livewire/livewire/archive/master.zip -O $TMPDIR/master.zip

7z x $TMPDIR/master.zip -o$TMPDIR
cp -rf $TMPDIR/livewire-master/js/* $DESTDIR/src
mkdir -p $DESTDIR/dist/
npm run build
