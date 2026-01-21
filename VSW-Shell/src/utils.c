#include "vsw.h"
#include <stdbool.h>
#include <ctype.h>

/* Wrappers */

void *Getcwd(char *buf, size_t size) {
    if (getcwd(buf, size) == NULL) {
        perror(RED "getcwd Falhou!" RST);
        return NULL;  /* Corrigido: retorna NULL em caso de erro */
    }
    return buf;
}



/* Macro Alocador de memória */ 
void *Malloc(size_t size)
{
    void *ptr;

    if (size == 0) {
        return NULL;
    }

    ptr = malloc(size);  /* Corrigido: alocar memória */
    if (!ptr) {
        perror(RED "Malloc Falhou!" RST);
        exit(EXIT_FAILURE);
    }
    
    return ptr;
}

/* Macro Realocador de memória */
void *Realloc(void *ptr, size_t size)
{
    void *novo_ptr;

    novo_ptr = realloc(ptr, size);
    if (!novo_ptr && size != 0) {
        perror(RED "Realloc Falhou!" RST);
        exit(EXIT_FAILURE);
    }

    return novo_ptr;
}

/* Sanitizador de strings */
bool limpador(const char *input, char *output, size_t out_size) {
  if (!input || !output || out_size == 0) return false;

  size_t i = 0;
  while (input[i] && i < out_size - 1) {
    if (isalnum(input[i]) || input[i] == '.' || 
      input[i] == '-' || input[i] == '_' || input[i] == '/' ) {
      output[i] = input[i];
      i++;
    } else {
      fprintf(stderr, RED "[vsw-erro]: Caractere inválido '%c' no caminho\n" RST, input[i]);
    return false;
    }
  }
  output[i] = '\0';
  return true;
}


void exibebanner(void)
{
    p(G "\n["RST"vsw-shell"G"]-"RST"By"G"-["RST"FelipeArnt"G"]\n\n");
    p(G "  _    ________      __            _____ __  __________    __ \n"
        "| |  / / ___/ |     / /           / ___// / / / ____/ /   / / \n"
        "| | / /\\__ \\| | /| / /  ______    \\__ \\/ /_/ / __/ / /   / /  \n"
        "| |/ /___/ /| |/ |/ /  /_____/   ___/ / __  / /___/ /___/ /___\n"
        "|___//____/ |__/|__/            /____/_/ /_/_____/_____/_____/\n\n" RST
  );
}
