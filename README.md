# Sicredi Challenge

### Exercício:
Criar uma API onde se insere o número da conta corrente de um associado na URL e retorna o nome de
CPF/CNPJ de todos os associados que compõem o grupo econômico.
Deve-se usar o relatório "cadastro_visao_geral_associado_conta.csv" para criar uma collection dentro do
MongoDB para que seja usada como base de dados para as buscas via API, essa automação de população do
banco deve rodar de maneira orquestrada em um horário específico do dia, realizando a criação ou
atualização dos registros contidos na base de dados.
Obs: Retorno não deve conter os dados da conta que está sendo usada para buscar o grupo econômico.
>>> Biblioteca recomendadas: fastapi, pandas, beanie e scheduller.


### Informações que devem estar contidas no MongoDB: num_conta, nom_associado, num_cpf_cnpj,
cod_conglomerado_economico.

Exemplo: a conta 581516 tem grupo econômico de código 1003, composto por 3 membros. O retorno seria:
```[
{
"nome": "Maria Fernanda Alves",
"cpf_cnpj":"94544960659"
},
{
"nome": "Carlos Eduardo Santos",
"cpf_cnpj":"22872352687"
}
]
````

Exemplo de dados para criar arquivo exemplo “cadastro_visao_geral_associado_conta.csv”:

num_conta | nom_associado         | num_cpf_cnpj | cod_conglomerado_economico
58151-6   | João Pedro Silva      | 94544960659  | 1003
42842-1   | Maria Fernanda Alves  | 22872352687  | 1003
33647-7   | Ana Paula Costa       | 50379613043  | 1003
35740-8   | Carlos Eduardo Santos | 68346379018  | 1003
02123-5   | Ricardo Menezes       | 80139389628  | 1002