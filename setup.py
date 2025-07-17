from setuptools import setup

setup(
    name="customer-support-bot",
    install_requires=[
        "fastapi==0.109.1",
        "uvicorn==0.27.0",
        "asyncpg==0.29.0",
        # دیگر نیازمندی‌ها...
    ],
    dependency_links=[
        "https://github.com/pgvector/pgvector-python/tarball/master#egg=pgvector-0.4.1"
    ]
)

