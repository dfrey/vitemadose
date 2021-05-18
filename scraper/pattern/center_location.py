from __future__ import annotations

from dataclasses import asdict
from typing import Optional

from pydantic.dataclasses import dataclass

from utils.vmd_utils import departementUtils
from utils.vmd_logger import get_logger

logger = get_logger()


@dataclass
class CenterLocation:
    longitude: float
    latitude: float
    city: Optional[str] = None
    cp: Optional[str] = None

    # TODO: Use `asdict()` directly, default is not clear.
    def default(self):
        return asdict(self)



# def convert_csv_data_to_location(csv_data: dict) -> Optional[CenterLocation]:
#     long = csv_data.get("long_coor1", None)
#     lat = csv_data.get("lat_coor1", None)
#     city = csv_data.get("com_nom", None)
#     cp = csv_data.get("com_cp", None)

#     if not long or not lat:
#         return None
#     if "address" in csv_data:
#         if not city:
#             print("csv_data", csv_data)
#             print("getting city from '",csv_data.get("address"),"'")
#             city = departementUtils.get_city(csv_data.get("address"))
#             print("got city '",city,"'")
#         if not cp:
#             cp = departementUtils.get_cp(csv_data.get("address"))
#             print("got cp '",cp,"'")
#     try:
#         return CenterLocation(float(long), float(lat), city, cp)
#     except:
#         return None

    @classmethod
    def from_csv_data(cls, data: dict) -> Optional[CenterLocation]:
        long = data.get("long_coor1")
        lat = data.get("lat_coor1")
        city = data.get("com_nom")
        cp = data.get("com_cp")

        if long and lat:
            if address := data.get("address"):
                if not city:
                    city = departementUtils.get_city(address)
                if not cp:
                    cp = departementUtils.get_cp(address)
            try:
                return CenterLocation(long, lat, city, cp)
            except Exception as e:
                logger.warning("Failed to parse CenterLocation from {}".format(data))
                logger.warning(e)
        return


convert_csv_data_to_location = CenterLocation.from_csv_data

