import json

from streamlit_elements import mui
from .dashboard import Dashboard


class DataGrid(Dashboard.Item):
    DEFAULT_COLUMNS = [
        { "field": 'id', "headerName": 'ID', "width": 90 },
        { "field": 'space_name', "headerName": '空间名称', "width": 90 },
        { "field": 'volume', "headerName": '空间体积(m3)', "width": 150, "editable": True, },
        { "field": 'space_heat_capacitance', "headerName": '空间热容(kJ/K)',  "width": 110, "editable": True, },
        { "field": 'envelope_heat_resistance', "headerName": '围护体热阻(K/kW)',  "width": 110, "editable": True, },
        { "field": 'neighbor_heat_conductance', "headerName": '近邻热感(K/(H.kJ))',  "width": 110, "editable": True, },
        { "field": 'average_heat_load', "headerName": '典型热负荷(kJ)',  "width": 110, "editable": True, },
        { "field": 'average_fresh_air_demand', "headerName": '典型需求新风量(m3/h)',  "width": 110, "editable": True, },
    ]

    DEFAULT_ROWS = [
        { "id": 1, "space_name": '病房区域I', "空间体积(m3)": 210, "空间热容(kJ/K)": 35, "围护体热阻(K/kW)": 1.3 , '近邻热感(K/(H.kJ))': 2.1, '典型热负荷(kJ)':200, '典型需求新风量(m3/h)': 10000},
        { "id": 2, "space_name": '病房区域II', "空间体积(m3)": 210, "空间热容(kJ/K)": 42, "围护体热阻(K/kW)": 1.3 , '近邻热感(K/(H.kJ))': 2.1, '典型热负荷(kJ)':200, '典型需求新风量(m3/h)': 10000},
        { "id": 3, "space_name": '办公区域', "空间体积(m3)": 1190, "空间热容(kJ/K)": 45, "围护体热阻(K/kW)": 1.3 , '近邻热感(K/(H.kJ))': 2.1, '典型热负荷(kJ)':200, '典型需求新风量(m3/h)': 10000},
        { "id": 4, "space_name": '公共走廊', "空间体积(m3)": 1071, "空间热容(kJ/K)": 16, "围护体热阻(K/kW)": 1.3 , '近邻热感(K/(H.kJ))': 2.1, '典型热负荷(kJ)':200, '典型需求新风量(m3/h)': 10000},
        { "id": 5, "space_name": '娱乐活动区', "空间体积(m3)": 420, "空间热容(kJ/K)": 32, "围护体热阻(K/kW)": 1.3 , '近邻热感(K/(H.kJ))': 2.1, '典型热负荷(kJ)':200, '典型需求新风量(m3/h)': 10000},
    ]



    def _handle_edit(self, params):
        print(params)

    def __call__(self, title, COLUMNS, json_data):
        #try:
        #    data = json.loads(json_data)
        #except json.JSONDecodeError:
        #    data = self.DEFAULT_ROWS
        data = json.loads(json_data)
        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=True):
                mui.icon.ViewCompact()
                mui.Typography(title)


            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                
                mui.DataGrid(
                    columns=COLUMNS,
                    rows=data,
                    color='Blue',
                    pageSize=5,
                    rowsPerPageOptions=[5],
                    checkboxSelection=True,
                    disableSelectionOnClick=True,
                    onCellEditCommit=self._handle_edit,
                )
