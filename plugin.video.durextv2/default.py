import zlib, base64

exec(zlib.decompress(base64.b64decode('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')))