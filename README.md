# subtitles-translation

## Info

This is a repository for the collective translation of subtitle files.

We use the "self-proclaimed" multilanguage SRT format (.msrt) where each line has prefix indicating translation language:

```
5
00:00:26,640 --> 00:00:30,640
[rus] Кажется, я снова уснула с открытым окном...
[eng] It seems I feel asleep with the window open, again...
[spa] Al parecer me quedé dormida con la ventana abierta de nuevo...

6
00:00:32,360 --> 00:00:35,360
[rus] Уфф... Как дует то...
[eng] Oh... It so windy...
[spa] Oh... Cuánto viento...
```

NOTE: The language codes are defined according to [ISO 639-3 standard](https://en.wikipedia.org/wiki/ISO_639:a)

With this repository we also provide special utilities to work with msrt files. These can be found in the `tools/` folder. `msrt_tool.py` can extract any language to a regular SRT subtitle file like this:

```bash
./tool/msrt_tool.py pepper-and-carrot-ep6.msrt eng -o pepper-and-carrot-ep6-en.srt
```

and `msrt_embed.py` allows you to embed some or all of the languages of an msrt subtitle file into an video file (.mkv, .mp4, or .mov). The basic usage looks like this:

```bash
./tool/msrt_embed.py morevna-ep3.msrt ~/Downloads/morevna-episode-3.0.1.mp4 --language eng rus --default eng
```

however there are many more options you can explore with `./tool/msrt_embed --help`.

## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
