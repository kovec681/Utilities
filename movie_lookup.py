#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  movie_lookup.py
#  
#  Copyright 2021 Seth Borkovec <kovec@AMD-LXCute>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Abstract:
#  Takes in a list of movie titles, gets information about it on IMDB.com,
#  and saves this to a tab-separated values file. A TSV file format is
#  used because some movie titles contain commas but a TSV can still be
#  imported to a spreadsheet.
#
#  Requirements:
#  1. Each movie title should be on a separate line.
#  2. If the input file already has more information separated by tabs,
#     it must be in this format:
#     title <TAB> year <TAB> IMDB url <TAB> media type <NEWLINE>
#  3. Any of the information in the above line may be omitted, except
#     for the tabs.
#
#  Output:
#  Saves a TSV file for a list of movies where each is in this format:
#     title <TAB> year <TAB> IMDB url <TAB> media type <NEWLINE>
#
#  Note:
#  This script will fail to work if IMDB changes their HTML that this
#  script is made to parse.
#
#  Usage:
#  python3 movie_lookup.py <input file> <output TSV file>

import os, requests


def main(args):
    
    # Check usage
    if len(args) != 3:
        print('USAGE: python3 movie_lookup.py <input file> <output TSV file>')
    else:
        # Read the TSV file
        print('Attempting to import ' + args[1])
        f = open(args[1], 'r')
        lines = f.readlines()
        f.close()
        
        # Make sure the TSV file isn't empty
        if len(lines) == 0:
            print('ERROR: Nothing in the list')
        else:
            # Parse the line for lookup
            defaultMedia = 'DVD'
            
            # Determine if the header line is present
            if lines[0][0:len('Title')] != 'Title':
                startIndex = 0
            else:
                startIndex = 1
            
            # Parse all movie entries in the list
            for index in range(startIndex, len(lines)):
                entry = lines[index].split('\t')
                
                # Title
                if len(entry) > 0:
                    title = entry[0].strip()
                else:
                    title = ''
                
                # Year
                if len(entry) > 1:
                    year = entry[1].strip()
                else:
                    year = ''
                
                # IMDB URL
                if len(entry) > 2:
                    imdb = entry[2].strip()
                else:
                    imdb = ''
                
                # Media type (DVD, BD, VHS, etc...)
                if len(entry) > 3:
                    media = entry[3].strip()
                else:
                    media = ''
                
                # Skip any blank lines
                if title != '':
                    updateEntry = True
                    
                    # Ask to skip current entry if all fields present
                    if (year != '') and (imdb != '') and (media != ''):
                        print('\nMovie: "' + title + '"\t(' + year + ')\t"' + imdb + '"\t' + media)
                        answer = ' '
                        while answer != '' and answer != 'n' and answer != 'y':
                            answer = input('Do you want to update this movie (y/n, default is No)? ').lower()
                            updateEntry = answer != '' and answer != 'n'
                    
                    if updateEntry:
                        # Look up title and get result
                        print('\nLooking up "' + title + '"')
                        r = requests.get('https://www.imdb.com/find?q=' + title)
                        result = getMovieResult(r.text, title)
                        
                        # Get the data if a result was chosen
                        if len(result) > 3:
                            # Get official title
                            title = result[0]
                            
                            # Get year
                            if year == '':
                                year = result[1]
                            
                            # Get url
                            if imdb == '':
                                imdb = 'https://www.imdb.com/title/' + result[2]
                        
                        # Set the media type (DVD, BD, VHS, etc...)
                        while media == '':
                            media = input('Input the media type for "' + title + '" (Press ENTER for "' + defaultMedia + '"): ')
                            if media == '':
                                media = defaultMedia
                            else:
                                defaultMedia = media
                
                # Save the movie entry
                lines[index] = title + '\t' + year + '\t' + imdb + '\t' + media + '\n'
            
            # Write the TSV to the file
            print('Writing new TSV to ' + args[2])
            f = open(args[2], 'w')
            for line in lines:
                f.write(line)
            f.close()
            print('Finished')
    
    return 0

def getMovieResult(responseText, query):
    lines = responseText.split('\n')
    
    # Parse the HTTP response text for the options
    for index in range(0, len(lines)):
        if lines[index] == '<h3 class="findSectionHeader"><a name="tt"></a>Titles</h3>':
            resultsLine = lines[index + 2]
            
            # Find all options in the results
            tdStartIndex = 0
            resultsList = []
            while tdStartIndex != -1:
                # Find the <td> with the result
                tdStartIndex = resultsLine.find('<td class="result_text">', tdStartIndex)
                if tdStartIndex != -1:
                    # Find the url
                    aIndex = resultsLine.find('<a', tdStartIndex + len('<td class="result_text">'))
                    url = resultsLine[(aIndex + len('<a href="/title/')):(aIndex + len('<a href="/title/tt0416449/'))]
                    
                    # Find the title
                    titleEndIndex = resultsLine.find('</a>', tdStartIndex + len('<td class="result_text">'))
                    title = resultsLine[(aIndex + len('<a href="/title/tt0416449/" >')):titleEndIndex]
                    
                    # Find the year
                    yearStartIndex = resultsLine.find('(', titleEndIndex)
                    yearEndIndex = resultsLine.find(')', titleEndIndex)
                    year = resultsLine[(yearStartIndex + 1):yearEndIndex]
                    
                    # Get the rest of the information about tv series or other media format
                    mediaStartIndex = resultsLine.find('(', yearEndIndex, yearEndIndex + 3)
                    media = '(' + year + ')'
                    if mediaStartIndex > 0:
                        mediaEndIndex = resultsLine.find(')', mediaStartIndex)
                        media += ' ' + resultsLine[mediaStartIndex:(mediaEndIndex + 1)]
                        
                    # Add to the results list
                    resultsList.append([title, year, url, title + ' ' + media])
                    tdStartIndex += 1
                    
            # Check if any results were found
            if len(resultsList) == 0:
                print('WARNING: No results for "' + query + '"')
                return []
            else:
                # Let the user choose which result to use
                for resultIndex in range(0, len(resultsList)):
                    print(str(resultIndex + 1) + ': ' + resultsList[resultIndex][3])
                selection = -1
                while not int(selection) in range(0, len(resultsList)):
                    selection = input('Select a result from the list (choose the corresponding number or press ENTER to skip): ')
                    if selection == '':
                        break
                    if int(selection) - 1 in range(0, len(resultsList)):
                        return resultsList[int(selection) - 1]
                    else:
                        print('ERROR: Invalid selection: ' + selection)
            break
    return []

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
