from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "Users" (
    "user_id" VARCHAR(50) NOT NULL PRIMARY KEY,
    "user_name" VARCHAR(100),
    "pwd_hash" VARCHAR(255),
    "token_id" VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS "Diaries" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255),
    "content" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" VARCHAR(50) NOT NULL REFERENCES "Users" ("user_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Quotes" (
    "quotes_id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT,
    "author" VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS "Bookmarks" (
    "bookmarks_id" SERIAL NOT NULL PRIMARY KEY,
    "quote_id" INT NOT NULL REFERENCES "Quotes" ("quotes_id") ON DELETE CASCADE,
    "user_id" VARCHAR(50) NOT NULL REFERENCES "Users" ("user_id") ON DELETE CASCADE,
    CONSTRAINT "uid_Bookmarks_user_id_a04dd5" UNIQUE ("user_id", "quote_id")
);
CREATE TABLE IF NOT EXISTS "Qeustions" (
    "question_id" SERIAL NOT NULL PRIMARY KEY,
    "question_text" TEXT
);
CREATE TABLE IF NOT EXISTS "User_Questions" (
    "user_question" SERIAL NOT NULL PRIMARY KEY,
    "question_id" INT NOT NULL REFERENCES "Qeustions" ("question_id") ON DELETE CASCADE,
    "user_id" VARCHAR(50) NOT NULL REFERENCES "Users" ("user_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztml1T4jAUhv8Kw5U74zrK+jXegeDKqrAq7jo6Tie0ETq0CbbpIuPw3zdJv9LSIEUq7d"
    "g7epKTJg/JeU+SvlVNrEHD3rmzoVU9qbxVETAh/RGxb1eqYDwOrcxAQN/gFVkNbgF9m1hA"
    "JdT4DAwbUpMGbdXSx0THiFqRYxjMiFVaUUeD0OQg/cWBCsEDSIa8I49P1KwjDb5C238cj5"
    "RnHRpapJ8Ofb2ia6wDvFAh0zEvOB0C64xXZ+/sKyo2HBPFXMZTMsQo8KH9YtYBRNACBGrC"
    "UFhPvSH7JrfX1EAsBwbd1UKDBp+BYxBh6EvyUDFiLHVEbD5YE7wqBkQDMqSPB7szd0TheN"
    "1abAR/6jen5/WbrYPdb2wkmP4h7t/U8UpqvGjGmwAEuI1wxDGm/CEtVd9pJa4etQCrXyXk"
    "Gs6rLMDu7S5DltaSouVljG3IcjzRlCGwh2lQij6FJFk7OFiCJK0lJcnLoiQJHkGUcqmLPl"
    "+bJAugzyNhuTNDH6ijCbA0JVISItd0YOnQnife8BzPLm6gAfgQ5wl7EtKkjUxXCavZs575"
    "88W3ev94ZN71MR6ZwBp9EEPDa6bAJHiIpz2yWesfxMHShmuvqYIhYSsH17BsLc0XmTUzbg"
    "EIDHiv2bvZmyKLJSERC1aRPBNrhqt1M7lYUmxuI5IcmhODMqMcmwxeBN5o/jVgb/le29s/"
    "2j/+cbh/TKvwngSWowVBut3pvZNvEZ0YqXKtwOFra5oYm+gbCXRnT5RiD75KZqDgUhCOC7"
    "D1Wvc91mfTtl8MkdbWVf2egzSnXsllt/PTry7QPb3sNuJQLciGr4AErk1aQnQTSthGPGN4"
    "Nc91x/+RTwGo0jFoXWRMQy2U0m9ftW579avfkb+gWe+1WEktgt+3bh3G5nfQSOVvu3deYY"
    "+Vh26nxQlimwws/sawXu+hyvoEHIIVhCcK0ITg51t9MPNKvuFd82eHnfXsm+fy6CjUeaJn"
    "2IL6AF3AKefapj0ESE2K3rEjl/zxlGVE1GyBSZAQiFOFDo8OChJ3ctVvT+vNVnUm33tkmV"
    "sFGXhCeiVm5/IMqyFuBdabYz0G0+fFwRTX07JJV7A9SVzP0vQr7lYmYice+nQcRZf3GeZj"
    "Ha8HY6kmpZrkQk3EqegGz49ju/bbKS43MTLlSYZdtAkaHDCXCzCvssETDs40pdJGfEqZLf"
    "fq2ezV6X5viBMUQ67BoUdBkGZ0XbfS1YifP0NN6U+/5M1Athrh3QwkykR4a7BAKaATXlNs"
    "SizcjqaVi4hXKRgiE0IFIo1szDkWJNJ9hnisFPYAsifQokHP8T/7Ka8A1xz7Ilgkn2QtFw"
    "NZTeVavK/d4DdaL0KXlwyFc35lMPw8WcnHCiyPqsqjqs3zzOioShYQVzitKqKKxunFQlSe"
    "zqzq0NLVYZIaeyULdRiEdcrvcnInDnKl/UdT3MQFKhcLwaWYYpHJxzlsaaSA6FUvJsBMvi"
    "KXnpj+uu120p6Y3iE6wEdNV8l2xdBt8pRPrAsoslEv3gPHt7vb0U9oWAMp98Drl5fZf1f8"
    "qPU="
)
