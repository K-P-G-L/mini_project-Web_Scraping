from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "Qeustions" (
    "question_id" SERIAL NOT NULL PRIMARY KEY,
    "question_text" TEXT
);
CREATE TABLE IF NOT EXISTS "Quotes" (
    "quotes_id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT,
    "author" VARCHAR(100)
);
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
    "user_id" VARCHAR(50) NOT NULL REFERENCES "Users" ("user_id") ON DELETE CASCADE
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
    "eJztmv9zojgUwP8Vh596M709pVj1frOtve3tVq+tvdvZbocJEJUREoWw1tnxf78kfAsInN"
    "r1wBl+Qcl7D5JPkvdeEn5INjag5X64wnhuA2cu/d74ISFgQ/pnS3bekMBiEUtYAQGaxZVD"
    "LV4KNJc4QCdUMAGWC2mRAV3dMRfExIiWIs+yWCHWqaKJpnGRh8ylB1WCp5DMoEMFLy+S59"
    "J/VLj0MIHS6yv9ayIDvkGXydntYq5OTGgZiQZoYZ1U02DmXEMl6wWX3iFyy01YRTRVx5Zn"
    "oyyzxZrMMIrsTERY6RQi6AAC2SuJ47E2siYEPMJm+82JVfxqCzYGnADPIgKTHUHpGDHItD"
    "Yub/SUveVXuaV0lO7FpdKlKrwmUUln4zc0puAbchbDsbThckCAr8HRxiw5+v04iib/zTAk"
    "VgQxLIgpxsOrShhjbGzkZlK7ngEnG5tgkqJGK1pRajZ4Uy2IpmRGb9vNAkR/9x+vP/Yfz9"
    "rNX1hbMHUTvgMZBhKZizYbNqsn88yxGLqDJNFb7EBzij7BNed6R2sIkA4zOAaO7Tl4TPV4"
    "bsIxEZbG/sIBq8jTiUOFNo82ChJ/cPWfrvs3AykxFH3n+X5sD+FzTpeb6JmywbHRpwF9vg"
    "KOoSaGIZNgGadKIt1tkS3b6RKAwJQDYM1glQ7Q3pjAWWfFYF9QGICZigmPEH53jbZ7xYY6"
    "skbciEmsjHmZHyAig4PCQ0CntOggt9s7hAeqlRsfuCwZZukbCfRHT5LiGL7ljEDB5EQ4Fm"
    "AbD76MWZ1t111aIq2z+/4XDtJeB5LPo+EfobpA9/rz6CoN1YGs+SrI4HpDJcS0YQ7bhGUK"
    "rxGYfgj/VDOWSLQNxghZ66Cvi+jf3Q+exv37vxJdcNMfD5hETuAPS88uU+M7ekjjn7vxxw"
    "a7bXwdDQecIHbJ1OFvjPXGX1l8l4BHsIrwSgWG4PzC0hBMnZTWSWlVktJycqsHD7pBk7fS"
    "q0hWmGE9QI9rlZhjLYOK7rsQT1jVWZfIhNAMYZ+8Ycuwzh6i7GHLPeZP9bgnAHJX0KHZAn"
    "Mc7nZXXAX2t58eoQXCaZrvPcXJfDpedHNc34e5D85wfMFavsDrMZVSXR57/wE7j/X27Uu9"
    "QDrqAokm2TOckfTlp9GxxYkgTSbRreYuWTTVyk2juezAQBGey9BQoa3fFyfEM606RsQLj4"
    "wQES5I8iPEcxi3ywkQVVjNHhgepG+e3gQ6vV6CHr12es3GNw/osMluZHajtxWF3XToVWu3"
    "lMYZ/dUuur42k08UPtvKWRAXxRxOmd/s2zWhUblOMrt3gq7odZXf6I+sU4nWknkfdZVDOu"
    "KnOVUxNC1WhjoD7mwf9KJN6eSNNsOsy5MW5au0dEpeg2wqaHqzya5dOgWMy4vuIciPsgdN"
    "8BxmL8wLtvIFm9KR05HN3EqvZ1DYRgtQzEazw8e8bBiMua7406BU5u/KHd65vjzRvEEcpk"
    "Z8Tng4h+g88kQh8CgT7uTUew7HyieL9lzT2IrzS/VB7KwSE82lUOUddyO27Oodif9vK7sa"
    "M7D+rKw+wSuf55E+K8tziAd8WXaKUTRNL+WiqnQG2oeOqc+yonEgKYzDINapPzCrXHDIj7"
    "TfoeNmTtD8YCGYnGawOMoKn02NPSAG6qcJ8Ci7UrmnUH8+jYb7nkI9I9rAF8PUyXnDMl3y"
    "Wk2sBRRZq4sPpdLnT+fJb8HYA/Y8d//54WXzLx5Y5IA="
)
