#include <stdio.h>
#include <time.h>

void tempo(){
  time_t tempo_bruto;
  time(&tempo_bruto);
  struct tm *data_hora = localtime(&tempo_bruto);

  printf("Registro do ponto do dia: %02d/%02d/%04d\n", 
         data_hora->tm_mday,
         data_hora->tm_mon + 1,
         data_hora->tm_year + 1900);
}

void registro(){
  float entrada;
  printf("Digite o horário de entrada: \n");
  scanf("%f",&entrada);

  float intervalo = (entrada + 6);
  float saida = (entrada + 9);
  float horas = (saida - entrada);
  printf("\n--------------------------\n");
  tempo();
  printf("\nEntrada: %.2f\nIntervalo: %.2f\nSaida: %.2f\nHoras trabalhadas: %2.f\n", entrada, intervalo, saida, horas);
  printf("\n--------------------------\n");
}

int main(){

  registro();
  return 0;
}
