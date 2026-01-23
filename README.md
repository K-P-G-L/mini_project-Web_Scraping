# 주의사항
- app/models/ 내부의 코드를 수정하고 깃허브에 올렸다면, 코드를 받은 후 반드시 uv run aerich --config app.db.base.TORTOISE_CONFIG upgrade 명령어를 입력해야 본인의 DB에도 변경 사항이 반영됩니다.

- 새로운 모델 추가: 새로운 모델 파일(예: comment.py)을 만들면 반드시 app/models/__init__.py에 등록해 주세요.

# 명령어
- uv run uvicorn app.main:app --reload
- uv run ruff check .
- uv run ruff check . --fix
- uv run ruff format .

# DB 설정
- brew install postgresql@15

-  brew services start postgresql@15

# 포스트그리
 - /opt/homebrew/opt/postgresql

# 유저 생성 
- CREATE ROLE mini_user WITH LOGIN PASSWORD 'password';

# DB 생성
- CREATE DATABASE mini_project OWNER mini_user;

# 권한 부여
- ALTER ROLE mini_user SUPERUSER;

# init설정
- uv run aerich init -t app.db.base.TORTOISE_CONFIG
- uv run aerich init-db

<img width="1387" height="563" alt="스크린샷 2026-01-21 오전 11 25 54" src="https://github.com/user-attachments/assets/71b3c3cf-8a73-408c-9d5c-9fd9221c6554" />
