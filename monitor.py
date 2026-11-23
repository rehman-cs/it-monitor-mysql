import mysql.connector
import getpass
import subprocess
import socket
import re
import psutil
conn = mysql.connector.connect(
host="localhost",
user="root",
password=getpass.getpass("ENTER YOUR PASSWORD : ")       ,
database="it_monitor" )
my_cursor=conn.cursor()





def show_devices():
    try:
        my_cursor.execute("SELECT* FROM devices")
        devices_detail=my_cursor.fetchall()
        if not devices_detail:
            print(" NO DEVICE FOUND. ADD A DEVICE FIRST \n")
            return
        for row in devices_detail:
            print(f"DEVICE_ID: {row[0]} | NAME: {row[1]} | IP: {row[2]} | TYPE: {row[3]} | LOCATION: {row[4]} | PORT: {row[5]} \n ")
    except mysql.connector.Error as e:
        print(f" Database Error: {e} \n")
        return




def add_device():
    try:
        name       =input("ENTER DEVICE NAME :            ").strip()
        if not name:
            print("NAME CAN NOT BE EMPTY :\n")
            return
        ip_address =input("ENTER IP ADDRESS :             ").strip()
        if not ip_address:
            print("IP ADDRESS CAN NOT BE EMPTY :\n")
            return
        device_type=input("ENTER TYPE (ROUTER/SERVER/PC) :").strip()
        if not device_type:
            print("TYPE CAN NOT BE EMPTY :\n")
            return
        location   =input("ENTER LOCATION :               ").strip()
        if not location:
            print("LOCATION CAN NOT BE EMPTY :\n")
            return
        port_text  =input("ENTER PORT TO CHECK (EMPTY = NO PORT) :").strip()
        if port_text=="":
            port=None
        else:
            port=int(port_text)
            if port<1 or port>65535:
                print("PORT MUST BE BETWEEN 1 AND 65535 \n")
                return
    except ValueError:
        print("WRONG INPUT. PORT MUST BE A NUMBER \n")
        return

    try:
        query_for_adding_a_device="INSERT INTO devices (name, ip_address, device_type, location, port) VALUES (%s, %s, %s, %s, %s)"
        my_cursor.execute(query_for_adding_a_device,(name,ip_address,device_type,location,port))
        conn.commit()
        print("DEVICE ADDED SUCCESSFULLY! \n")
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Database Error: {e}")




def remove_device():
    try:
        device_id=int(input("ENTER DEVICE-ID WHICH YOU WANT TO REMOVE : "))
    except ValueError:
        print(" WRONG INPUT\n")
        return
    try:
        query_for_removing_device="DELETE FROM devices where device_id=%s"
        my_cursor.execute(query_for_removing_device,(device_id,))
        if my_cursor.rowcount == 0:
            print("DEVICE ID DOES NOT EXIST. NOTHING REMOVED.\n")
        else:
            conn.commit()
            print("DEVICE AND ITS OLD CHECKS HAVE BEEN REMOVED\n")
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"DATA BASE ERROR {e} \n")




def check_all_devices():
    try:
        my_cursor.execute("SELECT device_id, name, ip_address, port FROM devices")
        all_devices=my_cursor.fetchall()
        if not all_devices:
            print(" NO DEVICE FOUND. ADD A DEVICE FIRST \n")
            return

        print(" CHECKING ALL DEVICES. PLEASE WAIT... \n")
        for d in all_devices:
            ip_address=d[2]
            port=d[3]

            ping_result=subprocess.run(["ping","-n","1","-w","1000",ip_address],capture_output=True,text=True)
            ping_text=ping_result.stdout
            if "TTL=" in ping_text:
                status="ONLINE"
                time_found=re.search(r"(?:time|zeit)[=<](\d+)",ping_text,re.IGNORECASE)
                if time_found:
                    response_ms=int(time_found.group(1))
                else:
                    response_ms=None
            else:
                status="OFFLINE"
                response_ms=None

            if port is None:
                port_status=None
            else:
                try:
                    connection=socket.create_connection((ip_address,port),timeout=2)
                    connection.close()
                    port_status="OPEN"
                except OSError:
                    port_status="CLOSED"

            query_for_saving_check="INSERT INTO checks(device_id,check_time,status,response_ms,port_status) VALUES(%s,NOW(),%s,%s,%s)"
            my_cursor.execute(query_for_saving_check,(d[0],status,response_ms,port_status))
            print(f"NAME: {d[1]} | IP: {ip_address} | STATUS: {status} | RESPONSE: {response_ms} ms | PORT {port}: {port_status} ")

        conn.commit()
        print("\n ALL RESULTS HAVE BEEN SAVED \n")

    except mysql.connector.Error as e:
        conn.rollback()
        print(f"\nCheck failed! Changes rolled back. Error: {e}\n")




def check_this_pc():
    cpu =psutil.cpu_percent(interval=1)
    ram =psutil.virtual_memory().percent
    disk=psutil.disk_usage("C:\\").percent
    print(f"\n CPU: {cpu} % | RAM: {ram} % | DISK: {disk} % ")
    if cpu>90 or ram>90 or disk>90:
        print(" WARNING: ONE VALUE IS ABOVE 90 % \n")

    try:
        query_for_saving_pc_values="INSERT INTO system_stats(stat_time,cpu_percent,ram_percent,disk_percent) VALUES(NOW(),%s,%s,%s)"
        my_cursor.execute(query_for_saving_pc_values,(cpu,ram,disk))
        conn.commit()
        print("\n PC VALUES HAVE BEEN SAVED \n")
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Database Error: {e} \n")




