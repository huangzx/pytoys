#!/usr/bin/env python
# -*- coding: utf8 -*-
#------------------------------------------------------------------------------

import urllib

def downloadFile(fileUrl, fileToSave, needReport=False):
    ''' download from fileUrl then save to fileToSave

    the caller should make sure the fileUrl is a valid internet resource/file

    '''
    isDownOK = False
    downloadingFile = ''

    def reportHook(copiedBlocks, blockSize, totalFileSize):
        # totalFileSize
        # maybe -1 on older FTP servers which do not return a file size in response to a retrieval request
        if copiedBlocks == 0:
            print 'Begin to download {}, total size is {}'.format(downloadingFile, totalFileSize)
        else: 
            print 'Downloaded bytes: {}'.format(blockSize * copiedBlocks)
        return
    try:
        if fileUrl:
            downloadingFile = fileUrl
            if needReport:
                urllib.urlretrieve(fileUrl, fileToSave, reportHook);
            else:
                urllib.urlretrieve(fileUrl, fileToSave);
            isDownOK = True
        else:
            print "Input download file url is NULL"
    except urllib.ContentTooShortError(msg):
        isDownOK = False;
    except:
        isDownOK = False;
    return isDownOK;


if __name__ == '__main__':
    dstPicFile = 'test.jpg'
    curUrl = 'http://img2.cache.netease.com/photo/0001/2013-03-19/8QA0UTSV3R710001.jpg'
    if dstPicFile and curUrl:
        downloadFile(curUrl, dstPicFile, needReport=True)
