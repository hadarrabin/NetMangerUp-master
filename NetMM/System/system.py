__author__ = 'Hadar'

from subprocess import Popen, PIPE
import win32api #win32
import win32pdh #win32
import win32process #win32
import multiprocessing  #win32
import _winreg  #win32
from System.Monitor import * #monitoring the usage of the computer resources (critical!!!!)
import ctypes   # C language writing in python environment (used to get low level details)
from ctypes import * # C language writing in python environment (used to get low level details)
from ctypes.wintypes import * # C language writing in python environment (used to get low level details)

# ============================================================================ STATIC PARAMETRS
CPU_LIMIT = 65
PROCESS_USAGE_LIMIT = (100/multiprocessing.cpu_count()) + 1

def bytes2percent(smaller_num, bigger_num):
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

# -- DLL --
KERNEL_32 = windll.Kernel32
GetDiskFreeSpaceExW = windll.kernel32.GetDiskFreeSpaceExW

# -- Security --
ALL_PROCESS_ACCESS = (0x000F0000L | 0x00100000L | 0xFFF)

def get_registry_value(key, subkey, value):
    """
    Finds a value from the registry editor in windows
    :param key: (HKEY_CLASSES_ROOT | HKEY_CURRENT_USER | HKEY_LOCAL_MACHINE | HKEY_USERS | HKEY_CURRENT_CONFIG)
    :param subkey: The folders under param: key
    :param value: The filed that we want to find its value
    :return: value of param: value
    """

    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return value

# ============================================================================ CPU
class FILETIME(Structure):
    _fields_ = [
        ("dwLowDateTime", DWORD),
        ("dwHighDateTime", DWORD)]


# ============================================================================ Memory
class MEMORYSTATUSEX(Structure):
    _fields_ = [
        ("dwLength", c_ulong),
        ("dwMemoryLoad", c_ulong),
        ("ullTotalPhys", c_ulonglong),
        ("ullAvailPhys", c_ulonglong),
        ("ullTotalPageFile", c_ulonglong),
        ("ullAvailPageFile", c_ulonglong),
        ("ullTotalVirtual", c_ulonglong),
        ("ullAvailVirtual", c_ulonglong),
        ("sullAvailExtendedVirtual", c_ulonglong),
    ]


class PROCESS_MEMORY_COUNTERS_EX(Structure):
    _fields_ = [
        ('cb', DWORD),
        ('PageFaultCount', DWORD),
        ('PeakWorkingSetSize', c_size_t),
        ('WorkingSetSize', c_size_t),
        ('QuotaPeakPagedPoolUsage', c_size_t),
        ('QuotaPagedPoolUsage', c_size_t),
        ('QuotaPeakNonPagedPoolUsage', c_size_t),
        ('QuotaNonPagedPoolUsage', c_size_t),
        ('PagefileUsage', c_size_t),
        ('PeakPagefileUsage', c_size_t),
        ('PrivateUsage', c_size_t),
    ]

proc = KERNEL_32.OpenProcess(ALL_PROCESS_ACCESS, False, 14436)


def bytes2percent(smaller_num, bigger_num):
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
# ============================================================================ System

