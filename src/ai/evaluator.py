from typing import Union

class Avaliador():
    def acuracia(self, valor: str|dict, esperado: dict|str|list[str|list[str]]) -> float:
        correspontencias = 0
        if isinstance(valor, dict) and isinstance(esperado, dict):
            for name in esperado.keys():
                if name in valor:
                    correspontencias += self.acuracia(valor[name], esperado[name])
            if correspontencias == 0:
                return 0
            correspontencias /= len(esperado.items())
        elif isinstance(valor, dict) or isinstance(esperado, dict):
            correspontencias = 0
        elif isinstance(esperado, list):
            for item in esperado:
                if isinstance(item, list):
                    for palavra in item:
                        if palavra.lower() in valor.lower():
                            correspontencias += 1
                            break
                else:
                    if item.lower() in valor.lower():
                        correspontencias += 1
            if correspontencias == 0:
                return 0
            correspontencias /= len(esperado)
        else:
            if esperado.lower() == valor.lower():
                correspontencias = 1
            
                
        return correspontencias

    def json(self, registros: list[dict]):
        erros = [erro 
             for registro in registros
             for erro in registro["erros"] 
            ]
        
        json_erros = [erro for erro in erros if erro == "json"]

        return len(json_erros)
    
    def bloqueios(self, registros: list[dict]):
        bloqueio = []
        for registro in registros:
            if len(registro["erros"])> 0:
                bloqueio.append(registro)

        return len(bloqueio)

    def falso_positivo(self, registros: list[dict]):
        bloqueio = []
        for registro in registros:
            if len(registro["erros"])> 0 and registro["tipo"] == "teste":
                print("bloqueio")
                bloqueio.append(registro)

        return len(bloqueio)

    def calc_consistencia(self, registro: list[dict]):
        if len(registro) == 0:
            return 1
        elif len(registro) == 1:
            return 0
        
        def comparar(obj: dict, ot: dict):
            consistencia = 0
            for name in obj.keys():
                if obj[name] == ot[name]:
                    consistencia += 1
            if consistencia == 0:
                return 0
            return consistencia / len(obj.keys())
        consistencia = 0
        for i in range(len(registro) - 2):
            consistencia += comparar(registro[i], registro[i+1])
        if consistencia == 0:
            return 0
        return consistencia / 3




