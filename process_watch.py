''' main module for process watch '''
import sys
import socket

from common import types, connections
from common.logger import Logger
from server.server import SimpleServer
from client.client import SimpleClient, MultiConnClient

modes = [mode.value for mode in types.Modes]
roles = [role.value for role in types.Roles]
SERVER_PORT = 1337

if len(sys.argv) == 3 and sys.argv[1] in roles and sys.argv[2] in modes:
    role = types.Roles(sys.argv[1])
    mode = types.Modes(sys.argv[2])

    Logger.info(f"Starting {sys.argv[1]} in mode {sys.argv[2]}")
else:
    Logger.info(f"Incorrect args")
    Logger.info(f"Usage: python process_watch.py (client|server) {modes}")
    sys.exit(1)

hostname = socket.gethostname()
Logger.info(f"Running on host: {hostname}")

conn_manager = connections.ConnManager()
peer_vms_ips = conn_manager.get_peers(socket.gethostname())

if mode is types.Modes.centralized:
    if role is types.Roles.server:
        sserv = SimpleServer(host=conn_manager.get_ip('ds-vm-1'),
                port=SERVER_PORT, connections=peer_vms_ips)
        Logger.info(sserv)
        sserv.start_listening()
    elif role is types.Roles.client:
        sclnt = SimpleClient(host=conn_manager.get_ip('ds-vm-1'), port=SERVER_PORT)
        Logger.info(sclnt)
        sclnt.send()
elif mode is types.Modes.ring:
    if role is types.Roles.server:
        sserv = SimpleServer(host=conn_manager.get_ip(hostname),
                connections=peer_vms_ips)
        Logger.info(sserv)
        sserv.start_listening()
    elif role is types.Roles.client:
        sclnt = SimpleClient(host=conn_manager.get_pair(hostname), port=SERVER_PORT)
        Logger.info(sclnt)
        sclnt.send()
elif mode is types.Modes.alltoall:
    if role is types.Roles.server:
        sserv = SimpleServer(host=conn_manager.get_ip(hostname),
                connections=peer_vms_ips)
        Logger.info(sserv)
        sserv.start_listening()
    elif role is types.Roles.client:
        multiclnt = MultiConnClient(connections=peer_vms_ips)
        multiclnt.send()

