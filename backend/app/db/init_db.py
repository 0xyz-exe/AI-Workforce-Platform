from sqlalchemy.orm import Session

from app.services.bootstrap import seed_reference_data


def init_db(session: Session) -> None:
    seed_reference_data(session)
    session.commit()