# coding: utf-8
import os

from pydub import AudioSegment


class EditAudioFile(object):
    """
    Class to manage audio file editing
    """
    def __init__(self, audio_file_path):
        self.all_sound = AudioSegment.from_wav(audio_file_path)

    @staticmethod
    def pitch_sound_period_(period, pitch_rate):
        """
        take a sound and return the same sound with a pitch shift corresponding
        to the pitch_rate

        :param period: a pydub sound
        :param pitch_rate: the pitch rate (0.1 ~= 1/2 tone)
        :return: a pydub sound
        """
        octaves = 0.5
        new_sample_rate = int(
            period.frame_rate * (2.0 ** (octaves * pitch_rate))
        )
        return period._spawn(
            period.raw_data,
            overrides={'frame_rate': new_sample_rate}
        )

    def get_period(self, period):
        """

        :param period: file_parsing.Period
        :return: the period of self.all_sound corresponding to the period
        """
        sound_period = self.all_sound[period.begin.to_ms():period.end.to_ms()]
        sound_period = self.pitch_sound_period_(sound_period, period.pitch_rate)
        return sound_period

    def make_track(self, track_cut):
        """

        :param track_cut:
        :return:
        """
        res = self.get_period(track_cut.periods[0])
        for period in track_cut.periods[1:]:
            res = res.append(
                self.get_period(period),
                crossfade=period.overlay * 1000,
            )
        return res

    def make_disk(self, disk_cut, output_folder=None, cover=None, tags=None):
        """

        :param output_folder:
        :param disk_cut:
        :param cover:
        :param tags:
        :return:
        """
        for track_cut in disk_cut.tracks:
            track_num = "%02d" % track_cut.rank
            file_name = track_num + "- " + track_cut.title + ".wav"
            sound_track = self.make_track(track_cut)
            print(file_name)

            info_track = {
                "title": track_cut.title,
                "track": track_num,
            }
            if tags:
                info = {**info_track, **tags}
            else:
                info = info_track

            if cover:
                sound_track.export(
                    os.path.join(
                        output_folder,
                        file_name,
                    ) if output_folder else file_name,
                    format="wav",
                    tags=info,
                    cover=cover,
                )
            else:
                sound_track.export(
                    os.path.join(
                        output_folder,
                        file_name,
                    ) if output_folder else file_name,
                    format="wav",
                    tags=info,
                )