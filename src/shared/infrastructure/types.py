from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


__all__ = ['SessionFactory']


SessionFactory = async_sessionmaker[AsyncSession]
