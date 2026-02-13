import subprocess
from typing import Union, List, Dict, Optional


def run_command(
    command: Union[str, List[str]],
    timeout: int = 60
) -> Dict[str, Optional[str]]:
    """
    Ejecuta un comando del sistema y devuelve resultados estructurados.

    :param command: Comando como string o lista
    :param timeout: Tiempo máximo en segundos
    :return: dict con:
        - success (bool)
        - stdout (str)
        - stderr (str)
        - returncode (int | None)
        - timeout (bool)
        - error_type (str | None)
    """

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=isinstance(command, str)
        )

        success = result.returncode == 0

        return {
            "success": success,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "timeout": False,
            "error_type": None if success else "execution_error"
        }

    except subprocess.TimeoutExpired as e:
        return {
            "success": False,
            "stdout": e.stdout or "",
            "stderr": e.stderr or "",
            "returncode": None,
            "timeout": True,
            "error_type": "timeout"
        }

    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": None,
            "timeout": False,
            "error_type": "system_error"
        }