def show_device_history():
    try:
        device_id=int(input("ENTER DEVICE-ID TO SEE ITS CHECKS : "))
    except ValueError:
        print("ENTER A VALID NUMBER \n")
        return

    try:
        query_for_cheaking_device_id="SELECT* FROM devices where device_id=%s"
        my_cursor.execute(query_for_cheaking_device_id,(device_id,))
        device=my_cursor.fetchone()
        if device is None:
            print(" DEVICE ID DOES NOT EXIST. \n")
            return

        query_for_device_history="""
                   SELECT
                   check_time,
                   status,
                   response_ms,
                   port_status

                   FROM checks
                   WHERE device_id=%s
                         ORDER BY check_time DESC """
        my_cursor.execute(query_for_device_history,(device_id,))
        history=my_cursor.fetchall()
        if not history:
            print(" NO CHECK FOUND FOR THIS DEVICE. RUN A CHECK FIRST (OPTION 4) \n")
            return
        print(f" CHECKS OF {device[1]} ({device[2]}) - NEWEST FIRST \n")
        for h in history:
            print(f"TIME = {h[0]} | STATUS = {h[1]} | RESPONSE = {h[2]} ms | PORT = {h[3]} \n ")
    except mysql.connector.Error as e:
        print(f" Database Error: {e} \n")




def availability_report():
    try:
        query_for_availability_report="""
                   SELECT
                   d.name,
                   d.ip_address,
                   COUNT(c.check_id) as total_checks,
                   SUM(c.status='ONLINE') as online_checks,
                   ROUND(SUM(c.status='ONLINE')*100/COUNT(c.check_id),1) as availability_percent,
                   ROUND(AVG(c.response_ms),1) as average_ms

                   FROM devices as d
                   JOIN checks as c
                        ON d.device_id=c.device_id
                   GROUP BY d.device_id, d.name, d.ip_address
                         ORDER BY availability_percent ASC """
        my_cursor.execute(query_for_availability_report)
        report=my_cursor.fetchall()
        if not report:
            print(" NO CHECK FOUND. RUN A CHECK FIRST (OPTION 4) ")
            return
        print(" AVAILABILITY REPORT (WORST DEVICE FIRST) \n")
        for r in report:
            print(f"NAME = {r[0]} | IP = {r[1]} | CHECKS = {r[2]} | ONLINE = {r[3]} | AVAILABILITY = {r[4]} % | AVERAGE RESPONSE = {r[5]} ms \n ")
    except mysql.connector.Error as e:
        print(f" Database Error: {e} \n")




def update_device():
    try:
        device_id=int(input("ENTER DEVICE-ID WHICH YOU WANT TO UPDATE : "))
    except ValueError:
        print("ENTER A VALID NUMBER \n")
        return

    try:
        query_for_cheaking_device_id="SELECT* FROM devices where device_id=%s"
        my_cursor.execute(query_for_cheaking_device_id,(device_id,))
        device=my_cursor.fetchone()
        if device is None:
            print(" DEVICE ID DOES NOT EXIST. \n")
            return
    except mysql.connector.Error as e:
        print(f" Database Error: {e} \n")
        return

    print(f"OLD IP: {device[2]} | OLD PORT: {device[5]}")
    try:
        ip_address=input("ENTER NEW IP ADDRESS :                 ").strip()
        if not ip_address:
            print("IP ADDRESS CAN NOT BE EMPTY :\n")
            return
        port_text =input("ENTER NEW PORT (EMPTY = NO PORT) :     ").strip()
        if port_text=="":
            port=None
        else:
            port=int(port_text)
            if port<1 or port>65535:
                print("PORT MUST BE BETWEEN 1 AND 65535 \n")
                return
    except ValueError:
        print("WRONG INPUT. PORT MUST BE A NUMBER \n")
        return

    try:
        query_for_updating_device="UPDATE devices SET ip_address=%s, port=%s where device_id=%s"
        my_cursor.execute(query_for_updating_device,(ip_address,port,device_id))
        conn.commit()
        print(" DEVICE HAS BEEN UPDATED \n")
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"DATA BASE ERROR {e} \n")






while True:
    print(" \nPLEASE CHOOSE ONE OF THE OPTIONS FROM BELOW ")
    print(" 1:  Show     Devices        ")
    print(" 2:  Add      Device         ")
    print(" 3:  Remove   Device         ")
    print(" 4:  CHECK    ALL DEVICES    ")
    print(" 5:  CHECK    THIS PC        ")
    print(" 6:  SHOW     DEVICE HISTORY ")
    print(" 7:  AVAILABILITY REPORT     ")
    print(" 8:  UPDATE   DEVICE         ")
    print(" 9: Exit                     ")
    option=input(" CHOOSE :  ")
    if   option=="1":
        show_devices()
    elif option=="2":
        add_device()
    elif option=="3":
        remove_device()
    elif option=="4":
        check_all_devices()
    elif option=="5":
        check_this_pc()
    elif option=="6":
        show_device_history()
    elif option=="7":
        availability_report()
    elif option=="8":
        update_device()
    elif option=="9":
        my_cursor.close()
        conn.close()
        print("Exiting IT monitor. Goodbye!")
        break
    else:
        print(" \nPLEASE ENTER A VALID VALUE (1-9): \n")
