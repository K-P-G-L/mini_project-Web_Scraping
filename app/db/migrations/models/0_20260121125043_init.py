from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "Questions" (
    "question_id" SERIAL NOT NULL PRIMARY KEY,
    "question_text" TEXT
);
CREATE TABLE IF NOT EXISTS "Quotes" (
    "quotes_id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT,
    "author" VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS "token_blacklist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(500) NOT NULL,
    "blacklisted_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expires_at" TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_token_black_token_3c6615" ON "token_blacklist" ("token");
CREATE TABLE IF NOT EXISTS "Users" (
    "user_id" VARCHAR(50) NOT NULL PRIMARY KEY,
    "user_name" VARCHAR(100),
    "pwd_hash" VARCHAR(255),
    "token_id" VARCHAR(255)
);
COMMENT ON COLUMN "Users"."user_id" IS '사용자 고유 아이디 (문자열)';
COMMENT ON COLUMN "Users"."user_name" IS '사용자 이름/닉네임';
COMMENT ON COLUMN "Users"."pwd_hash" IS '해싱된 비밀번호';
COMMENT ON COLUMN "Users"."token_id" IS '인증 토큰 식별자';
CREATE TABLE IF NOT EXISTS "Bookmarks" (
    "bookmarks_id" SERIAL NOT NULL PRIMARY KEY,
    "quote_id" INT NOT NULL REFERENCES "Quotes" ("quotes_id") ON DELETE CASCADE,
    "user_id" VARCHAR(50) NOT NULL REFERENCES "Users" ("user_id") ON DELETE CASCADE,
    CONSTRAINT "uid_Bookmarks_user_id_a04dd5" UNIQUE ("user_id", "quote_id")
);
CREATE TABLE IF NOT EXISTS "Diaries" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255),
    "content" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" VARCHAR(50) NOT NULL REFERENCES "Users" ("user_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "User_Questions" (
    "user_question" SERIAL NOT NULL PRIMARY KEY,
    "question_id" INT NOT NULL REFERENCES "Questions" ("question_id") ON DELETE CASCADE,
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
    "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"
)
