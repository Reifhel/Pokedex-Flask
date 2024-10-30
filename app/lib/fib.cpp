#include <iostream>

// Lembrar de ativar
// em++ main.cpp -s EXPORTED_FUNCTIONS="['_add']" -s EXPORTED_RUNTIME_METHODS="['ccall', 'cwrap']"
typedef unsigned long long int_ulonglong;

extern "C" {
    int_ulonglong fibonacci(int_ulonglong n){
        // Caso base
        if (n == 0) return n;
        if (n == 1) return n;

        int_ulonglong last = 0;
        int_ulonglong next = 1;
        int_ulonglong temp;

        for (int_ulonglong i = 2; i <= n; i++) {
            temp = next;
            next = last + next;
            last = temp;

        }
        
        return next;
    }
}