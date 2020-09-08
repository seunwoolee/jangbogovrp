import pymssql
import pymysql
from pymysql.cursors import DictCursor
from rest_framework.response import Response


class MysqlMixin:

    def __init__(self):
        self._HOST = "14.63.164.165"
        self._NAME = "jangboja_wolbae"
        self._USER = "root"
        self._PASS = "jangboja^^12"
        self.conn: pymysql.Connection = pymysql.connect(host=self._HOST, user=self._USER,
                                                        password=self._PASS,
                                                        db=self._NAME, charset='utf8', cursorclass=DictCursor)
        self.cursor: pymysql.cursors = self.conn.cursor()


class DB(MysqlMixin):
    def get_delivery_list(self, start_date: str, end_date: str) -> list:
        query = f" SELECT s.vs_seq," \
                f" s.vs_deliveryDate," \
                f" s.vs_meridiemType," \
                f" s.vs_meridiemFlag," \
                f" SUM(vr_distanceValue) AS totalDistance, " \
                f" COUNT(vr_seq) AS counts," \
                f" SUM(vr_deguestPay) AS pay" \
                f" FROM vehicleAllocateStatus AS s" \
                f" LEFT JOIN vehicleAllocateResult AS r ON s.vs_deliveryDate = r.vr_deliveryDate " \
                f" AND s.vs_meridiemType = r.vr_meridiemType" \
                f" WHERE s.vs_deliveryDate >= '{start_date}' AND r.vr_deliveryDate <= '{end_date}'" \
                f" AND s.vs_locationId='3'" \
                f" AND r.vr_deguestName <> 'guestName'" \
                f" AND s.vs_vehicleEndStatus='Y'" \
                f" GROUP BY s.vs_deliveryDate, s.vs_meridiemType, s.vs_meridiemFlag" \
                f" HAVING counts > 0" \
                f" ORDER BY s.vs_deliveryDate DESC"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_vehicle_allocate_status(self, vs_seq: str) -> dict:
        query = f"SELECT * FROM vehicleAllocateStatus WHERE vs_seq = {vs_seq}"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_map_group_list(self, delivery_date: str, is_am: str) -> list:
        query = f"SELECT A.vr_vehicleNo AS vehicleNo " \
                f",COUNT(distinct vr_deguestLat,vr_deguestLon) AS count " \
                f",SUM(A.vr_distanceValue) AS sum " \
                f",SUM(A.vr_deguestPay) AS deguestPay " \
                f",A.vr_meridiemFlag AS meridiemFlag " \
                f",A.vr_deliveryDate AS deliveryDate " \
                f"FROM (SELECT * FROM vehicleAllocateResult WHERE 1=1 " \
                f"AND vr_deliveryDate='{delivery_date}' " \
                f"AND vr_meridiemType='{is_am}' " \
                f"AND vr_locationId='3' " \
                f"AND vr_meridiemFlag='1' " \
                f"AND vr_deguestName <> 'guestName' " \
                f"GROUP BY vr_vehicleNo,vr_vehicleNoIndex) AS A " \
                f"GROUP BY A.vr_vehicleNo " \
                f"ORDER BY A.vr_vehicleNo*1 ASC, A.vr_vehicleNoIndex ASC "
        self.cursor.execute(query)

        results: list = self.cursor.fetchall()

        for result in results:
            result['vehicle_results'] = []

        query = f"SELECT * FROM vehicleAllocateResult " \
                f"WHERE vr_deliveryDate = '{delivery_date}' " \
                f" AND vr_meridiemType = '{is_am}' " \
                f" AND vr_deguestName <> 'guestName' " \
                f" AND vr_locationId='3' " \
                f" AND vr_meridiemFlag='1' "
        self.cursor.execute(query)

        for vehicle_result in self.cursor.fetchall():
            results[int(vehicle_result['vr_vehicleNo'])]['vehicle_results'].append(vehicle_result)

        return results
