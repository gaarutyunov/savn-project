__CREATE_TAG_NODES_VIEW__ = """CREATE OR REPLACE VIEW kaggle.v_tag_co_occurrence_nodes AS
    SELECT id AS node
    FROM kaggle.t_tag
    ORDER BY id"""

__CREATE_TAG_EDGES_VIEW__ = """CREATE OR REPLACE VIEW kaggle.v_tag_co_occurrence_edges AS
    SELECT a.tag_id a, b.tag_id b, COUNT(*) weight
    FROM kaggle.t_competition_tag a
             JOIN kaggle.t_competition_tag b ON a.competition_id = b.competition_id AND b.tag_id > a.tag_id
    GROUP BY a.tag_id, b.tag_id"""

VIEWS = [__CREATE_TAG_NODES_VIEW__, __CREATE_TAG_EDGES_VIEW__]
