import os
import sys
import threading
from datetime import datetime
from time import time, sleep

import requests
from lxml import html


class PSADownloader(object):

    def __init__(self):
        self.page_links = []
        self.counts = {}
        self.paths = []
        self._get_urls()
        self._make_dirs()

    def _get_urls(self):
        with open('links.txt', 'r') as fh:
            self.page_links = map(lambda x: x.strip(), fh.readlines())

        if not self.page_links:
            raise ValueError('No links found in links.txt.')
        else:
            self.counts['reports'] = len(self.page_links)

    def _make_dirs(self):
        root_dl_dir = os.path.join(os.getcwd(), 'Downloads')
        main_dl_dir = os.path.join(
            root_dl_dir,
            datetime.now().strftime('%Y-%m-%d\\%H.%M.%S')
        )

        for i in range(self.counts['reports']):
            path = os.path.join(main_dl_dir, '%03d' % (i + 1))
            os.makedirs(path)
            self.paths.append(path)

    def run(self):
        self.counts['total files found'] = 0
        self.counts['total files saved'] = 0
        self.totalsize = 0
        self.totaltime = 0

        self._print('Found %d pages' % self.counts['reports'])
        t_start = time()
        for idx, url in enumerate(self.page_links):
            self.idx = idx
            try:
                self._print('Now processing %s' % url)
                self.parse_page(url)
            except Exception as e:
                self._print('- %s' % e, level=1)
                continue

        self.totaltime = time() - t_start
        self._print('Finished.')
        self._show_summary()

    def parse_page(self, url):
        self.counts['files found'] = 0
        self.counts['files saved'] = 0

        page = requests.get(url)
        tree = html.fromstring(page.text)
        items = tree.xpath('//section[3]//a')

        if not items:
            raise ValueError('No attachments found.')
        else:
            self.counts['files found'] = len(items)
            self.counts['total files found'] += self.counts['files found']
            self._print(
                '- Found %d attachments.' % self.counts['files found'],
                level=1
            )

            self.download_files(items)
            self.counts['total files saved'] += self.counts['files saved']

    def download_files(self, items):
        for item in items:
            name = item.attrib.get('title', item.text)
            link = item.attrib.get('href')
            try:
                if link is None:
                    raise ValueError('File URL not available.')

                self._print('- Accessing %s' % name, level=2,
                            newline=False)

                r = requests.get(link, stream=True)

                if r.status_code == 200:
                    size = r.headers.get('Content-Length')
                    if not size:
                        raise ValueError('Files %s has size 0.' % name)

                    size = int(size)
                    path = os.path.join(self.paths[self.idx], name)

                    with open(path, 'wb') as f:
                        self.pct = ''
                        done = 0

                        e = threading.Event()
                        th = threading.Thread(
                            target=self._show_progress,
                            args=(e,)
                        )

                        th.start()
                        for chunk in r.iter_content(2048):
                            f.write(chunk)
                            done += float(len(chunk))
                            self.pct = '- Downloading %s [%0.1f%%]' % (
                                name, (done / size) * 100
                            )

                        self.counts['files saved'] += 1
                        self.totalsize += size
                        sleep(0.5)
                        e.set()
                else:
                    raise ValueError('Unable to download %s' % name)
            except Exception as e:
                self._print('- %s' % e, level=2, newline=False)
                self.counts['files skipped'] += 1
            finally:
                self._print()

    def _show_summary(self):
        counts = '{:25}{:>15}'
        values = '{:25}{:>15,.1f}'

        print '\n'
        print '{:^40}'.format('Summary')
        print 'Reports'
        print counts.format('  Accessed:', self.counts['reports'])
        print 'Attachments'
        print counts.format('  Accessed:',
                            self.counts['total files found'])
        print counts.format('  Downloaded:',
                            self.counts['total files saved'])
        print 'Others'
        print values.format('  Total file size (KB)',
                            self.totalsize / 1000)
        print values.format('  Total time (mins.)', self.totaltime / 60)

    def _print(self, prompt='', level=0, newline=True):
        sys.stdout.write('\r' + 2 * level * ' ' + prompt + newline * '\n')
        sys.stdout.flush()

    def _show_progress(self, e):
        while not e.is_set():
            self._print(self.pct, level=2, newline=False)
            e.wait(0.01)

if __name__ == '__main__':
    d = PSADownloader()
    d.run()
