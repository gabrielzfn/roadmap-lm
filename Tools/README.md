# 🧰 Tools Directory

This repository also includes a dedicated directory containing tools that may be useful during software analysis, testing, or documentation review. These tools should be introduced gradually over time. Therefore, please be patient.

```sh
roadmap-lm
├── README.md
└── Tools
    ├── comparador
    │   └── comparador.sh
    ├── tv-box
    │   └── tv-box.sh
    └── vsw-tools
        └── vsw-tools
```

<br>

- ## 🔎 C0mparad0r 📁
Script desenvolvido para comparação recursiva entre diretórios/pastas, identificando possíveis mudanças realizadas.

### Uso
- Execute o script com o seguinte comando:
    ```bash
    python comparador.py
```
```
- Escolher o pacote antigo e o pacote atualizado via interface gráfica.

---

- ## 📺 Script de Ensaios Funcionais em TV-Box

### Descrição

Script que executa verificações essenciais para procedimentos de ensaio, incluindo listagem de softwares, propriedades do sistema, configurações de rede e verificações específicas de segurança cibernética. 

### Uso

- Torne o script executável:

```bash
   chmod +x tvbox.sh
```

- Certifique-se de que o ADB está no PATH do sistema. Teste com:

```bash
   adb version
```

- Conecte o TV-Box ao computador via USB e execute o script:

```bash
./tvbox.sh || bash tv-box.sh
```

--- 

- ## VSW-Tools - Ensaios de Metrologia e Segurança Cibernética 

> Um canivete suíço para automação de tarefas do laboratório de Verificação de Software do LABELO.

`vsw-tools` é um script de shell projetado para agilizar o fluxo de trabalho no laboratório, centralizando funções essenciais como cálculo de hashes, verificação de integridade de arquivos e configuração rápida de rede.


**Torne o script executável:**
```bash
    chmod +x vsw-tools
```

**Mova o script para um diretório no seu PATH (recomendado):** Isso permite que você chame a ferramenta apenas pelo nome (`vsw-tools`) em vez do caminho completo (`./vsw-tools`). O diretório `/usr/local/bin` é o local padrão para isso.
    
```bash
sudo mv vsw-tools /usr/local/bin/**`vsw-tools`**
```

### Comandos

A sintaxe geral para usar a ferramenta é:

```bash
vsw-tools <comando> [argumentos...]
````

---

