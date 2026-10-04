#include <windows.h>
#include <iostream>

PROCESS_INFORMATION pythonProcess{};

bool StartPythonServer()
{
    STARTUPINFOA si{};
    si.cb = sizeof(si);

    // Make sure python.exe is in PATH.
    char command[] = "python server\\server.py";

    BOOL success = CreateProcessA(
        NULL,           // Application
        command,        // Command line
        NULL,
        NULL,
        FALSE,
        CREATE_NEW_CONSOLE,
        NULL,
        NULL,
        &si,
        &pythonProcess
    );

    if (!success)
    {
        std::cout << "Failed to start Python server.\n";
        return false;
    }

    std::cout << "Python server started!\n";
    return true;
}

void StopPythonServer()
{
    TerminateProcess(pythonProcess.hProcess, 0);

    CloseHandle(pythonProcess.hThread);
    CloseHandle(pythonProcess.hProcess);
}

int main()
{
    StartPythonServer();

    std::cout << "Press Enter to quit...";
    std::cin.get();

    StopPythonServer();
}