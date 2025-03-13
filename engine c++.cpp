// DummyDLL.cpp : Defines the entry point for the DLL application.
#include <windows.h>

// DllMain: The entry point for a Windows DLL.
// This function is called by the system when processes and threads are initialized and terminated,
// or upon calls to the LoadLibrary and FreeLibrary functions.
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // A process is loading the DLL.
        break;
    case DLL_THREAD_ATTACH:
        // A process is creating a new thread.
        break;
    case DLL_THREAD_DETACH:
        // A thread exits normally.
        break;
    case DLL_PROCESS_DETACH:
        // A process unloads the DLL.
        break;
    }
    return TRUE;
}
