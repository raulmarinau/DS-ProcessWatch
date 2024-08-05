from enum import Enum


class Modes(Enum):
    centralized = "centralized"
    ring        = "ring"
    alltoall    = "alltoall"
    gossip      = "gossip"


class Roles(Enum):
    server = "server"
    client = "client"
