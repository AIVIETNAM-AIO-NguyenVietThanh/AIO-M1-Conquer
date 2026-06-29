from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db, SessionLocal
from app.routers import documents, rag  # noqa: F401 - registers models with Base

from sqlalchemy import text # <-- THÊM DÒNG NÀY

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database on startup.

    Args:
        app: The FastAPI application instance.

    Returns:
        None
    """
    init_db()
    yield

app = FastAPI(title="ChatBot RAG API", lifespan=lifespan)

# --- THÊM ĐOẠN CODE NÀY ĐỂ TẠO ROUTE KIỂM TRA ---
@app.get("/test-db", tags=["Cấu hình hệ thống"])
def test_database_connection():
    try:
        # Sử dụng SessionLocal đã import từ app.database
        with SessionLocal() as session:
            result = session.execute(text("SELECT version();")).fetchone()
            return {
                "status": "Kết nối Postgres trong Docker OK!", 
                "postgres_version": result[0]
            }
    except Exception as e:
        return {
            "status": "Lỗi kết nối hoặc lỗi khởi tạo pgvector", 
            "detail": str(e)
        }
# ------------------------------------------------

app.include_router(documents.router)
app.include_router(rag.router)
