from flask import Blueprint, request, jsonify
from app.scrapers.reddit import RedditScraper
from app.openai_client import OpenAIClient
from app.models import db, Comment, Influencer
from app.services.cleaner import TextCleaner
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/scrape/reddit', methods=['POST'])
def scrape_reddit():
    data = request.json

    keywords = data.get('keywords', [])
    limit = int(data.get('limit', 10))

    if not keywords:
        return jsonify({"error": "Debe proporcionar al menos una palabra clave."}), 400

    scraper = RedditScraper(keywords=keywords, limit=limit)
    raw_posts = scraper.scrape()

    # Instanciamos el cliente de OpenAI
    gpt = OpenAIClient()

    result_count = 0
    for post in raw_posts:
        name = post['keyword']
        influencer = Influencer.query.filter_by(name=name).first()
        if not influencer:
            influencer = Influencer(name=name, last_scrape=datetime.utcnow())
            db.session.add(influencer)
            db.session.commit()

        # Analizar sentimiento de título + texto
        full_text = f"{post['title']} {post['selftext']}".strip()
        print(f"Analizando sentimiento para: {full_text[:100]}...")
        sentiment, score = gpt.analyze_sentiment(full_text)
        print(f"Resultado análisis: Sentiment={sentiment}, Score={score}")
        post['sentiment'] = sentiment
        post['score_sentiment'] = score

        comment = Comment(
            influencer_id=influencer.id,
            platform='reddit',
            date=post['created_utc'],
            text=full_text,
            sentiment=sentiment,
            score=score
        )
        db.session.add(comment)
        result_count += 1

    db.session.commit()
    return jsonify({
        "message": f"{result_count} publicaciones de Reddit procesadas.",
        "keywords": keywords
    }), 200

@bp.route('/comments/<influencer_name>', methods=['GET'])
def get_comments(influencer_name):
    influencer = Influencer.query.filter_by(name=influencer_name).first()
    if not influencer:
        return jsonify({"error": "Influencer no encontrado"}), 404

    comments = Comment.query.filter_by(influencer_id=influencer.id).order_by(Comment.date.desc()).all()

    comments_list = []
    for c in comments:
        comments_list.append({
            "text": c.text,
            "sentiment": c.sentiment,
            "score": c.score,
            "date": c.date.isoformat()
        })

    return jsonify(comments_list), 200

@bp.route('/analytics/<influencer>', methods=['GET'])
def influencer_analytics(influencer):
    comments = Comment.query.filter(Comment.influencer.has(name=influencer)).all()
    if not comments:
        return jsonify({"error": "No se encontraron comentarios"}), 404

    pos = [c for c in comments if c.sentiment == "positivo"]
    neg = [c for c in comments if c.sentiment == "negativo"]
    neu = [c for c in comments if c.sentiment == "neutral"]
    avg_score = sum(c.score for c in comments) / len(comments)

    if avg_score > 0.25:
        karma = "positivo"
        recommendation = "Buena percepción general con apoyo sólido."
    elif avg_score < -0.25:
        karma = "negativo"
        recommendation = "Percepción negativa predominante, influenciador en crisis de imagen."
    else:
        karma = "neutral"
        recommendation = "Opiniones divididas. No hay una tendencia clara."

    return jsonify({
        "total": len(comments),
        "positive": len(pos),
        "neutral": len(neu),
        "negative": len(neg),
        "average_score": avg_score,
        "karma_score": karma,
        "recommendation": recommendation
    })