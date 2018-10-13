# coding: utf-8
import re

LINE_TYPES = ["blank", "title", "period"]


class Hms(object):
    """
    A class te represent a time in hour, minute and seconds format
    """
    def __init__(self, h, m, s):
        self.hour = float(h)
        self.minute = float(m)
        self.second = float(s)

    def to_ms(self):
        """

        :return: the corresponding time in milliseconds
        """
        hours = self.hour * 60 * 60 * 1000
        minutes = self.minute * 60 * 1000
        seconds = self.second * 1000
        return hours + minutes + seconds


class ConsistencyError(Exception):
    pass


class Period(object):
    """
    Represents a period to cut and paste
    It contains a Hms begin and Hms end.
    """
    def __init__(self, begin, end, pitch=0., overlay=0.):
        self.begin = begin
        self.end = end
        self.pitch_rate = pitch
        self.overlay = overlay
        if begin.to_ms() >= end.to_ms():
            raise ConsistencyError


class Track(object):
    """
    Represents a track, with title, rank, and list of periods to cut/paste
    """
    def __init__(self, rank, title, periods=None):
        self.rank = rank
        self.title = title.lstrip()
        self.periods = periods if periods else []

    def __add__(self, other):
        """
        add a period to the track. Warning: other must be a Period

        :param other:
        :return:
        """
        if not isinstance(other, Period):
            raise ValueError
        self.periods.append(other)
        return self


class Disk(object):
    """
    Represents an audio disk, with tracks
    """
    def __init__(self, name, tracks=None):
        self.name = name
        self.tracks = tracks if tracks else []

    def __add__(self, other):
        """
        add a track to the Disk. Warning: other must be a Track

        :param other:
        :return:
        """
        if not isinstance(other, Track):
            raise ValueError
        self.tracks.append(other)
        return self


class Line(object):
    """
    Store the information of a line
    """
    def __init__(self, line_type):
        if line_type not in LINE_TYPES:
            raise ValueError
        self.line_type = line_type


class BlankLine(Line):
    """
    Store the information of a blank line
    """
    def __init__(self):
        Line.__init__(self, "blank")


class TitleLine(Line):
    """
    Store the information of a title line
    """
    def __init__(self, rank, text):
        Line.__init__(self, "title")
        self.rank = int(rank)
        self.text = text


class PeriodLine(Line):
    """
    Store the information of a period line
    """
    def __init__(self, begin, end, pitch=0., overlay=0.):
        Line.__init__(self, "period")
        self.begin = begin
        self.end = end
        self.pitch = pitch
        self.overlay = overlay


class ParseCutFile(object):
    """
    A tool that parses a file that contains an audio file cutting.
    Can compute the data in miliseconds instead of a (h m s) format
    """
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def parse_line(line):
        """

        :return: the line type (blank line, title, period), and the begin and
        end time, if period time
        """
        if line.isspace():
            return BlankLine()

        title = re.match(r"^([0-9]+)-(.+)$", line)
        if title:
            title_rank = title.group(1)
            title_text = title.group(2)
            return TitleLine(title_rank, title_text)

        period_regex = "^([0-9]{2})\D+([0-9]{2})\D+([0-9]{2}\.[0-9]+)\D+->"
        period_regex += "\D+([0-9]{2})\D+([0-9]{2})\D+([0-9]{2}\.[0-9]+)\D? "
        period_regex += "?((\+|-)[0-9]+\.?([0-9]*)?)?.*$"
        period = re.match(period_regex, line)

        if period:
            overlay = 0.
            if "chevaucher" in line:
                overlay = float(line.split("chevaucher=")[1][0])

            return PeriodLine(
                Hms(
                    period.group(1),
                    period.group(2),
                    period.group(3),
                ),
                Hms(
                    period.group(4),
                    period.group(5),
                    period.group(6),
                ),
                pitch=float(period.group(7)) if period.group(7) else 0.,
                overlay=overlay,
            )

        # if one get there, one consider a blank line
        return BlankLine()

    def parse_file(self, disk_name):
        """
        Parse the file an instantiate a Disk, that contains all needed
        information

        :return: a Disk
        """
        res_disk = Disk(disk_name)

        file_stream = open(self.file_path, "r")

        line = file_stream.readline()
        while line != '':
            the_line = self.parse_line(line)

            if the_line.line_type == "blank":
                line = file_stream.readline()
                continue

            if the_line.line_type == "title":
                current_track = Track(the_line.rank, the_line.text)
                res_disk += current_track
                line = file_stream.readline()
                continue

            if the_line.line_type == "period":
                current_track += Period(
                    the_line.begin,
                    the_line.end,
                    the_line.pitch,
                    the_line.overlay,
                )
                line = file_stream.readline()
                continue

        return res_disk
