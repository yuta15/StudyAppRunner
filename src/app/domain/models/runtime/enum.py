from enum import Enum


class RuntimeStatus(Enum):
    CREATING="CREATING"
    RUNNING = "RUNNING"
    STOPPING="STOPPING"
    STOPPED="STOPPED"
    FAILED="FAILED"
    EXPIRED="EXPIRED"
