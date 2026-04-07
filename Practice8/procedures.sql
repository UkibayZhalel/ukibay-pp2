-- 1. Процедура Upsert (добавить новый или обновить телефон, если имя уже есть)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Процедура удаления по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_identifier OR phone = p_identifier;
END;
$$;

-- 3. Массовая вставка с валидацией (цикл, IF и проверка длины номера)
CREATE OR REPLACE PROCEDURE bulk_insert_with_validation(
    p_names VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    -- Цикл по массиву переданных имен
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        -- Простая валидация: номер должен быть не короче 10 символов
        IF length(p_phones[i]) >= 10 THEN
            INSERT INTO contacts (name, phone)
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            -- Вывод ошибки в консоль базы данных
            RAISE NOTICE 'Валидация не пройдена для %: номер % слишком короткий', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;