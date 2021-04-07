import cx_Oracle as oci
from haversine import haversine

oracle_dsn = oci.makedsn(host="192.168.2.247", port=1521, sid="orcl")
conn = oci.connect(dsn=oracle_dsn, user="emg", password="1234566")

# class aid:
#     def __init__(self,
#                  onspot_dstn, gout_firesttn_nm, gout_safe_center_nm, statmnt_tm,emrlf_emd_nm, jurisd_div_nm_cnt, jurisd_div_nm_out
#                  salary=None, commission_pct=None,
#                  manager_id=None, department_id=None):
#         self.ONSPOT_DSTN = ONSPOT_DSTN
#         self.GOUT_FIRESTTN_NM = GOUT_FIRESTTN_NM
#         self.GOUT_SAFE_CENTER_NM = GOUT_SAFE_CENTER_NM
#         self.STATMNT_TM = STATMNT_TM
#         self.EMRLF_EMD_NM = EMRLF_EMD_NM
#         self.JURISD_DIV_NM_CNT = JURISD_DIV_NM_CNT
#         self.JURISD_DIV_NM_OUT = JURISD_DIV_NM_OUT
#         self.salary = salary
#         self.commission_pct = commission_pct
#         self.manager_id = manager_id
#         self.department_id = department_id
#
#     def __str__(self):
#         return f"{self.ONSPOT_DSTN}, {self.GOUT_FIRESTTN_NM}, {self.GOUT_SAFE_CENTER_NM}, " \
#                f"{self.STATMNT_TM}, {self.phone_number}, {self.hire_date}, " \
#                f"{self.job_id}, {self.salary}, {self.commission_pct}, " \
#                f"{self.manager_id}, {self.department_id}"
#
#     def to_dict(self):
#         return {"employee_id": self.employee_id,
#                 "first_name": self.first_name,
#                 "last_name": self.last_name,
#                 "email": self.email,
#                 "phone_number": self.phone_number,
#                 "hire_date": self.hire_date,
#                 "job_id": self.job_id,
#                 "salary": self.salary,
#                 "commission_pct": self.commission_pct,
#                 "manager_id": self.manager_id,
#                 "department_id": self.department_id}


def get_geoinfo():
    sql = "select * from locations"
    cursor = conn.cursor()
    cursor.execute(sql)
    geoinfo = cursor.fetchall()
    return geoinfo

x = 37.643217
y = 126.788109
#sample = (37.643217, 126.788109) #백석역, 받아온 좌표값으로 대체할 것

def dist(x, y):
    cursor = conn.cursor()

    sql = 'select * from locations'
    cursor.execute(sql)

    lst = []
    for i in cursor:
        center_119 = (float(i[2]), float(i[1]))
        temp = haversine((x, y), center_119, unit='km')
        lst.append((temp, i[0], i[3]))
    lst.sort()
    return (lst[0][1],lst[0][2])

def get_safe(x, y):
    cursor = conn.cursor()

    sql = 'select * from locations'
    cursor.execute(sql)

    lst = []
    for i in cursor:
        center_119 = (float(i[2]), float(i[1]))
        temp = haversine((x, y), center_119, unit='km')
        lst.append((temp, i[0], i[3]))
    lst.sort()
    return lst[0][2]

def dist_only(x, y):
    cursor = conn.cursor()

    sql = 'select * from locations'
    cursor.execute(sql)

    lst = []
    for i in cursor:
        center_119 = (float(i[2]), float(i[1]))
        temp = haversine((x, y), center_119, unit='km')
        lst.append((temp))
    lst.sort()
    return (lst[0])

a = dist(x, y)
b = get_safe(x, y)
c = dist_only(x, y)
print("dist :" + str(a))
print("safe_label : " + str(b))
print("dist_only : " + str(c))

def get_donginfo(dong_nm):
    sql = "select LABEL from DONG where DONG =:dong_nm"
    cursor = conn.cursor()
    cursor.execute(sql, {'dong_nm': dong_nm})
    donginfo = cursor.fetchone()
    dong2 = donginfo[0]
    return dong2

def get_safeinfo(safe_id):
    sql = "select safe_name from safe_center where safe_label =:safe_id"
    cursor = conn.cursor()
    cursor.execute(sql)
    safeinfo = cursor.fetchone()
    return safeinfo

dong_nm = '연무동'
b = get_donginfo(dong_nm)
print(b)
