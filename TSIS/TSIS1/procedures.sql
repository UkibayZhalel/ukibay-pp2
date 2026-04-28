-- Procedure to delete a contact by name
CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR)
AS $$
BEGIN
    DELETE FROM contacts WHERE name = p_name;
END;
$$ LANGUAGE plpgsql;

-- Procedure to update contact basics
CREATE OR REPLACE PROCEDURE update_contact_details(
    p_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE
)
AS $$
BEGIN
    UPDATE contacts
    SET email = p_email, birthday = p_birthday
    WHERE name = p_name;
END;
$$ LANGUAGE plpgsql;