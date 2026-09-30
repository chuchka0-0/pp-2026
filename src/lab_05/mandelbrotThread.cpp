#include <stdio.h>
#include <thread>
#include <algorithm>
#include <stdlib.h>

#include "CycleTimer.h"

typedef struct {
    float x0, x1;
    float y0, y1;
    unsigned int width;
    unsigned int height;
    int maxIterations;
    int* output;
    int threadId;
    int numThreads;
} WorkerArgs;


extern void mandelbrotSerial(
    float x0, float y0, float x1, float y1,
    int width, int height,
    int startRow, int numRows,
    int maxIterations,
    int output[]);


//
// workerThreadStart --
//
// Thread entrypoint.
void workerThreadStart(WorkerArgs * const args) {

    const double start = CycleTimer::currentSeconds();

    if (getenv("BLOCK")) {
        // Пункты 1-3: блочное разбиение — каждый поток считает непрерывную полосу строк.
        const int rows = (args->height + args->numThreads - 1) / args->numThreads;
        const int startRow = args->threadId * rows;
        const int numRows = std::min(rows, (int)args->height - startRow);
        if (numRows > 0)
            mandelbrotSerial(args->x0, args->y0, args->x1, args->y1,
                             args->width, args->height, startRow, numRows,
                             args->maxIterations, args->output);
    } else {
        // Пункт 4: чередование строк — поток i считает строки i, i+T, i+2T, ...
        // Тяжёлые и лёгкие строки распределяются равномерно, синхронизация не нужна.
        for (unsigned int row = args->threadId; row < args->height; row += args->numThreads)
            mandelbrotSerial(args->x0, args->y0, args->x1, args->y1,
                             args->width, args->height, row, 1,
                             args->maxIterations, args->output);
    }

    // Пункт 3: время работы каждого потока (включается переменной THREAD_TIMES).
    if (getenv("THREAD_TIMES"))
        printf("thread %d: %.3f ms\n", args->threadId, (CycleTimer::currentSeconds() - start) * 1000);
}

//
// MandelbrotThread --
//
// Multi-threaded implementation of mandelbrot set image generation.
// Threads of execution are created by spawning std::threads.
void mandelbrotThread(
    int numThreads,
    float x0, float y0, float x1, float y1,
    int width, int height,
    int maxIterations, int output[])
{
    static constexpr int MAX_THREADS = 32;

    if (numThreads > MAX_THREADS)
    {
        fprintf(stderr, "Error: Max allowed threads is %d\n", MAX_THREADS);
        exit(1);
    }

    // Creates thread objects that do not yet represent a thread.
    std::thread workers[MAX_THREADS];
    WorkerArgs args[MAX_THREADS];

    for (int i=0; i<numThreads; i++) {
      
        // TODO FOR CS149 STUDENTS: You may or may not wish to modify
        // the per-thread arguments here.  The code below copies the
        // same arguments for each thread
        args[i].x0 = x0;
        args[i].y0 = y0;
        args[i].x1 = x1;
        args[i].y1 = y1;
        args[i].width = width;
        args[i].height = height;
        args[i].maxIterations = maxIterations;
        args[i].numThreads = numThreads;
        args[i].output = output;
      
        args[i].threadId = i;
    }

    // Spawn the worker threads.  Note that only numThreads-1 std::threads
    // are created and the main application thread is used as a worker
    // as well.
    for (int i=1; i<numThreads; i++) {
        workers[i] = std::thread(workerThreadStart, &args[i]);
    }
    
    workerThreadStart(&args[0]);

    // join worker threads
    for (int i=1; i<numThreads; i++) {
        workers[i].join();
    }
}

