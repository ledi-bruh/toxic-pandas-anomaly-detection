from ...domain.models import AnomalyDetection
from ..models import DbAnomalyDetection


__all__ = [
    'db_to_domain',
    'domain_to_db',
]


def domain_to_db(aggregate: AnomalyDetection) -> DbAnomalyDetection:
    return DbAnomalyDetection(
        timestamp=aggregate.timestamp,
        valves=aggregate.valves,
        pumps=aggregate.pumps,
        fans=aggregate.fans,
        slide=aggregate.slide,
    )


def db_to_domain(db_model: DbAnomalyDetection) -> AnomalyDetection:
    return AnomalyDetection(
        timestamp=db_model.timestamp,
        valves=db_model.valves,
        pumps=db_model.pumps,
        fans=db_model.fans,
        slide=db_model.slide,
    )
