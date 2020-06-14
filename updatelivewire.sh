set -x 
TMPDIR=$(mktemp -d )
wget https://github.com/livewire/livewire/archive/master.zip -O $TMPDIR/master.zip

7z x $TMPDIR/master.zip -o$TMPDIR
cp -rf $TMPDIR/livewire-master/js/* livewire/static/livewire/
