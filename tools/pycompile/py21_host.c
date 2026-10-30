/* F943 — host the game's OWN CPython 2.1 (vampire_python21.dll) to compile the campaign hub
 * scripts, which ship as .py source only. D2 chose precompiled .pyc with an offline 2.1 as the
 * build-time compiler; this IS that compiler, and it is the most faithful one available because it
 * is the interpreter the game itself shipped with. Runs under Wine; emits .pyc only. */
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

typedef void(__cdecl* PyVoidFn)(void);
typedef int(__cdecl* PyStrFn)(const char*);

int main(int argc, char** argv)
{
    if (argc < 2)
    {
        printf("usage: py21_host <script.py>\n");
        return 64;
    }
    HMODULE dll = LoadLibraryA("vampire_python21.dll");
    if (dll == NULL)
    {
        printf("py21_host: cannot load vampire_python21.dll (err %lu)\n", GetLastError());
        return 65;
    }
    PyVoidFn pyInit = (PyVoidFn)GetProcAddress(dll, "Py_Initialize");
    PyStrFn pyRun = (PyStrFn)GetProcAddress(dll, "PyRun_SimpleString");
    PyVoidFn pyFini = (PyVoidFn)GetProcAddress(dll, "Py_Finalize");
    int* noSite = (int*)GetProcAddress(dll, "Py_NoSiteFlag");
    if (pyInit == NULL || pyRun == NULL)
    {
        printf("py21_host: required exports missing\n");
        return 66;
    }
    if (noSite != NULL)
    {
        *noSite = 1; /* no stdlib on disk for this host; site import would only warn */
    }
    pyInit();

    FILE* f = fopen(argv[1], "rb");
    if (f == NULL)
    {
        printf("py21_host: cannot open %s\n", argv[1]);
        return 67;
    }
    fseek(f, 0, SEEK_END);
    long n = ftell(f);
    fseek(f, 0, SEEK_SET);
    char* buf = (char*)malloc((size_t)n + 1);
    size_t got = fread(buf, 1, (size_t)n, f);
    buf[got] = '\0';
    fclose(f);

    int rc = pyRun(buf);
    if (pyFini != NULL)
    {
        pyFini();
    }
    free(buf);
    printf("py21_host: script returned %d\n", rc);
    return rc == 0 ? 0 : 1;
}
