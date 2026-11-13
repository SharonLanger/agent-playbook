"""Create local-only Langfuse settings once, without replacing existing data."""

import os
import secrets
from pathlib import Path

target = Path(__file__).with_name(".env")
values = {
    name: secrets.token_hex(size)
    for name, size in {
        "POSTGRES_PASSWORD": 24,
        "CLICKHOUSE_PASSWORD": 24,
        "REDIS_AUTH": 24,
        "MINIO_ROOT_PASSWORD": 24,
        "NEXTAUTH_SECRET": 32,
        "SALT": 24,
        "ENCRYPTION_KEY": 32,
    }.items()
}
old_umask = os.umask(0o077)
try:
    with target.open("x", encoding="utf-8") as output:
        output.write("LANGFUSE_PORT=3000\n")
        output.write("MINIO_PORT=9090\n")
        for name, value in values.items():
            output.write(f"{name}={value}\n")
except FileExistsError:
    print("Local .env already exists; left unchanged.")
else:
    print("Created private local .env. Keep this file for future starts.")
finally:
    os.umask(old_umask)
