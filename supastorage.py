"""
NOTE: In case the script fails with timeout error, go to virtual env folder ->
Lib -> site-packages -> httpx -> _client.py, line 818, and set 'timeout' to None
"""

import os
from transliteration import *
from tqdm import tqdm
from storage3.utils import StorageException
import supabase


def connect_supabase(url = os.getenv("SUPABASE_URL"), key = os.getenv("SUPABASE_KEY")):
    return supabase.create_client(url, key)


def slugify(string: str) -> str:
    """Takes a string, removes potentially dangerous chars,
    replaces spaces with dashes, and lowers the case"""
    dangerous_chars = {ord(c): None for c in "?.:,!«»()$—"}
    dangerous_chars[ord(" ")] = "-"
    return string.translate(dangerous_chars).lower()


def main():

    connect = connect_supabase()
    storage = connect.storage()
    storage_bucket = storage.get_bucket("prabyss")
    fldr = "slvlv1"

    source_path = "D:\\box"
    files = os.listdir(source_path)

    for f in tqdm([f for f in files if f != "dn"]):
        old_name, ext = f.rsplit(".", 1)
        new_name = slugify(transliterate(old_name, ru_args)) if " " in old_name else old_name
        os.rename(f"{source_path}/{f}", (pth:=f"{source_path}/{new_name}.{ext}"))

        try:
            storage_bucket.upload(f"{fldr}/{new_name}.{ext}", pth, {"cacheControl": "3600", "content-type": "audio/mpeg"})
        except StorageException:
            continue

        # os.rename(pth, f"{source_path}/dn/{new_name}.{ext}")


if __name__ == "__main__":
    main()