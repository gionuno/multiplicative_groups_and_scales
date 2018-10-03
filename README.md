# multiplicative_groups_and_scales
Based on Musical Scales and Multiplicative Groups by Donald Spector.
A crappy implementation in Python 2.7, using:

- pypianoroll to get the midi data.
- pyaudio, for, uhhh, audio.

So, it gets inverses of the set {1,2,3,4,5,6,7,8,9,10,11,12} under mod 13 multiplication and assigns a number to a tone.
eg: 1 -> C (Do), 3 -> D (Re), etc. Or 1 -> D (Re), 3 -> E (Mi), etc.

And using the midi data, we use a simple mapping for a given transformation for the tones, moving it within it's original octave using C -1 as the 0 in the midi chart.

I thought it was interesting, but maybe it's not so **A E S T H E T I C**ally pleasing. Maybe in the hands of an able composer it'd work.
