'''
    Goal: Functions that deal with Name of file
'''

# return file name without extension
def cutExtension(fileName):
    idx = fileName.rfind('.')
    nameWithoutExtension = fileName[:idx]
    # print('fileName: {}, fileName after cut extension: {}'.format(fileName, nameWithoutExtension))
    return nameWithoutExtension

# get extension of the file name
def getExtension(fileName):
    idx = fileName.rfind('.')
    if idx == -1:
        # print('Error: input file name: {} does not have extension'.format(fileName))
        return ''
    extension = fileName[idx + 1:]
    # print('fileName {} -> extension: {}'.format(fileName, extension))
    return extension
