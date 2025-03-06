class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.advance()
        self.code = []
        self.temp_counter = 0  # Adicionado para gerar nomes de variáveis temporárias

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def match(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Erro de sintaxe: esperava '{token_type}', obteve '{self.current_token[0]}'")

    def programa(self):
        self.declaracoes()
        self.comandos()

    def declaracoes(self):
        while self.current_token and self.current_token[0] in ['int', 'real']:
            self.declaracao()
            self.match(';')

    def declaracao(self):
        tipo = self.current_token[0]
        self.match(self.current_token[0])  # tipo
        self.lista_variaveis(tipo)

    def lista_variaveis(self, tipo):
        var_name = self.current_token[1]
        self.match('ID')
        self.code.append(f"DECLARE {var_name} {tipo}")
        while self.current_token and self.current_token[0] == ',':
            self.match(',')
            var_name = self.current_token[1]
            self.match('ID')
            self.code.append(f"DECLARE {var_name} {tipo}")

    def comandos(self):
        while self.current_token:
            if self.current_token[0] == 'EOF':
                return
            elif self.current_token[0] == '}':
                return
            elif self.current_token[0] == 'ID':
                self.atribuicao()
            elif self.current_token[0] == 'while':
                self.repeticao()
            elif self.current_token[0] == 'if':
                self.fluxo_controle()
            else:
                raise SyntaxError(f"Erro de sintaxe: token inesperado '{self.current_token[0]}'")

    def atribuicao(self):
        var = self.current_token[1]
        self.match('ID')
        self.match('=')
        expr = self.expressao()
        self.match(';')
        temp_var = self.new_temp()
        self.code.append(f"{temp_var} = {expr}")
        self.code.append(f"{var} = {temp_var}")

    def repeticao(self):
        self.match('while')
        self.match('(')
        cond = self.expressao_relacional()
        self.match(')')
        self.match('{')
        start_label = f"WHILE_{self.index}"
        end_label = f"END_WHILE_{self.index}"
        self.code.append(f"LABEL {start_label}")
        self.code.append(f"IF {cond} <= 0 GOTO {end_label}")
        self.comandos()
        self.match('}')
        self.code.append(f"GOTO {start_label}")
        self.code.append(f"LABEL {end_label}")

    def fluxo_controle(self):
        self.match('if')
        self.match('(')
        cond = self.expressao_relacional()
        self.match(')')
        self.match('{')
        else_label = f"ELSE_{self.index}"
        end_if_label = f"END_IF_{self.index}"
        self.code.append(f"IF {cond} <= 0 GOTO {else_label}")
        self.comandos()
        self.match('}')
        if self.current_token and self.current_token[0] == 'else':
            self.match('else')
            self.match('{')
            self.code.append(f"GOTO {end_if_label}")
            self.code.append(f"LABEL {else_label}")
            self.comandos()
            self.match('}')
        else:
            self.code.append(f"LABEL {else_label}")
        self.code.append(f"LABEL {end_if_label}")

    def expressao(self):
        termo = self.termo()
        expr = termo
        while self.current_token and self.current_token[0] in ['+', '-', '*', '/']:
            op = self.current_token[0]
            self.match(op)
            termo = self.termo()
            expr = f"{expr} {op} {termo}"
        return expr

    def termo(self):
        fator = self.fator()
        term = fator
        while self.current_token and self.current_token[0] == '^':
            self.match('^')
            fator = self.fator()
            term = f"{term} ^ {fator}"
        return term

    def fator(self):
        if self.current_token[0] == 'ID' or self.current_token[0] == 'NUMERO':
            valor = self.current_token[1]
            self.match(self.current_token[0])
            return valor
        elif self.current_token[0] == '(':
            self.match('(')
            expr = self.expressao()
            self.match(')')
            return f"({expr})"
        else:
            raise SyntaxError("Erro de sintaxe: fator esperado")

    def expressao_relacional(self):
        expr1 = self.expressao()
        op = self.current_token[0]
        self.match(self.current_token[0])
        expr2 = self.expressao()
        return f"{expr1} {op} {expr2}"

    def new_temp(self):
        temp_var = f"T{self.temp_counter}"
        self.temp_counter += 1
        return temp_var

tokens = [
    ('int', ''), ('ID', 'x'), (';', ''),
    ('int', ''), ('ID', 'y'), (';', ''),
    ('while', ''), ('(', ''), ('ID', 'a'),
    ('>', ''), ('ID', 'b'), (')', ''), ('{', ''),
    ('ID', 'x'), ('=', ''), ('ID', 'x'), ('+', ''), ('ID', 'y'), (';', ''),
    ('}', ''), ('EOF', '')
]

try:
    parser = Parser(tokens)
    parser.programa()
    print("Análise sintática bem-sucedida!")
    print("Código Intermediário Gerado:")
    for line in parser.code:
        print(line)
except SyntaxError as e:
    print(f"Erro de sintaxe: {e}")
