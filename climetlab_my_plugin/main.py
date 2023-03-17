#!/usr/bin/env python3
# (C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
from __future__ import annotations

import climetlab as cml
from climetlab import Dataset
from climetlab.decorators import normalize

__version__ = "0.1.0"

URL = "https://storage.ecmwf.europeanweather.cloud"

PATTERN = (
    "{url}/climetlab/test-data/0.5/fixtures/"
    "plugin_create_dataset_example_{year}_{parameter}.grib"
)


class Main(Dataset):
    name = None
    home_page = "-"
    # The licence is the licence of the data (not the licence of the plugin)
    licence = "-"
    documentation = "-"
    citation = "-"

    # These are the terms of use of the data (not the licence of the plugin)
    terms_of_use = (
        "By downloading data from this dataset, "
        "you agree to the terms and conditions defined at "
        "https://github.com/RoyCaitSith/"
        "climetlab-my-plugin/"
        "blob/main/LICENSE. "
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    #@normalize("parameter", ["tp", "t2m"])
    #def __init__(self, year, parameter):
        #request = dict(parameter=parameter, url=URL, year=year)
        #self.source = cml.load_source("url-pattern", PATTERN, request)

    @normalize("parameter", ['soil_temperature', 'forecast_error'])
    def __init__(self, parameter):
        self.source = cml.load_source("file", parameter + '.csv')
        # For a real plugin use "url" or "url-pattern" sources:
        # self.source = cml.load_source("url", URL_PREFIX + parameter + '.csv')
        # self.source = cml.load_source("url-pattern", PATTERN, {"parameter": parameter} )