class System:
    def __init__(self):
        self.processes = {}
        self.process_obj = 'process'
        self.item = 'ID Process'
        self.os_version = self.get_os_version()
        self.UUID = self.get_computer_UUID()
        self.user_name = win32api.GetUserName()

    def get_user_name(self):
        """
        By using win32api we return the user's name
        :return user_name(string)
        """
        return win32api.GetUserName()

    def get_os_version(self):
        """
        By using the regisry, we export the operation system's version
        :return: os_version(string)
        """

        return get_registry_value(
            "HKEY_LOCAL_MACHINE",
            "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            "ProductName")

    def get_computer_UUID(self):
        uuid = Popen(['wmic', 'csproduct', 'get', 'UUID'], stdout=PIPE, stdin=PIPE)
        return uuid.communicate()[0].split()[1]

    def get_processes_dict(self):
        """
        returns a dictionary that contains all the processes PIDs as keys and names as values.
        :return: processes dictionary as described above.
        """

        try:
            # Getting all processes name
            z, proc_name = win32pdh.EnumObjectItems(None, None, self.process_obj, win32pdh.PERF_DETAIL_WIZARD)# PERF_DETAIL_WIZARD = 400
            instances = {}
            for instance in proc_name:
                if instance in instances:
                    instances[instance] += 1
                else:
                    instances[instance] = 1
            proc_pid_name = {}
            for instance, max_instances in instances.items():
                for inum in xrange(max_instances + 1):
                    try:
                        hq = win32pdh.OpenQuery()  # initializes the query handle
                        path = win32pdh.MakeCounterPath((None, self.process_obj, instance, None, inum, self.item))
                        counter_handle = win32pdh.AddCounter(hq, path)  # convert counter path to counter handle
                        win32pdh.CollectQueryData(hq)  # collects data for the counter
                        type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)

                        proc_pid_name[val] = [instance]

                        win32pdh.CloseQuery(hq)
                    except:
                        raise OSError("Problem getting process id")

            return proc_pid_name

        except:
            try:
                from win32com.client import GetObject
                WMI = GetObject('winmgmts:')  # COM object
                proc_instances = WMI.InstancesOf('Win32_Process')  # WMI instanse

                proc_name = [process.Properties_('Name').Value for process in
                             proc_instances]  # Get the processess names

                proc_id = [process.Properties_('ProcessId').Value for process in
                           proc_instances]  # Get the processess names

                proc_pid_name = {}

                proc_id_counter = 0
                for instance in range(len(proc_name)):
                    proc_pid_name[proc_id[instance]] = [(proc_name[instance])]
                    proc_id_counter += 1

                return proc_pid_name

            except:
                raise OSError('Counldnt get the process list')

    def get_windows(self):
        """
        Return a list which contains the opened windows titles.
        :return: title (list)
        """

        EnumWindows = ctypes.windll.user32.EnumWindows  # Filters all opened windows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int),
                                             ctypes.POINTER(ctypes.c_int))  # Callback function. Returns a tuple
        GetWindowText = ctypes.windll.user32.GetWindowTextW  # Get all the window's title
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW  # Gets the exact buffer size of the title
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible  # Filters all the visible windows

        titles = []

        def foreach_window(hwnd):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                titles.append(buff.value)
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)  # Callback
        return titles

    def create_process_handle_dict(self, procsses):
        """
        Adds a handle to each process in the sent dictionary
        :param procsses: a dictionary of all the processes as the key is the PID and the value is the name
        :return: adds to the dictionary for every key a second value which is a handle in a int format
        """
        for pid in procsses:
            proc_handle = ctypes.windll.Kernel32.OpenProcess(ALL_PROCESS_ACCESS, False, pid)
            procsses[pid].append(proc_handle)


    def close_process_handle(self, proc_handle):
        """
        Closes a given process handle
        :param proc_handle: process handle
        :return: None
        """
        ctypes.windll.Kernel32.CloseHandle(proc_handle)
        return

    def add_each_process_using_cpu(self,cpu,processes):
        """
        adds to the dictionary a value that represents each process using
        :param cpu: CPU object
        :param processes: a dictionary of all the process formated(key - PID, first value - name, second value - handle)
        :return:None
        """
        for proces in processes:
            processes[proces].append(cpu.cpu_process_util(processes[proces][1]))

    def run(self):
        """
        Runs System class
        :return:
        """
        new_pid_dict = self.get_processes_dict()

        if not new_pid_dict:
            pass

        new_processes = set(new_pid_dict) - set(self.processes)
        closed_processes = set(self.processes) - set(new_pid_dict)

        new_processes_dict = {}
        closed_processes_dict = {}

        if len(new_processes) > 0:
            self.create_process_handle_dict(new_pid_dict)
            for pid in new_processes:
                self.processes.update({pid: new_pid_dict[pid]})
                new_processes_dict.update({pid: new_pid_dict[pid]})

        if len(closed_processes) > 0:
            for pid in closed_processes:
                closed_processes_dict.update({pid: self.processes[pid]})
                self.close_process_handle(self.processes[pid][1])
                self.processes[pid][1] = 0  # The place of 1 is the process handle
                self.processes.pop(pid, None)

        return new_processes_dict, closed_processes_dict

    def recieve_system_basic_info(self, info_list):
        info_list.append(self.UUID)
        info_list.append(self.user_name)
        info_list.append(self.os_version)

# ============================================================================ CPU


