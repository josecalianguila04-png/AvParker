"""
Funções utilitárias do Bot AvParker
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def log_message(level: str, message: str, extra: dict = None):
    """
    Log uma mensagem com informações adicionais
    
    Args:
        level: Nível de log (INFO, WARNING, ERROR, DEBUG)
        message: Mensagem a logar
        extra: Informações adicionais
    """
    extra_str = f" | {extra}" if extra else ""
    
    if level.upper() == "INFO":
        logger.info(f"{message}{extra_str}")
    elif level.upper() == "WARNING":
        logger.warning(f"{message}{extra_str}")
    elif level.upper() == "ERROR":
        logger.error(f"{message}{extra_str}")
    elif level.upper() == "DEBUG":
        logger.debug(f"{message}{extra_str}")


def get_timestamp() -> str:
    """
    Obter timestamp atual formatado
    
    Returns:
        String com timestamp no formato YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_duration(seconds: float) -> str:
    """
    Formatar duração em segundos para formato legível
    
    Args:
        seconds: Duração em segundos
    
    Returns:
        String formatada (ex: "1h 30m 45s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def validate_command(command: str) -> bool:
    """
    Validar se um comando é válido
    
    Args:
        command: Comando a validar
    
    Returns:
        True se válido, False caso contrário
    """
    if not command or not isinstance(command, str):
        return False
    
    # Comando deve ter apenas letras, números e underline
    return all(c.isalnum() or c == '_' for c in command)


class CommandHandler:
    """Handler para gerenciar comandos"""
    
    def __init__(self):
        """Inicializar handler de comandos"""
        self.commands = {}
        logger.info("CommandHandler inicializado")
    
    def register(self, command: str, handler):
        """
        Registrar um novo comando
        
        Args:
            command: Nome do comando
            handler: Função a executar
        """
        if validate_command(command):
            self.commands[command] = handler
            logger.info(f"Comando registrado: {command}")
        else:
            logger.warning(f"Comando inválido: {command}")
    
    def execute(self, command: str, *args, **kwargs):
        """
        Executar um comando registrado
        
        Args:
            command: Nome do comando
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
        """
        if command in self.commands:
            try:
                return self.commands[command](*args, **kwargs)
            except Exception as e:
                logger.error(f"Erro ao executar comando '{command}': {e}")
                return None
        else:
            logger.warning(f"Comando não encontrado: {command}")
            return None
