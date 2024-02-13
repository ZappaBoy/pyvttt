# pyvttt

`pyvttt` is a simple Video-to-Text Transcriber written in Python.

## Installation

This tool uses [poetry](https://python-poetry.org/) to manage dependencies and packaging. To install all the
dependencies simply run:

``` shell
poetry install
```

`pyvttt` uses gpu support by default if it's available. There is no need of any additional dependencies for `Nvidia`
gpus.
If you have an `AMD` gpu you can install the `ROCm` dependencies uncommenting the `torch` and `torchvision` specific
lines in
the `pyproject.toml` file and running the following command:
``` shell
poetry lock && poetry install
```

Don't forget to set the `ROCm` environment variable based on your system configuration. Example for `ROCm (6.0.0)`
and `AMD 6700XT` gpu:

``` shell
export HSA_OVERRIDE_GFX_VERSION=10.3.0
```

## Usage

You can run the tool using poetry:

``` shell
poetry run pyvttt --help
```

Or you can run the tool using python:

``` shell
python -m pyvttt --help
```

Or you can run the tool directly from the directory or add it to your path:

``` shell
pyvttt --help
```

```shell
usage: pyvttt [-h] [--verbose] [--debug] [--quiet | --no-quiet | -q] [--version] [--url URL] [--file FILE] [--output OUTPUT] [--stdout | --no-stdout | -s] [--threads THREADS]

pyvttt is a simple Video-to-Text Transcriber written in Python.

options:
  -h, --help            show this help message and exit
  --verbose, -v         Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).
  --debug               Enable debug mode.
  --quiet, --no-quiet, -q
                        Do not print any output/log
  --version             Show version and exit.
  --url URL, -u URL     URL of the video to download and transcribe.
  --file FILE, -f FILE  Path to file with urls to download and transcribe.
  --output OUTPUT, -o OUTPUT
                        Path to save the transcription.
  --stdout, --no-stdout, -s
  --threads THREADS, -t THREADS
                        Number of threads to use. Default is half of the available cores.
```

## Transcribe single video by url

```shell
# note the double quotes around the url
pyvttt --url "youtube_url" --output transcription.txt
```

## Translate the transcription

You can choose to translate the audio transcription using the `--translate` option:

```shell
pyvttt --url "youtube_url" --output transcription.txt --translate it
# or
pyvttt --url "youtube_url" --output transcription.txt --translate italian
```

### Supported languages

```text
- arabic (ar)
- czech (cs)
- german (de)
- english (en)
- spanish (es)
- estonian (et)
- finnish (fi)
- french (fr)
- gujarati (gu)
- hindi (hi)
- italian (it)
- japanese (ja)
- kazakh (kk)
- korean (ko)
- lithuanian (lt)
- latvian (lv)
- burmese (my)
- nepali (ne)
- dutch (nl)
- romanian (ro)
- russian (ru)
- sinhala (si)
- turkish (tr)
- vietnamese (vi)
- chinese (zh)
- afrikaans (af)
- azerbaijani (az)
- bengali (bn)
- persian (fa)
- hebrew (he)
- croatian (hr)
- indonesian (id)
- georgian (ka)
- khmer (km)
- macedonian (mk)
- malayalam (ml)
- mongolian (mn)
- marathi (mr)
- polish (pl)
- pashto (ps)
- portuguese (pt)
- swedish (sv)
- swahili (sw)
- tamil (ta)
- telugu (te)
- thai (th)
- tagalog (tl)
- ukrainian (uk)
- urdu (ur)
- xhosa (xh)
- galician (gl)
- slovene (sl)
```

## Transcribe multiple videos reading urls from a file

You can run `pyvttt` on multiple videos by using file with urls:

```bash
first_video_url_here
second_video_url_here
# this is a commented line that will be ignored
third_video_url_here
```
```shell
pyvttt --file urls.txt --output transcriptions
```

## Use more threads

```shell
pyvttt [...] --threads 16
```

## Development

### Testing

To run the tests simply run:

``` shell
poetry run test
```

### Update `setup.py`

To update the `setup.py` file with the latest dependencies and versions run:

``` shell
poetry run poetry2setup > setup.py
```

## Acknowledgements

This project was generated using powerful tools and libraries such as [poetry](https://python-poetry.org/),
[pydantic](https://docs.pydantic.dev/latest/), [pytest](https://docs.pytest.org/en/stable/), [openai-whisper](https://github.com/openai/whisper), [pytube](https://github.com/pytube/pytube)
and more, I simply put the
pieces together. Please check and support all the tools and libraries used in this project.