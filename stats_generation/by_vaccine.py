"""Sums available appointments per vaccine type.

Note: There are ~10% of centers that report multiple vaccine types.
For those, the individual breakdown is not clear, so they are left out at the moment.

Issue: https://github.com/CovidTrackerFr/vitemadose/issues/266

Usage:

```shell
python3 -m stats_generation.chronodoses_by_vaccine \
    --input="some/file.json" # Optional (should follow the same structure as data/output/info_centres.json.)\
    --output="put/it/here.json" # Optional
```

"""
import argparse
import json
import sys
from functools import reduce
from pathlib import Path
from typing import Iterator, List, Tuple

from utils.vmd_config import get_conf_outputs, get_conf_outstats

_default_input = Path(get_conf_outputs().get("last_scans"))
_default_output = Path(get_conf_outstats().get("by_vaccine_type"))


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=_default_input,
        type=Path,
        help="File with the statistics per department. Should follow the same structure as info_centres.json.",
    )
    parser.add_argument(
        "--output",
        default=_default_output,
        type=Path,
        help="Where to put the resulting statistics.",
    )
    return parser.parse_args(args)


def merge(data: dict, new: tuple) -> dict:
    vaccine_type, appointments = new
    if vaccine_type in data:
        data[vaccine_type] += appointments
    else:
        data[vaccine_type] = appointments
    return data


def flatten_vaccine_types_schedules(data: dict) -> Iterator[Tuple[str, int]]:
    return (
        (center["vaccine_type"][0], schedule["total"])
        for department in data.values()
        for center in department["centres_disponibles"]
        for schedule in center["appointment_schedules"]
        # Some centers report multiple vaccine types and it’s not clear how many are available for each
        # schedulable appointment. So, for the moment, they are left out.
        if len(center["vaccine_type"] or []) == 1
    )


def main(argv):
    args = parse_args(argv[1:])

    with open(args.input) as f:
        data = json.load(f)

    available_center_schedules = flatten_vaccine_types_schedules(data)
    by_vaccine_type = reduce(merge, available_center_schedules, {})

    with open(args.output, "w") as f:
        json.dump(by_vaccine_type, f)


if __name__ == "__main__":
    main(sys.argv)
