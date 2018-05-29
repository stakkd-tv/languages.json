#!/usr/bin/python3


class CsvWriter(object):

    def __init__(self, file):  # Expects an open file
        self.file = file

    def write_row(self, *values):
        for index, value in enumerate(values):
            self.file.write(value)
            if index < len(values) -1:
                self.file.write(',')
        self.file.write('\n')
