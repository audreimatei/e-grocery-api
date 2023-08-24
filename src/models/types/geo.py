import geoalchemy2

from src.config import cfg

Point = geoalchemy2.Geography('POINT', srid=cfg.SRID)
Polygon = geoalchemy2.Geography('POLYGON', srid=cfg.SRID)
