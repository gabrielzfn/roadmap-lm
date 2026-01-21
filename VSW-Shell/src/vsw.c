#define _GNU_SOURCE          // Requisito para o getline()
#include <stdio.h>           // Requisito para o printf()
#include <unistd.h>          // Requisito para fork()
#include <sys/wait.h>        // Requisito para waitpid()
#include <stdlib.h>          // Requisito para free(), malloc(), realloc() e exit()
#include <string.h>          // Requisito para strcmp()
#include "vsw.h"

/*
 * Shell builtins
 */
int vsw_cd(char **args);
int vsw_help(char **args);
int vsw_checksum(char **args);
int vsw_hexsend(char **args);
int vsw_tvbox(char **args);
int vsw_roteador(char **args);
int vsw_tools(char **args);
int vsw_autometro(char **args);
int vsw_comparador(char **args);
int vsw_difere(char **args);
int vsw_tabela(char **args);
int vsw_exit(char **args);

char *builtin_str[] = {
    "cd",
    "help",
    "ajuda",
    "tvbox",
    "roteador",
    "tools",
    "autometro",
    "repete",
    "comparador",
    "comparar",
    "difere",
    "diferenca",
    "tabela",
    "exit",
};

int (*builtin_func[]) (char **) = {
    &vsw_cd,
    &vsw_help,
    &vsw_help,
    &vsw_tvbox,
    &vsw_roteador,
    &vsw_tools,
    &vsw_autometro,
    &vsw_autometro,
    &vsw_comparador,
    &vsw_comparador,
    &vsw_difere,
    &vsw_difere,
    &vsw_tabela,
    &vsw_exit,
};

int vsw_num_builtins() {
    return sizeof(builtin_str) / sizeof(char *);
}

/* [Implementando Funções Builtins] */

int vsw_cd(char **args)
{
  if (args[1] == NULL) {
    fprintf(stderr, G"["Y"vsw-shell"G"]:"RST"Era esperado um argumento para \"cd\"\n");
      return 1;
  }
  
  char caminho_seguro[512];
  
  if (!limpador(args[1], caminho_seguro, sizeof(caminho_seguro))) {
    return 1;
  }
  if (chdir(args[1]) != 0) {
    perror(Y"[vsw-error]");
  }
  return 1;
}

int vsw_help(char **args)
{
    (void)args;  // Evita warning de unused paramete 

    printf(G"["RST"vsw-shell" G"]: "RST"Digite nome de programas, argumentos e pressione enter!!\n");
    printf(G"["RST"vsw-shell" G"] - [" RST"Ensaios Funcionais" G"] \n");

    for (int i = 0; i < vsw_num_builtins(); i++) {
        printf(" %s\n", builtin_str[i]);
    }
    printf(G"["RST"vsw-shell" G"]: "RST"Use o comando man para exibir informações de outros programas!!\n");

    return 1;
}

int vsw_tvbox(char **args)
{
  (void)args;

  const char *script = "/usr/local/bin/tvbox";
  if (access(script, X_OK) != 0){
    fprintf(stderr, RED"[vsw-error]:" RST" Script [%s] não encontrado ou não executável...\n", script);
    return 1;
  }

  pid_t pid = fork();
  if (pid == 0) {
    execl("/bin/sh", "sh", script, NULL);
    perror(RED "[vsw-error]: Falha ao executar tvbox..." RST);
    exit(EXIT_FAILURE);  
  }
  else if (pid > 0) {
    int status;
    waitpid(pid, &status, 0);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
  } else {
    perror(RED "[vsw-error]: Fork falhou..." RST);
  }
  return 1;
}

int vsw_roteador(char **args)
{
  (void)args;
   const char *script = "/usr/local/bin/roteador";
  if (access(script, X_OK) != 0){
    fprintf(stderr, RED"[vsw-error]:" RST" Script [%s] não encontrado ou não executável...\n", script);
    return 1;
  }

  pid_t pid = fork();
  if (pid == 0) {
    execl("/bin/sh", "sh", script, NULL);
    perror(RED "[vsw-error]: Falha ao executar roteador..." RST);
    exit(EXIT_FAILURE);  
  }
  else if (pid > 0) {
    int status;
    waitpid(pid, &status, 0);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
  } else {
    perror(RED "[vsw-error]: Fork falhou..." RST);
  }

  return 1;
}

