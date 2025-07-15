from . import db
def clean_like():
    db.session.execute('''
        DELETE FROM likes
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM likes
            GROUP BY user_id, post_id
        );
    ''')

    db.session.commit()
    return ("clear like success")