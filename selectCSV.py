import csv

import wx
import os


class SiteLog(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='SiteLog', size=(640, 480))
        self.SelBtn = wx.Button(self, label='select', pos=(305, 5), size=(80, 25))
        self.SelBtn.Bind(wx.EVT_BUTTON, self.OnOpenFile)
        self.FileName = wx.TextCtrl(self, pos=(5, 5), size=(230, 25))

    def OnOpenFile(self, event):
        wildcard = 'CSV files(*.csv)|*.csv'
        dialog = wx.FileDialog(None, 'select', os.getcwd(), '', wildcard, wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.FileName.SetValue(dialog.GetPath())


            file = open(self.FileName.GetValue())
            with file as f:
                reader = csv.reader(f)
                result = list(reader)
                labelrow = result[22]  # get line 23
                header = result[:22]  # get first 22 lines
                labelcolumn = []
                # validate row
                standardrow = ['kV', 'mA', 'BarCode', 'XraysOn', 'HVLFilter(mm)', 'Filter', 'FilterReady', 'HVLReady', 'N',
                               'Current1(pA)', 'Current2(pA)', 'P(kPa)', 'T(MC)', 'T(Air)', 'T(SC)', 'H(%)', 'Comment']
                standardrow.sort()
                labelrow.sort()

                # validate column
                standardcolumn = ['[COMET X-RAY MEASUREMENT]', 'Filename', 'Date', 'Chamber', 'Description', 'Software',
                                  'Backgrounds', 'Measurements', 'Trolley (mm)', 'SCD (mm)', 'Aperture wheel', 'Comment',
                                  'Monitor electrometer range', 'Monitor HV', 'MEFAC-IC electrometer range', 'IC HV',
                                  'Client name', 'Address 1', 'Address 2', 'Operator', 'CAL Number', '[DATA]']
                for i in header:
                    labelcolumn.append(i[0])
                labelcolumn.sort()
                standardcolumn.sort()

                if standardrow == labelrow and standardcolumn == labelcolumn:
                    print("The data structure is valid.")
                else:
                    print("The data structure is not valid.")


            file.close()
        dialog.Destroy


if __name__ == '__main__':
    app = wx.App()
    SiteFrame = SiteLog()
    SiteFrame.Show()
    app.MainLoop()