class CPU:
    def __init__(self, monitor):
        self.sys = None
        self.monitor = monitor
        self.cpu_model = self.get_cpu_model()
        self.cpus_num = self.get_cpu_num()

    def get_cpu_model(self):
        """
        Return the CPU model
        :return: CPU model (string)
        """
        return get_registry_value(
            "HKEY_LOCAL_MACHINE",
            "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
            "ProcessorNameString")

    def get_cpu_num(self):
        return multiprocessing.cpu_count()

    def GetSystemTimes(self):

        """
        Uses the function GetSystemTimes() (win32) in order to get the user mode time, kernel mode time and idle mode time
        :return: user time, kernel time and idle time (Dictinary)
        """

        __GetSystemTimes = windll.kernel32.GetSystemTimes
        idleTime, kernelTime, userTime = FILETIME(), FILETIME(), FILETIME()

        success = __GetSystemTimes(

            byref(idleTime),
            byref(kernelTime),
            byref(userTime))

        assert success, ctypes.WinError(ctypes.GetLastError())[1]

        return {
            "idleTime": idleTime.dwLowDateTime,
            "kernelTime": kernelTime.dwLowDateTime,
            "userTime": userTime.dwLowDateTime}

    def cpu_utilization(self):
        """
        Returns the total cpu usage

        Source: http://www.codeproject.com/Articles/9113/Get-CPU-Usage-with-GetSystemTimes
        :return: CPU usage (int)
        """

        FirstSystemTimes = self.GetSystemTimes()
        time.sleep(1)
        SecSystemTimes = self.GetSystemTimes()

        """
         CPU usage is calculated by getting the total amount of time
         the system has operated since the last measurement
         made up of kernel + user) and the total
         amount of time the process has run (kernel + user).
        """

        usr = SecSystemTimes['userTime'] - FirstSystemTimes['userTime']
        ker = SecSystemTimes['kernelTime'] - FirstSystemTimes['kernelTime']
        idl = SecSystemTimes['idleTime'] - FirstSystemTimes['idleTime']
        self.sys = usr + ker
        return int((self.sys - idl) * 100 / self.sys)

    def cpu_process_util(self, hproc):
        """
        Returns the process usage of CPU
        ** self.cpu_utilization() must run first!!
        Source: http://www.philosophicalgeek.com/2009/01/03/determine-cpu-usage-of-current-process-c-and-c/
        :param hproc: Process handle
        :return: Process CPU usage (int)
        """

        # hproc = proc
        if hproc == 0:
            return 0
        FirstProcessTimes = win32process.GetProcessTimes(hproc)
        time.sleep(1)
        SecProcessTimes = win32process.GetProcessTimes(hproc)

        """
         Process CPU usage is calculated by getting the total amount of time
         the system has operated since the last measurement
         made up of kernel + user) and the total
         amount of time the process has run (kernel + user).
        """

        proc_time_user_prev = FirstProcessTimes['UserTime']
        proc_time_kernel_prev = FirstProcessTimes['KernelTime']

        proc_time_user = SecProcessTimes['UserTime']
        proc_time_kernel = SecProcessTimes['KernelTime']

        proc_usr = proc_time_user - proc_time_user_prev
        proc_ker = proc_time_kernel - proc_time_kernel_prev

        proc_total_time = proc_usr + proc_ker

        proc_utilization = (100 * proc_total_time) / self.sys
        return proc_utilization

    def run(self, proc):
        """
        Runs CPU class
        :param proc: A process dictinary (dict)
        :return:
        """

        pid = proc.keys()[0]
        handle_proc = proc[pid][1]
        while True:
            time.sleep(1)

            if handle_proc == 0:
                return

            cpu_usage = self.cpu_utilization()
            if cpu_usage > CPU_LIMIT:
                try:
                    process_usage = self.cpu_process_util(handle_proc)
                except:
                    break
                if process_usage > PROCESS_USAGE_LIMIT:
                    suspicious = self.monitor.cpu_warning(self, proc)
                    if not suspicious[0]:
                        continue
            time.sleep(100)
    def recieve_cpu_basic_info(self,info_list):
        info_list.append(self.cpu_model)
        info_list.append(self.cpus_num)

# ============================================================================ Memory




