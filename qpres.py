#!/usr/bin/env python

import os, textwrap, sys, tty, termios

class QPres:
	def __init__(self, pages):
		# set defaults
		self.title = 'Qpres'
		self.columns = 80
		self.lines = 25
		self.footer = 'github.com/skoef/qpres'
		self.showPages = True
		self.pagesPrefix = 'Page '

		self.index = 0
		self.pages = pages

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

			currentPage = self.pages[self.index]
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

# get terminal size
import struct, fcntl
size = struct.unpack('hh', fcntl.ioctl(0, termios.TIOCGWINSZ, '1234'))

q = QPres(['slide0.txt', 'slide1.txt', 'slide2.txt'])
q.title = 'My presentation'
q.lines = int(size[0]) - 1
q.columns = int(size[1])
q.run()
