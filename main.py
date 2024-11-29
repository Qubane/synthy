import math
from collections.abc import Callable

import pyaudio


class Application:
    """
    Main application class
    """

    def __init__(self, sample_rate: int, bit_width: int):
        # values
        self.bit_width: int = bit_width
        self._max_int: int = 2 ** self.bit_width - 1
        self.sample_rate: int = sample_rate

        # instance pyaudio
        self.pyaudio = pyaudio.PyAudio()

        # open stream
        self.stream = self.pyaudio.open(
            format=self.pyaudio.get_format_from_width(self.bit_width // 8, True),
            channels=1,
            rate=self.sample_rate,
            output=True)

    def run(self) -> None:
        """
        Runs the application
        """

        self.play_sine(100, 1)
        self.play_tri(100, 1)
        self.play_saw(100, 1)
        self.play_square(100, 1)

    def stop(self) -> None:
        """
        Stops the application
        """

        self.stream.close()
        self.pyaudio.terminate()

    @staticmethod
    def clamp(value: float, min_: float = 0, max_: float = 1) -> float:
        """
        Clamps the value between 0 and 1
        :param value: value
        :param min_: minimum
        :param max_: maximum
        :return: clamped value
        """

        return min(max_, max(min_, value))

    def play_lambda(self, f: Callable, time: float, amp: float = 1) -> None:
        """
        Plays a given function, mapped to '[range (0 - 1)] * [time]'
        :param f: a function
        :param time: time (ms)
        :param amp: amplitude (range 0.0 - 1.0)
        """

        sample_count = int(self.sample_rate * time)
        mapped_function = map(f, [x / self.sample_rate for x in range(sample_count)])
        clamped_function = [int(self.clamp(val, max_=amp) * self._max_int) for val in mapped_function]
        self.stream.write(bytes(clamped_function))

    def play_sine(self, freq: float, time: float, amp: float = 1) -> None:
        """
        Plays a sine wave with a given frequency.
        :param freq: frequency (hz)
        :param time: time (ms)
        :param amp: amplitude (range 0.0 - 1.0)
        """

        self.play_lambda(lambda x: math.sin(x * freq * math.tau) / 2 + 0.5, time, amp)

    def play_tri(self, freq: float, time: float, amp: float = 1) -> None:
        """
        Plays a triangle wave with a given frequency.
        :param freq: frequency (hz)
        :param time: time (ms)
        :param amp: amplitude (range 0.0 - 1.0)
        """

        self.play_lambda(lambda x: abs((x * 2 * freq % 2) - 1), time, amp)

    def play_saw(self, freq: float, time: float, amp: float = 1) -> None:
        """
        Plays a sawtooth wave with a given frequency.
        :param freq: frequency (hz)
        :param time: time (ms)
        :param amp: amplitude (range 0.0 - 1.0)
        """

        self.play_lambda(lambda x: x * freq % 1, time, amp)

    def play_square(self, freq: float, time: float, amp: float = 1) -> None:
        """
        Plays a square wave with a given frequency.
        :param freq: frequency (hz)
        :param time: time (ms)
        :param amp: amplitude (range 0.0 - 1.0)
        """

        self.play_lambda(lambda x: ((x * freq % 1) - (x * freq % 0.5)) * 2, time, amp)


def main():
    app = Application(sample_rate=100000, bit_width=8)
    app.run()
    app.stop()


if __name__ == '__main__':
    main()
