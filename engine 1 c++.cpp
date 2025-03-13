// EngineSimulator.cpp
#include <windows.h>
#include <chrono>
#include <thread>
#include <atomic>

// Simple engine simulation class.
class EngineSimulator {
private:
    std::atomic<bool> running;
    std::atomic<int> rpm;
    std::atomic<float> temperature;
public:
    EngineSimulator() : running(false), rpm(0), temperature(25.0f) {}

    // Starts the engine simulation in a separate thread.
    void Start() {
        running = true;
        std::thread([this]() {
            // Simulate engine behavior until stopped.
            while (running) {
                // Increase RPM gradually, capping at 3000.
                if (rpm < 3000) {
                    rpm += 100;
                }
                // Increase temperature slightly.
                temperature += 0.1f;
                // Wait a short time before next update.
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
        }).detach();
    }

    // Stops the engine simulation and resets parameters.
    void Stop() {
        running = false;
        rpm = 0;
        temperature = 25.0f;
    }

    // Returns the current simulated RPM.
    int GetRPM() const {
        return rpm.load();
    }

    // Returns the current simulated temperature.
    float GetTemperature() const {
        return temperature.load();
    }
};

// Global engine simulator instance.
static EngineSimulator g_engine;

extern "C" {

// Starts the engine simulation.
__declspec(dllexport) void Engine_Start() {
    g_engine.Start();
}

// Stops the engine simulation.
__declspec(dllexport) void Engine_Stop() {
    g_engine.Stop();
}

// Returns the current RPM.
__declspec(dllexport) int Engine_GetRPM() {
    return g_engine.GetRPM();
}

// Returns the current temperature.
__declspec(dllexport) float Engine_GetTemperature() {
    return g_engine.GetTemperature();
}

// An optional update function (not used as simulation runs in background).
__declspec(dllexport) void Engine_Update() {
    // No operation needed; simulation updates automatically.
}

// DLL entry point.
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // Initialization code if needed.
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
}
