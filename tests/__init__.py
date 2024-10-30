from abc import ABC, abstractmethod

# Excepciones
class LongitudInvalidaError(Exception):
    pass

class FaltaMayusculaError(Exception):
    pass

class FaltaMinusculaError(Exception):
    pass

class FaltaNumeroError(Exception):
    pass

class FaltaCaracterEspecialError(Exception):
    pass

class CalistoInvalidoError(Exception):
    pass

# Clase abstracta de reglas de validación
class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    def _validar_longitud(self, clave):
        """Verifica si la clave tiene la longitud mínima requerida."""
        if len(clave) <= self._longitud_esperada:
            raise LongitudInvalidaError("La clave no tiene la longitud mínima requerida.")
        return True

    def _contiene_mayuscula(self, clave):
        """Verifica si la clave contiene al menos una letra mayúscula."""
        if not any(char.isupper() for char in clave):
            raise FaltaMayusculaError("La clave debe contener al menos una letra mayúscula.")
        return True

    def _contiene_minuscula(self, clave):
        """Verifica si la clave contiene al menos una letra minúscula."""
        if not any(char.islower() for char in clave):
            raise FaltaMinusculaError("La clave debe contener al menos una letra minúscula.")
        return True

    def _contiene_numero(self, clave):
        """Verifica si la clave contiene al menos un número."""
        if not any(char.isdigit() for char in clave):
            raise FaltaNumeroError("La clave debe contener al menos un número.")
        return True

    @abstractmethod
    def es_valida(self, clave):
        """Método abstracto para verificar si una clave es válida según la regla."""
        pass

# Regla de Validación Ganímedes
class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(longitud_esperada=8)

    def contiene_caracter_especial(self, clave):
        """Verifica si la clave contiene al menos un carácter especial."""
        caracteres_especiales = "@_#$%"
        if not any(char in caracteres_especiales for char in clave):
            raise FaltaCaracterEspecialError("La clave debe contener al menos un carácter especial (@, _, #, $, %).")
        return True

    def es_valida(self, clave):
        """Verifica todas las reglas de Ganímedes en orden."""
        self._validar_longitud(clave)
        self._contiene_mayuscula(clave)
        self._contiene_minuscula(clave)
        self._contiene_numero(clave)
        self.contiene_caracter_especial(clave)
        return True

# Regla de Validación Calisto
class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(longitud_esperada=6)

    def contiene_calisto(self, clave):
        """Verifica si la clave contiene la palabra 'calisto' con al menos dos letras en mayúscula, pero no todas."""
        indice = clave.lower().find("calisto")
        if indice == -1:
            raise CalistoInvalidoError("La clave no contiene la palabra 'calisto'.")

        subcadena = clave[indice:indice + 7]
        mayusculas = sum(1 for char in subcadena if char.isupper())

        if mayusculas < 2 or mayusculas == len(subcadena):
            raise CalistoInvalidoError("La palabra 'calisto' debe tener al menos dos letras en mayúscula, pero no todas.")
        return True

    def es_valida(self, clave):
        """Verifica todas las reglas de Calisto en orden."""
        self._validar_longitud(clave)
        self._contiene_numero(clave)
        self.contiene_calisto(clave)
        return True

# Clase Validador
class Validador:
    def __init__(self, regla: ReglaValidacion):
        self.regla = regla

    def es_valida(self, clave: str) -> bool:
        """Retorna si la clave es válida según la regla proporcionada."""
        return self.regla.es_valida(clave)
