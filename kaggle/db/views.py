__TAG_NODES_VIEW__ = """CREATE OR REPLACE VIEW kaggle.v_tag_co_occurrence_nodes AS
    SELECT id AS node
    FROM kaggle.t_tag
    ORDER BY id"""

__TAG_EDGES_VIEW__ = """CREATE OR REPLACE VIEW kaggle.v_tag_co_occurrence_edges AS
    SELECT a.tag_id a, b.tag_id b, COUNT(*) weight
    FROM kaggle.t_competition_tag a
             JOIN kaggle.t_competition_tag b ON a.competition_id = b.competition_id AND b.tag_id > a.tag_id
    GROUP BY a.tag_id, b.tag_id"""

__COMPETITION_NODES_VIEW__ = """CREATE OR REPLACE VIEW kaggle.v_competitions_teams_nodes AS
    SELECT id AS node
    FROM kaggle.t_competition
    ORDER BY id"""

__COMPETITION_EDGES_VIEW__ = """CREATE OR REPLACE VIEW kaggle.v_competitions_teams_edges AS
    SELECT a.competition_id a, b.competition_id b, COUNT(*) weight
    FROM kaggle.t_competition_team a
             JOIN kaggle.t_competition_team b ON a.team_id = b.team_id AND b.competition_id > a.competition_id
    GROUP BY a.competition_id, b.competition_id"""

VIEWS = [
    __TAG_NODES_VIEW__,
    __TAG_EDGES_VIEW__,
    __COMPETITION_NODES_VIEW__,
    __COMPETITION_EDGES_VIEW__,
]
