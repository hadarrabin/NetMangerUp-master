import time

def BytePercent(smaller_num, bigger_num):
    """
    Converts bytes to percents
    :param smaller_num: Smaller number
    :param bigger_num: Bigger number
    :return: The perecentege between the numbers
    """
    try:
        return int(round(smaller_num / float(bigger_num), 2) * 100)
    except:
        return 0

USAGE_LIMIT = 20
DISK_LIMIT = 75
class monitor(object):
    def __init__(self,clien):
        self.client = clien
        self.suspicious_processes = {}
        self.disk = {}

    def cpu_warning(self, cpuo, proc):
        """
        Seeing a process if suspicious or not.
        This function is invoked when a sepcific process usage is more then 20% from the cpu abilety

        :param cpuo: CPU() instance
        :param proc: process dictionary [key = PID, values(1- name, 2-handler)]
        :return: a boolean value that checks if a process is suspecioues and a statment
        """
        start = time.time()
        PID = proc.keys()[0]
        proc_name = proc[PID][0]
        proc_handle = proc[PID][1]
        while True:
            time.sleep(1)
            try:
                usage = cpuo.cpu_process_util(proc_handle)
            except:
                return False, 0
            if usage < USAGE_LIMIT:
                return False, usage

            now = time.time()

            if (now - start) >= 60:
                value = "(CPU) Suspicious process has been found: {} (PID: {}) has {}% of cpu using".format(str(proc_name),
                str(PID),str(usage))
                self.suspicious_processes[proc_name] = value
                return True, value

    def memory_warning(self, memoryo, proc_handle, used):
        """
        Checks if a process is suspecious or not.
        This function is ivoked when a sepcific process memory usage is more then 20%

        :param used: The used memory in percent
        :param memoryo: Memory() instance
        :param proc_handle: process handler
        :return: if suspicious (Boolean) and process handler (hprocess)
        """
        start = time.time()
        PID = proc_handle.keys()[0]
        proc_name = proc_handle[PID][0]
        proc_handle = proc_handle[PID][1]

        while True:
            time.sleep(1)
            try:
                proc_usage = BytePercent(memoryo.memory_process_usage(proc_handle), used)
            except:
                return False, 0
            if proc_usage <= USAGE_LIMIT:
                return False, proc_usage

            now = time.time()

            if (now - start) >= 60:
                value = "(Memory) Suspicious process has been found: {} (PID: {}) has {}%".format(str(proc_name),
                str(PID),str(proc_usage))
                self.suspicious_processes[proc_name] = value
                return True, proc_usage

    def disk_warning(self, Disks_Dictionary):
        """
        Checks if disk is full or is about to be full.
        This function is ivoked when a sepcific disk usage is more then 75%

        :param Disks_Dictionary: disk dictionary
        :return: a list of all the full disks
        """
        full_disks = []
        for key, disk_data in Disks_Dictionary.items():
            disk_used_percent = BytePercent(disk_data['used'], disk_data['total'])

            if disk_used_percent >= DISK_LIMIT and disk_used_percent > self.disk[key]:
                self.disk[key] = disk_used_percent
                value = "{} is {}% prety loaded".format(key, str(disk_used_percent))
                Disks_Dictionary[key].append(value)
                full_disks.append(key)
        return full_disks