class Memory:
    def __init__(self, monitor):
        self.monitor = monitor
        self.memory_size = self.RAM_memory()[0]
        self.memory_free_size = self.RAM_memory()[1]


    def RAM_memory(self):
        """
        Returning the total and the free amount of ram
        :return: total and the availabe ram (int tuple)
        """
        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        KERNEL_32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
        return memoryStatus.ullTotalPhys, memoryStatus.ullAvailPhys

    def memory_utilization(self):
        (Total, Avail) = self.RAM_memory()
        return BytePercent(Avail, Total)

    def memory_process_usage(self, proc_handle):
        """
        Return Win32 process memory counters structure as a dictionary.
        :param proc_handle: Process handle
        :returns WorkingSetSize of memory (int)
        """
        GetProcessMemoryInfo = ctypes.windll.psapi.GetProcessMemoryInfo
        counters = PROCESS_MEMORY_COUNTERS_EX()

        ret = GetProcessMemoryInfo(proc_handle, ctypes.byref(counters),
                                   ctypes.sizeof(counters))
        if not ret:
            raise ctypes.WinError()

        return counters.WorkingSetSize

    def run(self, proc):
        """
        Runs the class
        :param proc: process dictinary (dict)
        :return: None
        """
        total = self.RAM_memory()[0]
        pid = proc.keys()[0]
        proc_handle = proc[pid][1]

        while 1:
            if proc_handle == 0:
                return
            avail = self.RAM_memory()[1]
            used = total - avail
            used_usage = BytePercent(used, total)
            if used_usage > 40:
                try:
                    proc_usage = BytePercent(self.memory_process_usage(proc_handle), used)
                except:
                    break
                if proc_usage >= 10:
                    suspicious = self.monitor.memory_warning(self, proc, used)
                    if not suspicious[0]:
                        continue
            time.sleep(100)

    def recieve_ram_basic_info(self,info_list):
        info_list.append(self.memory_size)

# ============================================================================ Disk

class Disk:

    def __init__(self, monitor):
        self.monitor = monitor
        self.disk_C_size = self.get_disk_size()

        self.disk_dict = {}
        self.disk_get_partitions()
        self.disk_usage()

    def get_disk_size(self):
        print ("which size of data do you prefer to recieve the information in:\n1)bytes\n2)kilobytes\n3)megabytes\n4)gigabytes")
        num = int(raw_input("press the number of the size you want"))
        n_free_user, self.disk_C_size, n_free = win32api.GetDiskFreeSpaceEx(r"C:\\")
        self.sizechose(num)
        return self.disk_C_size


    def sizechose(self,num):
        if num == 1:
            pass
        if num == 2:
            self.disk_C_size = (self.disk_C_size/1024)
        if num == 3:
            self.disk_C_size = (self.disk_C_size/(1024*1024))
        if num == 4:
            self.disk_C_size = (self.disk_C_size(1024*1024*1024))


    def disk_get_partitions(self):
        """
        Fills the keys of self.disk_dict.
        The keys are the devices which connected to the computer.

        :return: None
        """
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        for drive in drives:
            self.disk_dict[drive] = {}

    def disk_usage(self):
        """
        Getting information about every device in self.disk_dict.
        :return: None
        """
        freeuser = ctypes.c_int64()
        total = ctypes.c_int64()
        free = ctypes.c_int64()
        for drive in self.disk_dict:
            GetDiskFreeSpaceExW(unicode(drive), ctypes.byref(freeuser), ctypes.byref(total), ctypes.byref(free))
            self.disk_dict[drive] = {'total': total.value,
                                     'used': (total.value - free.value)}

    def run(self):
        """
        Runs Disk class
        :return:
        """
        self.monitor.disk = dict.fromkeys(self.disk_dict)
        while True:
            self.monitor.disk_warning(self.disk_dict)
            time.sleep(1800)  # 30 minutes

    def recieve_basic_disk_info(self,info_list):
        info_list.append(self.disk_C_size)


def recieve_starting_info(clien):
    """
    :return: a list of basic inforamtion about the client to be presented in the GUI at the server
    the list consists the following objects:
    system : 1)the UUID, 2)user name, 3)operating system version
    CPU:1)the cpu model, 2)the number of cores
    RAM Memory: 1) the RAM size, 2)the current free RAM size(will be updated regulary)
    DISK: 1)the disk C size, 2) the partitions amount and size
    """
    starting_info_list = []
    systemo = System()
    systemo.run()
    systemo.recieve_system_basic_info(starting_info_list)
    monit = monitor(clien)
    cpuo = CPU(monit)
    processd = systemo.get_processes_dict()
    systemo.create_process_handle_dict(processd)

    cpuo.recieve_cpu_basic_info(starting_info_list)
    memoryo = Memory(monit)
    memoryo.recieve_ram_basic_info(starting_info_list)
    disko = Disk(monit)
    disko.recieve_basic_disk_info(starting_info_list)
    print starting_info_list
    return starting_info_list







