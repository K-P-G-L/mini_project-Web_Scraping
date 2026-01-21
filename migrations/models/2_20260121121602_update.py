from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "token_blacklist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(500) NOT NULL,
    "blacklisted_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expires_at" TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_token_black_token_3c6615" ON "token_blacklist" ("token");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "token_blacklist";"""


MODELS_STATE = (
    "eJztWm1zmzgQ/isePqUzuZ5NcOLcN+ftmmuTXBKn12maYQTINmMsHBBNPB3/99MKxJuBM0"
    "58wAxfsNHugvaRtM9q0S9pbhvYcj+e2PZsjpyZ9Efnl0TQHLM/a7L9joQWi0gCDRRpFlcW"
    "WrwVaS51kE6ZYIwsF7MmA7u6Yy6oaRPWSjzLgkZbZ4ommURNHjGfPaxSe4LpFDtM8PgoeS"
    "77x4TPnk2x9PTE/prEwK/YBTncLmbq2MSWkXBAE31STQPMuYZKlwsuvST0gptARzRVty1v"
    "TrLMFks6tUloZxIKrRNMsIMohldSxwMfwYUAD+G2706k4nc7ZmPgMfIsGsNkQ6B0mwDIrD"
    "cud3oCb/lN7ilHyuDgUBkwFd6TsOVo5TsaoeAbciyuR9KKyxFFvgaHNsKSQ18Ox7jJf2Mo"
    "ECsCUTREKEbTq04wRrDBzM1E7XSKnGzYYiYp1FhHa4raHL2qFiYTOmW3/W4BRF+Hd6efhn"
    "d7/e4H8MVmYcIPINeBROai1QpW9XiWORdFOEgiemE72JyQz3jJcb1kPURExxk4BoHtIXhM"
    "/fBciTkhWqN44aCXMNLFpwpzjzmFqT+5hvenw7NzKTEV/eD5dthuxXOai1s8MmUDB7NPQ/"
    "rsBTmGmpiGILFlO9US6q6L5vI83YIImnAAwA3odADtmYmcZRYH+4JCAgYVE++Afjdl21Lc"
    "0DJriBs1qZWxLvMJIjTYih4CdCpjB7nf34AemFYuP3BZkmbZGyn2Z08SxRF+zZmBMZOG4F"
    "gA2+j82wj6PHfdZyuO1t7V8BsHcr4MJF9urv8U6jF0T7/cnKRBdTC4r6IMXM+YhJpznINt"
    "wjIFrxGYfhR/6sklEvPBuCHWMhjrIvQvr87vR8OrvxNDcDYcnYNETsAvWvcOU/M7fEjnn8"
    "vRpw7cdr7fXJ9zBG2XThz+xkhv9B34XUIetVViv6jIiAU/0SqAaZPSNimtS1JaTW5162E3"
    "cHktvQplhRnWLfa4VoU51nPQ0bIb8YRVm3XFMaEsQyiTN6wZttlDmD2shcf8pR6NBCLuC3"
    "ZYtgCBw10fipPA/uLzHbaQWKb50TO+mJsTRVe7jX02j8EZgS/YyxdEPVCpNOTB+7eoPLbl"
    "28d2g7TTDRJLsqd2RtKXn0ZHFg2BNJlE97qbZNFMKzeN5rItiUJ8l2FUoS3fxhPxb1otR3"
    "BIRvYMkxOLPcsyXZpFFimNQtagoKtqCeW2KtkgwuADWKoqKQx2VR94bwBT5YHN6gNFBYJu"
    "uioZTv+timjr1m0hrWaFNPy6MNnTthjcpGUzB7YhAyncXhvJEknILomXV/wy6FZUAvNJ9k"
    "FsmKuh1jqUkbekWemHp3eRzq6H6Jhdj467nR8e0nEXbmS40fuKAjdH7Kr1e0pnj/1qBwNf"
    "G+RjhU/YairRRdzNUeY3ZYdGGFW7O8kenWAojgfK7+xH1plE68l8jAbKNgPxbruZOCUsXg"
    "x1itxpGejjNpUjb/QBZl0e9xi+Sk9nyGsYloKmd7twHbAlYBweDLaBfCcff/29RrlAFLep"
    "HHI2syGsHB8bDGyjhxjMRveIz3nZMABzXfGXQaWYv2nT/sbCbkM37PFpakQHdLbHITwI1F"
    "AQOMuITyhtsX9X+WTRx840bMX5pXobH6wKE83nWJc3LOes2bWVnf/vG3I9VmB7nrs9OlM9"
    "njs6z50XELc40t1EFk2jlwpRdTp8NMSOqU+z2DiQFPIwinTabyi1I4d8pv2JHTdzgeaTRc"
    "ykmWSxkx0+LI0SIAbqzQRwJ1Wp3OMff93fXJc9/vFAmIOPhqnT/Q58n3qqJ6wFKILXxadB"
    "0gc/9pOfHOABJQ+8vT+9rP4FYKpJqg=="
)
