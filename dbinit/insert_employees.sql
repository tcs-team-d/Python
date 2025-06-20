-- 管理者の追加
INSERT INTO employees (employee_id, name, email, password, is_admin)
VALUES (
    1,
    'Admin User',
    'admin@example.com',
    '$2a$10$NC7IzyGXDBQvpr0uzNDowu/2jveKLy2NEOJhnv2h7.6TBJs2S.ODa',
    TRUE
);

-- 非管理者の追加
INSERT INTO employees (employee_id, name, email, password, is_admin)
VALUES (
    2,
    'Regular User',
    'user@example.com',
    '$2a$10$z8cYNYfGDgvtN0znBFr5g.bDliHF1cIlzH5tvScFuCIc2ze8fARwG',
    FALSE
);
