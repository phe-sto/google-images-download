#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
Test the google_images_download with pytest.
"""
import shlex
from subprocess import Popen, PIPE

import pytest

from google_images_download import google_images_download

FOLDER = 'downloads'


# @pytest.mark.skip
@pytest.mark.parametrize("arguments", [
    ({
        "keywords": "Polar bears",
        "limit": 2,
        "print_urls": False
    }),
    ({
        "keywords": "Bear",
        "limit": 1,
        "print_urls": True
    }),
    ({
        "keywords": "Bear",
        "limit": 1,
        "prefix_keywords": "black"
    }),
    ({
        "keywords": "Bear",
        "limit": 1,
        "suffix_keywords": "mountain"
    }),
    ({
        "keywords": "Car",
        "limit": 1,
        "color": "red",
        "format": "jpg"
    }),
    ({
        "keywords": "Car",
        "limit": 1,
        "color_type": "black-and-white"
    }),
    ({
        "keywords": "Car",
        "limit": 1,
        "color_type": "full-color"
    }),
    ({
        "keywords": "Car",
        "limit": 1,
        "color_type": "transparent"
    }),
    ({
        "keywords": "Plane",
        "limit": 1,
        "usage_rights": "labeled-for-reuse-with-modifications"
    }),
    ({
        "keywords": "Plane",
        "limit": 1,
        "usage_rights": "labeled-for-noncommercial-reuse-with-modification"
    }),
    ({
        "keywords": "Plane",
        "limit": 1,
        "usage_rights": "labeled-for-reuse"
    }),
    ({
        "keywords": "Plane",
        "limit": 1,
        "usage_rights": "labeled-for-nocommercial-reuse"
    }),

    ({
        "keywords": "Bird",
        "limit": 1,
        "related_images": ""
    }),

    ({
        "keywords": "Bird",
        "limit": 1,
        "ri": ""
    }),
    ({
        "keywords": "House",
        "limit": 2,
        "offset": 1}),
    ({
        "keywords": "Flat",
        "limit": 1,
        "no_numbering": ""}),

    ({
        "keywords": "Castle",
        "limit": 1,
        "safe_search": ""}),
    ({
        "keywords": "Boat",
        "limit": 1,
        "thumbnail": ""}),
    ({
        "keywords": "Castle",
        "limit": 1,
        "language": "French"}),
    ({
        "keywords": "Lake",
        "limit": 1,
        "p": "",
        "ps": "",
        "m": "",
        "pp": "",
    }),
    ({
        "keywords": "Person",
        "limit": 1,
        "type": "face", }),

    ({
        "keywords": "Dog",
        "limit": 1,
        "type": "photo", }),

    ({
        "keywords": "Dog",
        "limit": 1,
        "type": "clipart", }),

    ({
        "keywords": "Dog",
        "limit": 1,
        "type": "line-drawing", }),

    ({
        "keywords": "Dog",
        "limit": 1,
        "type": "animated", }),

    ({
        "keywords": "Dog",
        "limit": 1,
        "time_range": {"time_min": "09/01/2013", "time_max": "01/01/2019"}}),

    ({
        "keywords": "Dog",
        "limit": 1,
        "delay": 3}),  # output_directory
    ({
        "keywords": "Dog",
        "limit": 1,
        "specific_site": "https://pixabay.com", }),
    ({
        "keywords": "Dog",
        "limit": 1,
        "output_directory": "Toto"}),
])
def test_api_arguments(arguments):
    """
    Argument are parametrize to test them all... If possible.
    """
    try:
        response = google_images_download.GoogleImageDownload(arguments)
        response.download()
    except Exception as error:
        pytest.fail(str(error))


# @pytest.mark.skip
@pytest.mark.parametrize("config_file", [
    ("google_images_download/sample_config.json"),

])
def test_command_line_config_file(config_file):
    """
    Testing the command line interface.
       :param config_file: Configuration file parametrize.
    """
    command = shlex.split(
        "python3 google_images_download/google_images_download.py --config_file={0}".format(config_file))
    procedure = Popen(command, stderr=PIPE, stdout=PIPE)
    outs, errs = procedure.communicate()
    assert errs == b""
    assert outs != b""
