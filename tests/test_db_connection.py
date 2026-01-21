# ruff: noqa: E402
import asyncio
import os
import sys
from pathlib import Path

# 현재 파일의 부모의 부모(루트 폴더)를 파이썬 경로에 추가
# 이렇게 하면 어디서 실행해도 'app' 패키지를 잘 찾습니다.
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from tortoise import Tortoise

from app.db.base import TORTOISE_CONFIG
from app.models import User


async def test_database():
    print("🚀 DB 연결 테스트 시작...")
    try:
        await Tortoise.init(config=TORTOISE_CONFIG)

        # 테스트용 데이터 (팀원들마다 중복되지 않게 임의의 ID 사용)
        test_id = f"test_{os.urandom(2).hex()}"

        user = await User.create(
            user_id=test_id, user_name="연결테스터", pwd_hash="test_pwd"
        )
        print(f"✅ 연결 성공! 생성된 유저 ID: {user.user_id}")

        # 확인 후 바로 삭제 (DB를 깨끗하게 유지하기 위해)
        await user.delete()
        print("🧹 테스트 데이터 삭제 완료 (DB 클린업)")

    except Exception as e:
        print(f"❌ DB 연결 실패: {e}")
    finally:
        await Tortoise.close_connections()
        print("👋 테스트 종료")


if __name__ == "__main__":
    asyncio.run(test_database())
