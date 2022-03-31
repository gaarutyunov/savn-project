__TAG_LABEL_MAPPING_PROCEDURE__ = """CREATE OR REPLACE FUNCTION kaggle.pg_Tag_Get_LabelMapping() RETURNS TEXT AS
$BODY$
DECLARE
    l_json TEXT;
BEGIN
    SELECT JSON_OBJECT_AGG(t1.id, t1.label)::TEXT
    INTO STRICT l_json
    FROM (SELECT id, slug AS label
          FROM kaggle.t_tag) t1;

    RETURN l_json;
END;
$BODY$
    LANGUAGE plpgsql"""

__COMPETITION_LABEL_MAPPING_PROCEDURE__ = """CREATE OR REPLACE FUNCTION kaggle.pg_Competition_Get_LabelMapping() RETURNS TEXT AS
$BODY$
DECLARE
    l_json TEXT;
BEGIN
    SELECT JSON_OBJECT_AGG(t1.id, t1.label)::TEXT
    INTO STRICT l_json
    FROM (SELECT id, slug AS label
          FROM kaggle.t_competition) t1;

    RETURN l_json;
END;
$BODY$
    LANGUAGE plpgsql"""

PROCEDURES = [__TAG_LABEL_MAPPING_PROCEDURE__, __COMPETITION_LABEL_MAPPING_PROCEDURE__]
