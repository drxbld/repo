import zlib, base64

exec(zlib.decompress(base64.b64decode('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')))