import re
import codecs
import datetime
from pprint import pprint

EOR = u"=========="

def records(file_path):
    clip_file = codecs.open( file_path )
    clip_file.seek( 3 ) # skip magic cookie

    record = list()
    for line in clip_file:
        line = line.decode( 'utf-8' )
        if line.strip() == EOR:

            assert record[2] == '', "Non-blank line expected separating the header from the body of the clipping:%s" % record[2]

            clip = dict()

            # --- line 1

            match = re.match( r'(.*?)\((.*)\)', record[0] )
            clip['title'], clip['attribution'] =match.groups()
            clip['title'] = clip['title'].strip()
            clip['attribution'] = clip['attribution'].split( ') (' )
            
            # dumb parenthesis
            if len( clip['attribution'] ) > 1:
                clip['title'] += ' (%s)' % clip['attribution'][0]
                clip['title'] = clip['title'].strip()
            
            # cleanup
            clip['attribution'] = clip['attribution'][-1].strip()

            # --- line 2

            line2 = record[1].split( '|' )

            # type and page
            match = re.match( r'- (\w+) on Page (\d+)', line2[0].strip() )
            clip['type'], page = match.groups()
            clip['page'] = int( page )
            
            # location (if present)
            if len( line2 ) > 2:
                match = re.match( r'Loc. ([^|]+)', line2[1].strip() )
                location = match.groups()[0]
                location = location.strip().split('-')
                if len( location ) is 1:
                    clip['location'] = int( location[0] )
                else:
                    locmin = int( location[0] )
                    ndigit = len( location[1] )
                    locmax = int( locmin / 10**ndigit ) * 10**ndigit + int( location[1] )
                    clip['location'] = ( locmin, locmax )
                
            # date
            match = re.match( r'Added on (\w+), (.*)', line2[-1].strip() )
            dow, timestamp = match.groups()
            clip['datetime'] = datetime.datetime.strptime( timestamp, '%B %d, %Y, %I:%M %p' )

            # match = re.match( r'- (\w+) Loc. ([^|]+)\| Added on (\w+), (\w+ \d+, \d+), (\d+:\d+ \w\w)', record[1] )
            # clip['type'], clip['location'], clip['dow'], clip['date'], clip['time'] = match.groups()

            # --- main body content

            clip['body'] = "\n".join( record[3:] )

            # yield and reset for next record
            yield clip
            record = list() 
        else:
            record.append( line.strip() )

    clip_file.close()



if __name__ == '__main__':
    from sys import argv
    for n,r in enumerate( records(argv[1] ) ): #'My Clippings.txt') ):
        print n, 
        pprint( r )


