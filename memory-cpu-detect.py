import csv
import os
import time
import pandas as pd

now_cpu_list = []
now_ram_list = []
now_time_list = []

package_name = "com.example.kkn+"
cmd = f'adb shell "top -d 1 -n 1|grep {package_name}"'


def save_to_csv():
    df = pd.DataFrame({'CPU': now_cpu_list, '内存': now_ram_list, '时间': now_time_list})
    now = time.strftime("%H-%M-%S", time.localtime())
    file_name = now + ".csv"
    df.to_csv(file_name, index=False)
    print(f"save {file_name}")


def get_cpu_and_mem():
    global now_cpu_list, now_ram_list, now_time_list
    while True:
        end_time = time.time()
        if (end_time - start_time) / 60 >= tol_time:  # 分钟
            break
        # try:
        str_init = ''
        data = os.popen(cmd).readlines()
        for i in range(len(data)):
            str_init += data[i]
        # print(str_init)
        str_list = str_init.split()
        # CPU & 内存
        # print(str_list)
        try:
            ram = str_list[9].replace('K', '')
            cpu = str_list[8].replace('%', '')
        except Exception as e:
            print(f"此刻读不出数据，str_list = {str_list}, exception = {e}")
            ram = "can't catch the RAM data"
            cpu = "can't catch the CPU data"
        now = time.strftime("%H:%M:%S", time.localtime())
        print('CPU:', cpu, '内存:', ram, '时间:', now)

        # 数据添加到列表中
        now_cpu_list.append(cpu)
        now_ram_list.append(ram)
        now_time_list.append(now)
        time.sleep(1)
        if len(now_cpu_list) >= 3600:
            save_to_csv()
            now_cpu_list = []
            now_ram_list = []
            now_time_list = []
            print("------ 分片 ------")

        # except Exception as e:
        #     print('inside exception:', e)
        #     break


if __name__ == '__main__':
    start_time = time.time()
    tol_time = int(input("请输入脚本执行时间(分钟)："))
    try:
        get_cpu_and_mem()
    except Exception as e:
        print("outside exception: ", e)
    finally:
        save_to_csv()
    print("end")
    os.system("pause")
