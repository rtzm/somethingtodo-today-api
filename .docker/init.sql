CREATE SEQUENCE prompt_id_seq
INCREMENT BY 1 MINVALUE 1 START 1;

CREATE TABLE prompt (
    id INT NOT NULL,
    text TEXT NOT NULL, 
    use_date DATE DEFAULT NULL, 
    created_timestamp TIMESTAMP(0) WITH TIME ZONE DEFAULT current_timestamp NOT NULL, 
    updated_timestamp TIMESTAMP(0) WITH TIME ZONE DEFAULT current_timestamp NOT NULL, 
    PRIMARY KEY(id)
);

CREATE INDEX use_date_idx ON prompt (use_date);

CREATE OR REPLACE FUNCTION update_updated_timestamp_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_timestamp = now(); 
        RETURN NEW;
    END;

CREATE TRIGGER update_prompt_updated_timestamp BEFORE UPDATE
ON prompt FOR EACH ROW EXECUTE PROCEDURE 
update_updated_timestamp_column();