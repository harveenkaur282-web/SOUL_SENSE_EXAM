from app.db import get_session
from app.analysis.sentiment import analyze_sentiment
from app.models.reflection import UserReflection

def save_reflection(user_id, pov=None, challenges=None):
    session = get_session()

    reflection = UserReflection(
        user_id=user_id,
        pov_text=pov or None,
        challenges_text=challenges or None,
        pov_sentiment=analyze_sentiment(pov) if pov else None,
        challenges_sentiment=analyze_sentiment(challenges) if challenges else None
    )

    session.add(reflection)
    session.commit()
    session.close()