int vsw_tools(char **args)
{
  (void)args;
     const char *script = "/usr/local/bin/tools";
  if (access(script, X_OK) != 0){
    fprintf(stderr, RED"[vsw-error]:" RST" Script [%s] não encontrado ou não executável...\n", script);
    return 1;
  }

  pid_t pid = fork();
  if (pid == 0) {
    execl("/bin/sh", "sh", script, NULL);
    perror(RED "[vsw-error]: Falha ao executar vsw-tools..." RST);
    exit(EXIT_FAILURE);  
  }
  else if (pid > 0) {
    int status;
    waitpid(pid, &status, 0);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
  } 
  else {
    perror(RED "[vsw-error]: Fork falhou..." RST);
  }
  return 1;
}

int vsw_tabela(char **args)
{
  (void)args;
  const char *script = "/usr/local/bin/tablelo.py";

  if (access(script, X_OK) != 0){
    fprintf(stderr, RED"[vsw-error]:" RST" Script [%s] não encontrado ou não executável...\n", script);
    return 1;
  }

  pid_t pid = fork();
  if (pid == 0) {
    execl("/bin/python3.14", "python3", script, NULL);
    perror(RED "[vsw-error]: Falha ao executar script de tabelas..." RST);
    exit(EXIT_FAILURE);
  }

  else if (pid > 0) {
    int status;
    waitpid(pid, &status, 0);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
  }
  else {
    perror(RED "[vsw-error]: Fork falhou..." RST);
  }
  return 1;
}


int vsw_comparador(char **args) 
{
  (void)args;
  const char *script = "/usr/local/bin/comparador.py";

  if (access(script, X_OK) != 0){
    fprintf(stderr, RED"[vsw-error]:" RST" Script [%s] não encontrado ou não executável...\n", script);
    return 1;
  }

  pid_t pid = fork();
  if (pid == 0) {
    execl("/bin/python3.14", "python3", script, NULL);
    perror(RED "[vsw-error]: Falha ao executar script comparador..." RST);
    exit(EXIT_FAILURE);  
  }
  else if (pid > 0) {
    int status;
    waitpid(pid, &status, 0);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
  } 
  else {
    perror(RED "[vsw-error]: Fork falhou..." RST);
  }
  return 1;
}


int vsw_autometro(char **args) 
{
    (void)args;
     const char *script = "/usr/local/bin/autometro.py";
  if (access(script, X_OK) != 0){
    fprintf(stderr, RED"[vsw-error]:" RST" Script [%s] não encontrado ou não executável...\n", script);
    return 1;
  }

  pid_t pid = fork();
  if (pid == 0) {
    execl("/bin/python3.14", "python3", script, NULL);
    perror(RED "[vsw-error]: Falha ao executar autometro..." RST);
    exit(EXIT_FAILURE);  
  }
  else if (pid > 0) {
    int status;
    waitpid(pid, &status, 0);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
  } 
  else {
    perror(RED "[vsw-error]: Fork falhou..." RST);
  }
  return 1;
 }

int vsw_difere(char **args)
{
    (void)args;
     const char *script = "/usr/local/bin/differ.py";
  if (access(script, X_OK) != 0){
    fprintf(stderr, RED"[vsw-error]:" RST" Script [%s] não encontrado ou não executável...\n", script);
    return 1;
  }

  pid_t pid = fork();
  if (pid == 0) {
    execl("/bin/python3.14", "python3", script, NULL);
    perror(RED "[vsw-error]: Falha ao executar script differ..." RST);
    exit(EXIT_FAILURE);  
  }
  else if (pid > 0) {
    int status;
    waitpid(pid, &status, 0);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
  }
  else {
    perror(RED "[vsw-error]: Fork falhou..." RST);
  }
  return 1;
}


