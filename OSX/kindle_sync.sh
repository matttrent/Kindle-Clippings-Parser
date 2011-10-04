#! /bin/bash
if [ -d /Volumes/Kindle/documents ]
then
    # /bin/date >> /tmp/kindle_date
    cp /Volumes/Kindle/documents/My\ Clippings.txt $HOME/Archive/Filing/kindle
    cd $HOME/Archive/Filing/kindle
    git commit -am "Updating clippings"
fi

