import zlib, base64

exec(zlib.decompress(base64.b64decode('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')))