int vsw_exit(char **args)
{
    (void)args;  // Evita warning de unused parameter

    printf("[vsw]: Saindo...\n");
    return 0;
}

/*
int vsw_it(char **args)
{
  if (args[1] == NULL) {
    int return_status = /usr/local/bin/it 
// it.sh sera desenvolvido para que leia o input do usuario e assim, ira printar apenas a man especifica do ensaio.
  }
}
*/

/* [Executor da shell] */

int vsw_launch(char **args)
{
    pid_t pid;
    int status;

    pid = fork();
    if (pid == 0) {
        /* processo filho */
        if (execvp(args[0], args) == -1) {
            perror("[vsw]");
        }
        exit(EXIT_FAILURE);
    } else if (pid < 0) {
        /* erro no fork */
        perror("[vsw]");
    } else {
        /* processo pai */
        do {
            waitpid(pid, &status, WUNTRACED);
        } while (!WIFEXITED(status) && !WIFSIGNALED(status));
    }
    return 1;
}

int vsw_execute(char **args)
{
    if (args[0] == NULL) {
        return 1; /* Comando vazio foi digitado */
    }

    for (int i = 0; i < vsw_num_builtins(); i++) {
        if (strcmp(args[0], builtin_str[i]) == 0) {
            return (*builtin_func[i])(args);
        }
    }

    return vsw_launch(args);
}

// Loop da shell 
void vsw_loop(void)
{
    char *line;
    char **args;
    int status;

    // Carregar histórico se existir
    //system("test -f .vsw_history && history -r .vsw_history");

    do {
        char cwd[1024];
        if (getcwd(cwd, sizeof(cwd)) != NULL)
            printf(G "["RST"vsw" G"] %s " RST "> ", cwd);
        else
            printf(G "[vsw] ? " RST "> ");

        line = vsw_read_line();
        if (!line) break;

        // Salvar no histórico
        FILE *h = fopen(".vsw_history", "a");
        if (h) {
            fprintf(h, "%s\n", line);
            fclose(h);
        }

        args = vsw_split_line(line);
        status = vsw_execute(args);

        free(line);
        free(args);
    } while (status);
}
    
#define vsw_TOK_BUFSIZE 64
#define vsw_TOK_DELIM " \t\r\n\a"

char **vsw_split_line(char *line)
{
    int bufsize = vsw_TOK_BUFSIZE;
    int position = 0;
    char **tokens = malloc(bufsize * sizeof(char*));  /* CORRIGIDO: sizeof(char*) */
    char *token;

    if (!tokens) {
        fprintf(stderr, "[vsw:error]: Erro ao alocar\n");
        exit(EXIT_FAILURE);
    }

    token = strtok(line, vsw_TOK_DELIM);
    while (token != NULL) {
        tokens[position] = token;
        position++;

        if (position >= bufsize) {
            bufsize += vsw_TOK_BUFSIZE;
            tokens = realloc(tokens, bufsize * sizeof(char*));  /* CORRIGIDO: sizeof(char*) */
            if (!tokens) {
                fprintf(stderr, "[vsw:error]: Erro ao alocar\n");
                exit(EXIT_FAILURE);
            }
        }

        token = strtok(NULL, vsw_TOK_DELIM);
    }
    tokens[position] = NULL;
    return tokens;
}

char *vsw_read_line(void)
{
    char *line = NULL;
    size_t bufsize = 0;
    
    if (getline(&line, &bufsize, stdin) == -1) {
        if (feof(stdin)) {
            printf("\n");  // Nova linha limpa no EOF (Ctrl+D)
        } else {
            perror("[vsw:error]: getline falhou");
        }
        free(line);
        return NULL;
    }
    
    // Remove newline do final
    size_t len = strlen(line);
    if (len > 0 && line[len-1] == '\n') {
        line[len-1] = '\0';
    }
    
    return line;
}

int main(int argc, char **argv)
{
    (void)argc;
    (void)argv;

    exibebanner();
    vsw_loop();
    return EXIT_SUCCESS;
}
