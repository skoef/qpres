#!/usr/bin/env python

# vim: set noexpandtab

import getopt
import os, textwrap, sys, tty, termios

class QPres:
	def __init__(self):
		# set defaults
		self.title = 'Qpres'
		self.columns = 80
		self.lines = 25
		self.footer = 'github.com/skoef/qpres'
		self.showPages = False
		self.pagesPrefix = 'Page '

		self.index = 0
		self.pages = []

	def readStroke(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

	def getHeader(self):
		left = self.title.ljust((self.columns/2))
		right = ''
		if self.showPages:
			position = '%d/%d' % (self.index + 1, len(self.pages))
			right = (self.pagesPrefix + position).rjust((self.columns/2))
		return left + right + "\n" + ('-' * self.columns)

	def getFooter(self):
		return ('-' * self.columns) + "\n" + self.footer.rjust(self.columns)

	def run(self):
		while True:
			# clear screen
			os.system('clear')

			try:
				currentPage = self.pages[self.index]
			except IndexError:
				print "page %d could not be found" % self.index
				sys.exit(2)

			try:
				# open page content
				file = open(currentPage, 'r')
			except IOError:
				print 'error: could not open %s' % currentPage
				break

			# display header
			print self.getHeader()

			# display text
			screenbuf = []
			for line in file.readlines():
				screenbuf = screenbuf + textwrap.wrap(line, self.columns)
			print "\n".join(screenbuf[:(self.lines - 4)])

			# fill screen
			fill = max(0, (self.lines - 4) - len(screenbuf) - 1)
			print "\n" * fill

			# display footer
			print self.getFooter()

			# get user input
			command = self.readStroke()
			# next
			if (command == 'l' or command == ' ') and self.index < (len(self.pages) - 1):
				self.index = self.index + 1
			# previous
			elif command == 'j' and self.index > 0:
				self.index = self.index - 1
			# quit
			elif command == 'q':
				break

def usage():
	print """Usage: %s [-t title] [-f footer] [-l lines] [-c columns] slide.txt [slide2.txt [slide3.txt]]

	-t title   : title of the presentation                     [default: Qpres]
	-f footer  : footer text                                   [default: link to github]
	-l lines   : number of lines to use for the presentation   [default: 25]
	-c columns : number of columns to use for the presentation [default: 80]
	-p         : show pages in upper right corner              [default: False]
	-h         : show this help message
	""" % os.path.basename(sys.argv[0])

if __name__ == '__main__':
	# parse command line
	try:
		opts, args = getopt.getopt(sys.argv[1:], 't:f:l:c:ph', [])
	except getopt.GetoptError, e:
		print "Error: %s" % e
		usage()
		sys.exit(2)

	q = QPres()
	for o,a in opts:
		if o == '-t':
			q.title = a
		elif o == '-f':
			q.footer = a
		elif o == '-l':
			q.lines = int(a)
		elif o == '-c':
			q.columns = int(a)
		elif o == '-p':
			q.showPages = True
		elif o == '-h':
			usage()
			sys.exit(0)

	q.pages = args
	q.run()
