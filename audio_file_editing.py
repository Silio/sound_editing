# coding: utf-8
from pydub import AudioSegment


class EditAudioFile(object):
    """
    Class to manage audio file editing
    """
    def __init__(self, audio_file_path):
        self.audio_file = AudioSegment.from_wav(audio_file_path)

    def get_period(self, period):
        """

        :param period: file_parsing.Period
        :return: the period of self.audio_file corresponding to the period
        """
        return self.audio_file[period.begin.to_ms():period.end.to_ms()]

    def make_track(self, track_cut):
        """

        :param track_cut:
        :return:
        """
        return sum([self.get_period(period) for period in track_cut.periods])
