''' connection manager for peer vms'''

from common.logger import Logger


class ConnManager():
    ''' connection manager class '''
    def __init__(self):
        self.conns = {
            "ds-vm-1": "10.128.0.3",
            "ds-vm-2": "10.128.0.6",
            "ds-vm-3": "10.128.0.10",
            "ds-vm-4": "10.128.0.12",
        }

    def get_ip(self, vm):
        if vm not in self.conns.keys():
            Logger.warn("VM not in list")
        return self.conns[vm]

    def get_pair(self, vm):
        if vm not in self.conns.keys():
            Logger.warn("VM not in list")
        elif vm == "ds-vm-1":
            return self.conns['ds-vm-2']
        elif vm == "ds-vm-2":
            return self.conns['ds-vm-3']
        elif vm == "ds-vm-3":
            return self.conns['ds-vm-4']
        elif vm == "ds-vm-4":
            return self.conns['ds-vm-1']

    def get_peers(self, vm):
        if vm not in self.conns.keys():
            Logger.warn("VM not in list")
        return [ ip for vm_name, ip in self.conns.items() if vm != vm_name]
