#ifndef VSW_H
# define VSW_H

# define _GNU_SOURCE
# include <stdio.h>
# include <unistd.h>
# include <sys/wait.h>
# include <stdlib.h>
# include <string.h>

/* Cores */
#define Y     "\033[1;33m"
#define G     "\033[1;32m"
#define C     "\033[1;36m"
#define RED   "\033[1;31m"
#define RST   "\033[0m"

/* Macros */
#define p(...) printf(__VA_ARGS__)
#define DEL " \n\t\v\f\r"

/* Wrappers */
void *Getcwd(char *, size_t);
void *Malloc(size_t);
void *Realloc(void *ptr, size_t size);

/* Sanitização */

bool limpador(const char *input, char *output, size_t out_size);

/* Funções da Shell */
void exibebanner(void);
char **vsw_split_line(char *line);
char *vsw_read_line(void);
int vsw_execute(char **args);
void vsw_loop(void);

/* ===== BUILTINS ESPECIALIZADOS ===== */
int vsw_cd(char **args);
int vsw_help(char **args);
int vsw_exit(char **args);

/* Builtins para Ensaios Funcionais */
int vsw_roteador(char **args);        /*   Nmap com presets     */
int vsw_checksum(char **args);       /*   sha256/crc32/md5     */
int vsw_hexsend(char **args);       /*   Envia hex via netcat */
int vsw_tabela(char **args);
int vsw_autometro(char **args);
int vsw_comparador(char **args);
int vsw_tvbox(char **args);
int vsw_difere(char **args);
int vsw_tools(char **args);
int vsw_alias(char **args);      /*   Gerencia aliases     */


/* Helpers */
int vsw_launch(char **args);
int vsw_num_builtins(void);

#endif
