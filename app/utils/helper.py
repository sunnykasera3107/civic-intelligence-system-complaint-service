import logging

logger = logging.getLogger(__name__)


class Helper:
    
    @staticmethod
    def to_dict(model):
        return {
            column.name: getattr(model, column.name)
            for column in model.__table__.columns
        }
        