# librivoxraw

### Author

Richard Bruce Baxter - Copyright (c) 2024 Baxter AI (baxterai.com)

### Description

Raw LibriVox audio data transcription using WhisperX

### License

MIT License

### Execution
```
python downloadLibrivoxAudioBooks.py
cp audiobooks/extract/*.mp3 transcribeIn/
python transcribeLibrivoxAudioBooks.py
[post-transcription rewrite: python convertJSONtoTXTW.py]
python convertLinesToSequenceLength.py
python generateNLPdataFiles.py
python convertNLPdataFilesTokeniseProsody.py
```
