#!/usr/bin/env python
# -*- coding: utf8 -*-
#

import urllib


def download_file(file_url, file_to_save, needs_report=False):
    ''' download from file_url then save to file_to_save

    the caller should make sure the file_url is a valid internet resource/file

    '''
    is_download_ok = False
    downloading_file = ''

    def _report_hook(copied_blocks, block_size, total_file_size):
        # total_file_size
        # maybe -1 on older FTP servers which do not return a file size in response to a retrieval request
        if copied_blocks == 0:
            print 'Begin to download {}, total size is {}'.format(downloading_file, total_file_size)
        else: 
            print 'Downloaded bytes: {}'.format(block_size * copied_blocks)
        return
    try:
        if file_url:
            downloading_file = file_url
            if needs_report:
                urllib.urlretrieve(file_url, file_to_save, _report_hook)
            else:
                urllib.urlretrieve(file_url, file_to_save)
            is_download_ok = True
        else:
            print "Input download file url is NULL"
    except urllib.ContentTooShortError:
        is_download_ok = False
    except:
        is_download_ok = False
    return is_download_ok


def main():
    '''

    '''
    dst_pic_file = 'PKGBUILD'
    cur_url = 'https://projects.archlinux.org/svntogit/community.git/plain/fcitx-googlepinyin/trunk/PKGBUILD'
    if dst_pic_file and cur_url:
        download_file(cur_url, dst_pic_file, True)


if __name__ == '__main__':
    main()
