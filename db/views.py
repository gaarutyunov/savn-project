"""File containing views for nodes (users) and directed edges (communication between them)"""

__NODES__ = '''CREATE OR REPLACE VIEW github.v_nodes AS
    SELECT id, login as label
    FROM github.t_user'''

__EDGES__ = '''CREATE OR REPLACE VIEW github.v_edges AS
    WITH RECURSIVE
        comment AS (
            SELECT c.id, c.author_id AS author, c.review_id AS reply_to_id, r.author_id AS reply_to
            FROM github.t_comment c
                     JOIN github.t_review r ON c.review_id = r.id
            UNION ALL
            SELECT c.id, c.author_id AS author, c.reply_to_id AS reply_to_id, comment.author AS reply_yo
            FROM github.t_comment c
                     JOIN comment ON c.reply_to_id = comment.id
        ),
        reviews AS (
            SELECT c.id, c.author_id AS author, c.request_id AS reply_to_id, pr.author_id AS reply_to
            FROM github.t_review c
                     JOIN github.t_request pr ON c.request_id = pr.id
        )
    SELECT author as source, reply_to as target
    FROM comment
    UNION
    SELECT author as source, reply_to as target
    FROM reviews'''

VIEWS = [__NODES__, __EDGES__]