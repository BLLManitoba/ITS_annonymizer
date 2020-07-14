from __future__ import print_function
import re
import time
import json
import glob
import sys
import os


def load_replacements_file(filePath):  # 'replacement_dict.json'
    with open(filePath) as f:
        replacements = json.load(f)
    return replacements


def parse_file(inFile, outFile, replacements):
    with open(inFile, 'r') as inF:
        with open(outFile, 'w') as outF:

            # print('\n' + os.path.split(inFile)[1] + ':')

            for line in inF:
                for node in replacements.keys():
                    # print(line)
                    if re.search(r'<{}\b'.format(node), line):  # word boundary is important here
                        for name, value in replacements[node].items():
                            if isinstance(value,list):
                                if bool(value[1]["only_time"]) is True:
                                    line = re.sub(r'{}="[0-9\-]*'.format(name),
                                              r'{}="{}'.format(name, value[0]["replace_value"]),
                                              line)
                                    continue
                            
                            line = re.sub(r'{}="[a-zA-Z0-9_.:\-]*"'.format(name),
                                              r'{}="{}"'.format(name, value),
                                              line)
                        # print('\t- changed {}/{} to {}'.format(node, name, value))
                outF.write(line)


#if __name__ == '__main__':
def main(inDir, outDir, repFile):
    #print(sys.argv[1])
    #itsFolder = sys.argv[1]
    # itsFolder = "S:\Soderstrom-Lab\GitHubFiles\ITS_annonymizer\input_its_files"
    # print(itsFolder)
    itsFolder = inDir
    
    # Check that the its files directory exists
    if not os.path.isdir(itsFolder):
        raise Exception('Not a valid folder name')

    # Get paths of the its files
    files = glob.glob(os.path.join(itsFolder, '*.its'))
    if not files:
        raise Exception('There are no its files in the folder')

    # Make the output folder
    #outFolder = itsFolder + '_anonymised'
    #if os.path.isdir(outFolder):
    #    raise Exception('The output folder already exists, please consider delete/renaming it.')
    #else:
    #    os.mkdir(outFolder)
    outFolder = outDir
    if not os.path.isdir(outFolder):
        raise Exception('Not a valid folder name')
    
    # Load the replacements dictionary
    #replacements = load_replacements_file('./partial_replacements_dict.json')
    replacements = load_replacements_file(repFile)

    # Process all files
    for inFile in files:
        _, name = os.path.split(inFile)
        outFile = os.path.join(outFolder, name)

        parse_file(inFile, outFile, replacements)
        print('done {}'.format(name))

    print('\n-----\nProcessed {} files'.format(len(files)))
