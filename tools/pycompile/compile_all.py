import sys, marshal, imp
# F943: one "src|dst|mtime|co_filename" per line. The last two are what make our output
# byte-identical to the .pyc the game shipped (docs/specs/feature-943-campaign-hubs.md):
# compile() takes the filename to embed, and the 4 bytes after the magic are the source mtime.
log = open("compile_log.txt", "w")
listing = open("targets.txt", "r")
lines = listing.readlines()
listing.close()
ok = 0
bad = 0
for line in lines:
    line = line.strip()
    if line == "":
        continue
    parts = line.split("|")
    src = parts[0]
    dst = parts[1]
    mtime = long(parts[2])
    coname = parts[3]
    try:
        f = open(src, "r")
        text = f.read()
        f.close()
        text = text.replace("\r\n", "\n")
        if text[-1:] != "\n":
            text = text + "\n"
        code = compile(text, coname, "exec")
        out = open(dst, "wb")
        out.write(imp.get_magic())
        out.write(chr(mtime & 255) + chr((mtime >> 8) & 255) + chr((mtime >> 16) & 255) + chr((mtime >> 24) & 255))
        marshal.dump(code, out)
        out.close()
        ok = ok + 1
        log.write("OK   " + dst + "\n")
    except:
        bad = bad + 1
        log.write("FAIL " + src + " " + str(sys.exc_info()[1]) + "\n")
log.write("compiled=" + str(ok) + " failed=" + str(bad) + "\n")
log.close()
