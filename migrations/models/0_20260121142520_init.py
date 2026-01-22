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
    "eJztWm1zmzgQ/isePuVmej2b4MTpN+ftmmuTXBP3rtO0wwgk24wx2CAu8fT837sSiDcDF0"
    "h8wAxfbKPdxdKj1T6rlX5ISxsT0317atuLJXIW0rveD8lCSwI/dmRvehJarSIJa6BIM7my"
    "0OKtSHOpg3QKgikyXQJNmLi6Y6yoYVvQanmmyRptHRQNaxY1eZax9ohK7Rmhc+KA4OFB8l"
    "z4BcK1Z1Miff8OPw0LkyfiMjl7XC3UqUFMnBiAJvqkGpiZcw2VblZcemXRS27COqKpum16"
    "SyvLbLWhc9sK7QyLstYZsYiDKGF/SR2PjZENIcBDDNsfTqTidztmg8kUeSaNYfJMoHTbYi"
    "BDb1w+6Bn7l1/lgXKsjA6PlBGo8J6ELcdbf6ARCr4hx+JmIm25HFHka3BoIyw59OVwjJv8"
    "N4YCsSIQRUOEYuReTYIxgo15biZqZ3PkZMMWM0mhBh1tKGpL9KSaxJrROTwO+wUQ/TW+O3"
    "s/vjsY9n9hY7EhTPgB5CaQyFy03bJVPV1k+qIIB0lEL22HGDPrA9lwXK+gh8jSSQaOQWD7"
    "HLymeXhuhU+I1iheOOgxjHRxV4HhwaAI9Z1rfH82Pr+QEq7oB8+Xw/ZJvKe9uMUjUzZwzP"
    "s0pC8ekYPVhBsyiS3bqZZQd1e0lJfpFmShGQeADYN1OoD23EDOJouDfUEhATMVg+yBfp/L"
    "tqW4oWPWEDdqUDNjXeYTRGhQiR4CdGpjB3k4fAY9gFYuP3BZkmbhHynxvSeJ4oQ85XhgzK"
    "QlOBbANrn4MmF9Xrru2oyjdXA9/sKBXG4Cycfbm9+Fegzds4+3p2lQHcKGr6IMXM9BQo0l"
    "ycE2YZmCFwemb8WPZnKJBGPAt5a5Cea6CP2r64v7yfj6z8QUnI8nF0wiJ+AXrQdHKf8OX9"
    "L7+2ryvscee19vby44grZLZw7/x0hv8pXxu4Q8aquW/agiHAt+olUAk0xKV7jixCYtu4mt"
    "dWKDznebjW6z0YjNRj058yePuMGQd9LmUFaYOQutGnPnddCFsgWWhFWXTccxoZD5lckHdw"
    "y7rDDMCnfCY/5Sj2YCWe4jcSBZYIHD3Z2K08D+8sMdMZFYpvnRM76Y2xNFt/uNfTaPwRmB"
    "L6jRFEU9UKk15LH/r1BR7sryD93Gd68bX8ix53ZG0pefRkcWLYE0mUQP+s/JokErN43mso"
    "pEIc7bgCq0zct4In5W2XEEh2RiL4h1asK7TMOlWWSR0ihkDcp0VS2h3FWbW0QYfAJLVZuF"
    "wb7qA68NYKo88Lz6QFGBoJ+uNofuX6mGtmvd1dEaViAlTysD3lZhcpOW7ZzYlkykGPbOTJ"
    "ZIQvZJvLzil0G3ohKYT7KfxYa5HmptQhm5Is1K3zy9j3T4PEIn8Hl80u9985BO+uxBZg/6"
    "UFHYwzF8asOB0juAb+1w5Gsz+VThDltPJbqIuznK/KHs1Aijencn2bMTTMXJSPkNvmQdJN"
    "pA5nM0UqpMxKvtZuKUsHrE6hy58zLQx21qRx4PGcy6PB0AvspAB+Q1wpaCpvf77HMESwAf"
    "HY6qQL6XQ31/r1EuEMVtaoccPJuFlZMTDGDjAQKYcf+Y+7yMMcNcV/xlUCvmL9q0v7Cw29"
    "INe9xNcXTxqjoO4QWvloLAWWYdP0jriv17yCeLDjvTsBXnl2oDTj0TTlOinLNj11V2/r8z"
    "5GaswO6efnd1pn4893RPPy8gVriq30YWTaOXClFNunw0Jo6hz7PYOJAU8jCKdLozlMaRQz"
    "7T/kMcN3OB5pNFzKSdZLGXHT5bGiVADNTbCeBeqlK51z/+uL+9KXv9Axs67f3bE+e6zQO0"
    "AD823uJ7IOkrH2+Shw3sBSWvur0+sWx/AvNb3n0="
)
