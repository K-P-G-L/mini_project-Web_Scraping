from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "Diaries" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "Qeustions" RENAME TO "Questions";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "Diaries" DROP COLUMN "updated_at";
        ALTER TABLE "Questions" RENAME TO "Qeustions";"""


MODELS_STATE = (
    "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"
)
