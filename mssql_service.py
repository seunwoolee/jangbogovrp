import pymssql
from rest_framework.response import Response


class MssqlMixin:

    def __init__(self):
        self._HOST = "211.195.9.131:4171"
        self._NAME = "DB_Jang_Erp"
        self._USER = "sa"
        self._PASS = "rootdb1234!@#$"

        self.conn: pymssql.Connection = pymssql.connect(host=self._HOST, user=self._USER,
                                                        password=self._PASS,
                                                        database=self._NAME, charset='utf8')
        self.cursor: pymssql.Cursor = self.conn.cursor()


class ERPDB(MssqlMixin):
    def get_order_data(self, company_code: str = '003', is_am: bool = True) -> list:
        """
        프로시저 명 : Iregen_OrderSheet_Ready_List_Vehicle

        매개변수들 :
        $CRUN		= "MONITER"; -> 필요없어보임
        $CorpCode	= "10001";//1001
        $StartDDay	= '2020-09-03';
        $EndDDay	= '2020-09-03';
        $pStCode	= '003';
        $StCode		= '003';	//"0006"
        $IsMorning	= '1';

        :param company_code: 회사 코드(월배점 003)
        :param is_am: (오전, 오후) 오전(a) = 1, 오후면(b) = 2
        :return: order data list
        """

        CRUN = " "
        CorpCode = "10001"
        StartDDay = '2020-09-03'
        EndDDay = '2020-09-03'
        pStCode = '003'
        StCode = '003'
        IsMorning = '1'

        if is_am == False:
            IsMorning = '2'

        result = []

        self.cursor.callproc('Iregen_OrderSheet_Ready_List_Vehicle',
                             (CRUN, CorpCode, StartDDay, EndDDay, pStCode, StCode, IsMorning))

        for _ in self.cursor:  # 첫번째 프로시저 결과값 PASS
            pass

        self.cursor.nextset()

        for i, row in enumerate(self.cursor):
            temp_dict = {}
            temp_dict['id'] = i + 1
            temp_dict['orderNumber'] = row[0]
            temp_dict['locationId'] = "3"
            temp_dict['deliveryDate'] = i + 1
            temp_dict['no'] = i + 1
            temp_dict['jusoSubid'] = "1"
            temp_dict['lat'] = row[30]
            temp_dict['lon'] = row[29]
            temp_dict['isNew'] = "1"
            temp_dict['isShop'] = "0"
            temp_dict['flag'] = "1"
            temp_dict['isRoad'] = "n"
            temp_dict['pay'] = row[12]
            temp_dict['address'] = row[23]
            temp_dict['guestTel'] = ""
            temp_dict['name'] = row[7]
            temp_dict['guestId'] = row[6]
            temp_dict['meridiemType'] = "0"
            temp_dict['deliveryDate'] = row[22]
            result.append(temp_dict)
        return result
