"""Projeto 01: CRUD de alunos por matricula."""

from datetime import datetime
from pymongo.errors import DuplicateKeyError
from conexao import banco

alunos = banco['alunos_p01']

alunos.create_index('matricula', unique=True)

def validar_matricula(matricula: str):
    """Valida se a matricula contem apenas numeros e pelo menos 4 digitos."""
    return matricula.isdigit() and len(matricula) >= 4

while True:
    print('\n' + '=' * 40)
    print('      SISTEMA DE CADASTRO DE ALUNOS      ')
    print('=' * 40)
    print('[1] Cadastrar Aluno')
    print('[2] Listar Todos os Alunos')
    print('[3] Buscar Alunos por Curso')
    print('[4] Alterar Curso do Aluno')
    print('[5] Excluir Aluno')
    print('[0] Sair')
    
    opcao = input('Escolha uma opcao: ').strip()

    if opcao == '1':
        matricula = input('Matricula (somente numeros, min. 4 digitos): ').strip()
        nome = input('Nome do aluno: ').strip()
        curso = input('Curso (ex: ADS, Informatica): ').strip()

        if not all([matricula, nome, curso]):
            print('[!] Erro: Preencha todos os campos.')
            continue

        if not validar_matricula(matricula):
            print('[!] Erro: Matricula invalida! Digite apenas numeros (minimo 4 digitos).')
            continue

        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')

        novo_aluno = {
            'matricula': matricula,
            'nome': nome,
            'curso': curso,
            'data_matricula': data_atual
        }

        try:
           
            alunos.insert_one(novo_aluno)
            print('[OK] Aluno cadastrado com sucesso!')
        except DuplicateKeyError:
            print(f'[X] Erro: A matricula {matricula} ja esta cadastrada no sistema!')

    elif opcao == '2':
        print('\n--- Lista de Alunos Cadastrados ---')
        total = 0

        for aluno in alunos.find({}, {'_id': 0}).sort('nome', 1):
            total += 1
            data = aluno.get('data_matricula', 'Nao informada')
            print(f"- Matricula: {aluno['matricula']} | Nome: {aluno['nome']} | Curso: {aluno['curso']} | Data: {data}")
        
        if total == 0:
            print('Nenhum aluno cadastrado ate o momento.')

    elif opcao == '3':
        curso_busca = input('Digite o nome ou sigla do curso para filtrar: ').strip()
        if not curso_busca:
            print('[!] Digite um curso para pesquisar.')
            continue

        filtro = {'curso': {'$regex': curso_busca, '$options': 'i'}}
        resultados = list(alunos.find(filtro, {'_id': 0}))

        if resultados:
            print(f"\nAlunos encontrados no curso '{curso_busca}':")
            for aluno in resultados:
                print(f"- Matricula: {aluno['matricula']} | Nome: {aluno['nome']} | Curso: {aluno['curso']}")
        else:
            print(f"Nenhum aluno encontrado para o curso '{curso_busca}'.")

    elif opcao == '4':
        matricula = input('Digite a matricula do aluno que deseja alterar: ').strip()
        novo_curso = input('Digite o novo curso: ').strip()

        if novo_curso:
            resultado = alunos.update_one(
                {'matricula': matricula},
                {'$set': {'curso': novo_curso}}
            )
            if resultado.matched_count > 0:
                print('[OK] Curso do aluno atualizado com sucesso!')
            else:
                print('[X] Aluno nao encontrado para a matricula informada.')
        else:
            print('[!] O novo curso nao pode ser vazio.')

    elif opcao == '5':
        matricula = input('Digite a matricula do aluno a ser excluido: ').strip()
        resultado = alunos.delete_one({'matricula': matricula})

        if resultado.deleted_count > 0:
            print('[OK] Aluno excluido com sucesso!')
        else:
            print('[X] Aluno nao encontrado para a matricula informada.')

    elif opcao == '0':
        print('Encerrando o programa... Ate logo!')
        break

    else:
        print('[!] Opcao invalida. Digite um numero de 0 a 5.')
