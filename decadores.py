def mensagem_boas_vindas(nome):
    print(f"Isto é o PRINT de dentro da função: Seja Bem-vindo , onde só os fortes sobrevivem {nome}!")
    # O return devolve o valor, ele não imprime!
    return f"Isto é o VALOR que o RETURN devolveu: Oi {nome}, você está pronto para começar?"

print("--- PRIMEIRA CHAMADA ---")
# 1. A função é chamada
# 2. O print DENTRO dela é executado
# 3. O return devolve um valor, que é guardado na variável 'executar'
executar = mensagem_boas_vindas("Arthur")

# 4. AGORA NÓS IMPRIMIMOS o valor que foi guardado!
print(executar) 


print("\n--- SEGUNDA CHAMADA ---")
# O processo se repete
executar = mensagem_boas_vindas("Beatriz")

# Imprimimos o NOVO valor que está guardado em 'executar'
print(executar)