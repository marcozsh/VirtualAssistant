BEGIN TRANSACTION;

CREATE TABLE IA (
    id TEXT PRIMARY KEY,
    name TEXT,
    create_date DATE
);

INSERT INTO IA VALUES('1', '', date('now'));

CREATE TABLE phrase_type(
    id INTEGER PRIMARY KEY NOT NULL,
    description_phrase TEXT NOT NULL
);

INSERT INTO phrase_type VALUES(1, 'thanks responses');
INSERT INTO phrase_type VALUES(2, 'call responses');

CREATE TABLE phrases(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    phrase TEXT NOT NULL,
    phrase_type INTEGER NOT NULL,
    FOREIGN KEY(phrase_type) REFERENCES phrase_type(id)
);

COMMIT;
