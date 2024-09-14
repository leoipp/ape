import PyQt5.QtCore
from Database.Manejo import Manejo


class APEX(PyQt5.QtCore.QThread):
    barra_att = PyQt5.QtCore.pyqtSignal(int)
    bar_max = PyQt5.QtCore.pyqtSignal(int)
    fim = PyQt5.QtCore.pyqtSignal()

    def __init__(self, pbar, db, check_remanescentes):
        super().__init__()
        self.pbar = pbar
        self.db = Manejo(db)
        self.rem = check_remanescentes

    def run(self):
        steps = 36 if self.rem else 34  # Total number of steps in your pipeline
        self.bar_max.emit(steps)  # Emit the maximum value for the progress bar

        step_count = 0

        # Define a helper function to increment the progress and emit the signal
        def progress():
            nonlocal step_count
            step_count += 1
            self.barra_att.emit(step_count)

        # Start the pipeline
        self.db.create_table_with_repeated_rows('CustosSilvicultura_REF_REG', 'CustosSilvicultura_REF_REF', 7)
        progress()

        self.db.update_column_based_on_another_table('CustosSilvicultura_REF_REF', 'ANO', 'CustosSilvicultura_REF_REG', 'ANO', 'id')
        progress()

        cols_to_update = ['BO', 'IP', 'PO', 'CO', 'PI', 'SB', 'SA', 'VI']
        self.db.CustoTerra('CustosSilvicultura_REF_REF', cols_to_update, 8)

        self.db.CustosSilviculturaVPL('CustosSilvicultura_REF_REG', 'CustosSilvicultura_REF_REG_VPL', 'ANO')
        progress()

        self.db.CustosSilviculturaVPL('CustosSilvicultura_REF_REF', 'CustosSilvicultura_REF_REF_VPL', 'ANO')
        progress()

        cols = self.db.list_columns('CustosSilvicultura_REF_REG')[3:]
        self.db.create_summary_table_by_regiao('CustosSilvicultura_REF_REG_VPL', 'CustosSilvicultura_REF_REG_VPL_Total', cols, 7)
        progress()

        self.db.create_summary_table_by_regiao('CustosSilvicultura_REF_REF_VPL', 'CustosSilvicultura_REF_REF_VPL_Total', cols, 7)
        progress()

        self.db.ResInclinacao()
        progress()

        self.db.CustosColheita()
        progress()

        n = len([x for x in self.db.list_tables() if x.startswith('Apex_Manejo')])
        goal = f'Apex_Manejo_{n + 1}'

        self.db.create_table_from_another('apex_base_1', goal)
        progress()

        self.db.ESPAreaBasal(goal)
        progress()

        self.db.update_curva_and_vol7(goal)
        progress()

        self.db.perdas(goal)
        progress()

        self.db.CustoMADPE(goal, 'CustosSilvicultura_REF_REG_VPL', 'CustosSilvicultura_REF_REG_VPL_Total', 'CustoMADPE_REF_REG', 'Vol7', 'Vol7_2ROT')
        progress()

        self.db.CustoMADPE(goal, 'CustosSilvicultura_REF_REF_VPL', 'CustosSilvicultura_REF_REF_VPL_Total', 'CustoMADPE_REF_REF', 'Vol7', 'Vol7_1ROT')
        progress()

        acrescimo_colheita = (float(self.db.Parameters('Parametros')[10])) / 100

        self.db.CustosColheitaOP(goal, 'REF_REG', '2ROT', acrescimo_colheita)
        progress()

        self.db.CustosColheitaOP(goal, 'REF_REF', '1ROT', acrescimo_colheita)
        progress()

        self.db.CustosApoioColheita(goal, 'REF_REG', '2ROT')
        progress()

        self.db.CustosApoioColheita(goal, 'REF_REF', '1ROT')
        progress()

        self.db.CustosColheitaEstradaInterna(goal, 'REF_REG', '2ROT')
        progress()

        self.db.CustosColheitaEstradaInterna(goal, 'REF_REF', '1ROT')
        progress()

        self.db.CustosColheitaTotal(goal, 'REF_REG')
        progress()

        self.db.CustosColheitaTotal(goal, 'REF_REF')
        progress()

        self.db.CustosTransporteGeral(goal)
        progress()

        self.db.OutrosCustos(goal, 'REF_REG', '2ROT')
        progress()

        self.db.OutrosCustos(goal, 'REF_REF', '1ROT')
        progress()

        self.db.CustosPostoFabrica(goal, 'REF_REG')
        progress()

        self.db.CustosPostoFabrica(goal, 'REF_REF')
        progress()

        self.db.CustoMadAV(goal)
        progress()

        self.db.AVPipeline(goal)
        progress()

        self.db.t700(goal)
        progress()

        self.db.APEX(goal)
        progress()

        if self.rem:
            t_700 = f'Manejo_Apex_t700_{n + 1}'
            self.db.create_table_from_another(goal, t_700, ['Talhao', 'ManejoAPEX'])
            progress()

            self.db.t700(t_700)
            progress()

            self.db.t700_organizador(goal, t_700)
            progress()
        else:
            self.db.t700_organizador(goal, None)
            progress()

        self.db.create_table_from_existing_schema('ParametrosHistorico', 'Parametros')
        progress()
        self.db.insert_last_row_into_table('Parametros', 'ParametrosHistorico')
        progress()

        # Emit the completion signal
        self.fim.emit()
