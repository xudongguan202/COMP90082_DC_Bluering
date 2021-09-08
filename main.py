import wx
import wx.xrc
import wx.grid as grid
import numpy as np
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt = True)
        frame = MainFrame()
        #frame = GraphFrame()
        frame.Show()

class MainFrame(wx.Frame):
    def __init__(self, title = 'App', pos = wx.DefaultPosition, size = wx.Size( 1200,864 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL):
        # super().__init__(None, title = title)
        super().__init__(None, id=wx.ID_ANY, title=u"Digital Calibration Generator", pos=wx.DefaultPosition,
                         size=wx.Size(1100, 700), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.InitFrame()

    def InitFrame(self):
        self.SetSizeHints(wx.Size(1100, 700), wx.Size(1100, 700))

        bSizer_main = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_left = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(700, -1), wx.TAB_TRAVERSAL)
        self.m_panel_left.SetMinSize(wx.Size(700, -1))
        self.m_panel_left.SetMaxSize(wx.Size(700, -1))

        bSizer_left = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_show_run = wx.Panel(self.m_panel_left, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 40),
                                         wx.TAB_TRAVERSAL)
        self.m_panel_show_run.SetMinSize(wx.Size(-1, 40))
        self.m_panel_show_run.SetMaxSize(wx.Size(-1, 40))

        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel28 = wx.Panel(self.m_panel_show_run, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TAB_TRAVERSAL)
        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_total_run = wx.StaticText(self.m_panel28, wx.ID_ANY, u"Total Runs", wx.Point(-1, -1),
                                                    wx.DefaultSize, 0)
        self.m_staticText_total_run.Wrap(-1)

        bSizer15.Add(self.m_staticText_total_run, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl_total_run = wx.TextCtrl(self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                wx.DefaultSize, wx.TE_READONLY)
        bSizer15.Add(self.m_textCtrl_total_run, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel28.SetSizer(bSizer15)
        self.m_panel28.Layout()
        bSizer15.Fit(self.m_panel28)
        bSizer14.Add(self.m_panel28, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel281 = wx.Panel(self.m_panel_show_run, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_selected_run = wx.StaticText(self.m_panel281, wx.ID_ANY, u"Selected Runs", wx.DefaultPosition,
                                                       wx.DefaultSize, 0)
        self.m_staticText_selected_run.Wrap(-1)

        bSizer16.Add(self.m_staticText_selected_run, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl_selected_run = wx.TextCtrl(self.m_panel281, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                   wx.DefaultSize, wx.TE_READONLY)
        bSizer16.Add(self.m_textCtrl_selected_run, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel281.SetSizer(bSizer16)
        self.m_panel281.Layout()
        bSizer16.Fit(self.m_panel281)
        bSizer14.Add(self.m_panel281, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel282 = wx.Panel(self.m_panel_show_run, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer17 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button_confirm = wx.Button(self.m_panel282, wx.ID_ANY, u"Confirm", wx.DefaultPosition, wx.Size(100, 30),
                                          0)
        self.m_button_confirm.SetMinSize(wx.Size(100, 30))
        self.m_button_confirm.SetMaxSize(wx.Size(100, 30))

        bSizer17.Add(self.m_button_confirm, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.confirm, self.m_button_confirm)

        self.m_button_compare = wx.Button(self.m_panel282, wx.ID_ANY, u"Compare", wx.DefaultPosition, wx.Size(100, 30),
                                          0)
        self.m_button_compare.SetMinSize(wx.Size(100, 30))
        self.m_button_compare.SetMaxSize(wx.Size(100, 30))

        bSizer17.Add(self.m_button_compare, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.Bind(wx.EVT_BUTTON, self.compare, self.m_button_compare)

        self.m_panel282.SetSizer(bSizer17)
        self.m_panel282.Layout()
        bSizer17.Fit(self.m_panel282)
        bSizer14.Add(self.m_panel282, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_show_run.SetSizer(bSizer14)
        self.m_panel_show_run.Layout()
        bSizer_left.Add(self.m_panel_show_run, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_pbar = wx.Panel(self.m_panel_left, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 30),
                                     wx.TAB_TRAVERSAL)
        self.m_panel_pbar.SetMinSize(wx.Size(-1, 30))
        self.m_panel_pbar.SetMaxSize(wx.Size(-1, 30))

        bSizer18 = wx.BoxSizer(wx.VERTICAL)

        self.m_gauge_bar = wx.Gauge(self.m_panel_pbar, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(500, -1),
                                    wx.GA_HORIZONTAL)
        self.m_gauge_bar.SetValue(80)
        bSizer18.Add(self.m_gauge_bar, 0, wx.ALL | wx.EXPAND, 5)

        self.m_panel_pbar.SetSizer(bSizer18)
        self.m_panel_pbar.Layout()
        bSizer_left.Add(self.m_panel_pbar, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_upload1 = wx.Panel(self.m_panel_left, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TAB_TRAVERSAL)
        sbSizer_run1 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel_upload1, wx.ID_ANY, u"Run 1"), wx.VERTICAL)

        bSizer_run1_inside = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file = wx.Panel(sbSizer_run1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          wx.TAB_TRAVERSAL)
        bSizer24 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel39 = wx.Panel(self.m_panel_run1_file, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TAB_TRAVERSAL)
        bSizer27 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run11 = wx.FilePickerCtrl(self.m_panel39, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run11.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run11.SetMaxSize(wx.Size(600, -1))

        bSizer27.Add(self.m_filePicker_run11, 0, wx.ALL, 1)

        self.m_panel39.SetSizer(bSizer27)
        self.m_panel39.Layout()
        bSizer27.Fit(self.m_panel39)
        bSizer24.Add(self.m_panel39, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel40 = wx.Panel(self.m_panel_run1_file, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TAB_TRAVERSAL)
        bSizer271 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run12 = wx.FilePickerCtrl(self.m_panel40, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run12.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run12.SetMaxSize(wx.Size(600, -1))

        bSizer271.Add(self.m_filePicker_run12, 0, wx.ALL, 1)

        self.m_panel40.SetSizer(bSizer271)
        self.m_panel40.Layout()
        bSizer271.Fit(self.m_panel40)
        bSizer24.Add(self.m_panel40, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file.SetSizer(bSizer24)
        self.m_panel_run1_file.Layout()
        bSizer24.Fit(self.m_panel_run1_file)
        bSizer_run1_inside.Add(self.m_panel_run1_file, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check = wx.Panel(sbSizer_run1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1),
                                           wx.TAB_TRAVERSAL)
        bSizer_run1_check = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run1 = wx.CheckBox(self.m_panel_run1_check, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(-1, -1), 0)
        bSizer_run1_check.Add(self.m_checkBox_run1, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check.SetSizer(bSizer_run1_check)
        self.m_panel_run1_check.Layout()
        bSizer_run1_check.Fit(self.m_panel_run1_check)
        bSizer_run1_inside.Add(self.m_panel_run1_check, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run1.Add(bSizer_run1_inside, 1, wx.EXPAND, 1)

        self.m_panel_upload1.SetSizer(sbSizer_run1)
        self.m_panel_upload1.Layout()
        sbSizer_run1.Fit(self.m_panel_upload1)
        bSizer_left.Add(self.m_panel_upload1, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_upload2 = wx.Panel(self.m_panel_left, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TAB_TRAVERSAL)
        sbSizer_run11 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel_upload2, wx.ID_ANY, u"Run 2"), wx.VERTICAL)

        bSizer_run1_inside1 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file1 = wx.Panel(sbSizer_run11.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.TAB_TRAVERSAL)
        bSizer241 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel391 = wx.Panel(self.m_panel_run1_file1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer272 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run21 = wx.FilePickerCtrl(self.m_panel391, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run21.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run21.SetMaxSize(wx.Size(600, -1))

        bSizer272.Add(self.m_filePicker_run21, 0, wx.ALL, 1)

        self.m_panel391.SetSizer(bSizer272)
        self.m_panel391.Layout()
        bSizer272.Fit(self.m_panel391)
        bSizer241.Add(self.m_panel391, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel401 = wx.Panel(self.m_panel_run1_file1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer2711 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run22 = wx.FilePickerCtrl(self.m_panel401, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run22.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run22.SetMaxSize(wx.Size(600, -1))

        bSizer2711.Add(self.m_filePicker_run22, 0, wx.ALL, 1)

        self.m_panel401.SetSizer(bSizer2711)
        self.m_panel401.Layout()
        bSizer2711.Fit(self.m_panel401)
        bSizer241.Add(self.m_panel401, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file1.SetSizer(bSizer241)
        self.m_panel_run1_file1.Layout()
        bSizer241.Fit(self.m_panel_run1_file1)
        bSizer_run1_inside1.Add(self.m_panel_run1_file1, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check1 = wx.Panel(sbSizer_run11.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition,
                                            wx.Size(70, -1), wx.TAB_TRAVERSAL)
        self.m_panel_run1_check1.SetMinSize(wx.Size(70, -1))
        self.m_panel_run1_check1.SetMaxSize(wx.Size(70, -1))

        bSizer_run1_check1 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run2 = wx.CheckBox(self.m_panel_run1_check1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(-1, -1), 0)
        bSizer_run1_check1.Add(self.m_checkBox_run2, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check1.SetSizer(bSizer_run1_check1)
        self.m_panel_run1_check1.Layout()
        bSizer_run1_inside1.Add(self.m_panel_run1_check1, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run11.Add(bSizer_run1_inside1, 1, wx.EXPAND, 1)

        self.m_panel_upload2.SetSizer(sbSizer_run11)
        self.m_panel_upload2.Layout()
        sbSizer_run11.Fit(self.m_panel_upload2)
        bSizer_left.Add(self.m_panel_upload2, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_upload3 = wx.Panel(self.m_panel_left, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TAB_TRAVERSAL)
        sbSizer_run12 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel_upload3, wx.ID_ANY, u"Run 3"), wx.VERTICAL)

        bSizer_run1_inside2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file2 = wx.Panel(sbSizer_run12.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.TAB_TRAVERSAL)
        bSizer242 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel392 = wx.Panel(self.m_panel_run1_file2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer273 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run31 = wx.FilePickerCtrl(self.m_panel392, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run31.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run31.SetMaxSize(wx.Size(600, -1))

        bSizer273.Add(self.m_filePicker_run31, 0, wx.ALL, 1)

        self.m_panel392.SetSizer(bSizer273)
        self.m_panel392.Layout()
        bSizer273.Fit(self.m_panel392)
        bSizer242.Add(self.m_panel392, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel402 = wx.Panel(self.m_panel_run1_file2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer2712 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run32 = wx.FilePickerCtrl(self.m_panel402, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run32.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run32.SetMaxSize(wx.Size(600, -1))

        bSizer2712.Add(self.m_filePicker_run32, 0, wx.ALL, 1)

        self.m_panel402.SetSizer(bSizer2712)
        self.m_panel402.Layout()
        bSizer2712.Fit(self.m_panel402)
        bSizer242.Add(self.m_panel402, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file2.SetSizer(bSizer242)
        self.m_panel_run1_file2.Layout()
        bSizer242.Fit(self.m_panel_run1_file2)
        bSizer_run1_inside2.Add(self.m_panel_run1_file2, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check2 = wx.Panel(sbSizer_run12.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition,
                                            wx.Size(70, -1), wx.TAB_TRAVERSAL)
        self.m_panel_run1_check2.SetMinSize(wx.Size(70, -1))
        self.m_panel_run1_check2.SetMaxSize(wx.Size(70, -1))

        bSizer_run1_check2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run3 = wx.CheckBox(self.m_panel_run1_check2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(-1, -1), 0)
        bSizer_run1_check2.Add(self.m_checkBox_run3, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check2.SetSizer(bSizer_run1_check2)
        self.m_panel_run1_check2.Layout()
        bSizer_run1_inside2.Add(self.m_panel_run1_check2, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run12.Add(bSizer_run1_inside2, 1, wx.EXPAND, 1)

        self.m_panel_upload3.SetSizer(sbSizer_run12)
        self.m_panel_upload3.Layout()
        sbSizer_run12.Fit(self.m_panel_upload3)
        bSizer_left.Add(self.m_panel_upload3, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_upload4 = wx.Panel(self.m_panel_left, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TAB_TRAVERSAL)
        sbSizer_run13 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel_upload4, wx.ID_ANY, u"Run 4"), wx.VERTICAL)

        bSizer_run1_inside3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file3 = wx.Panel(sbSizer_run13.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.TAB_TRAVERSAL)
        bSizer243 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel393 = wx.Panel(self.m_panel_run1_file3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer274 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run41 = wx.FilePickerCtrl(self.m_panel393, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run41.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run41.SetMaxSize(wx.Size(600, -1))

        bSizer274.Add(self.m_filePicker_run41, 0, wx.ALL, 1)

        self.m_panel393.SetSizer(bSizer274)
        self.m_panel393.Layout()
        bSizer274.Fit(self.m_panel393)
        bSizer243.Add(self.m_panel393, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel403 = wx.Panel(self.m_panel_run1_file3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer2713 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run42 = wx.FilePickerCtrl(self.m_panel403, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run42.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run42.SetMaxSize(wx.Size(600, -1))

        bSizer2713.Add(self.m_filePicker_run42, 0, wx.ALL, 1)

        self.m_panel403.SetSizer(bSizer2713)
        self.m_panel403.Layout()
        bSizer2713.Fit(self.m_panel403)
        bSizer243.Add(self.m_panel403, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file3.SetSizer(bSizer243)
        self.m_panel_run1_file3.Layout()
        bSizer243.Fit(self.m_panel_run1_file3)
        bSizer_run1_inside3.Add(self.m_panel_run1_file3, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check3 = wx.Panel(sbSizer_run13.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition,
                                            wx.Size(70, -1), wx.TAB_TRAVERSAL)
        self.m_panel_run1_check3.SetMinSize(wx.Size(70, -1))
        self.m_panel_run1_check3.SetMaxSize(wx.Size(70, -1))

        bSizer_run1_check3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run4 = wx.CheckBox(self.m_panel_run1_check3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(-1, -1), 0)
        bSizer_run1_check3.Add(self.m_checkBox_run4, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check3.SetSizer(bSizer_run1_check3)
        self.m_panel_run1_check3.Layout()
        bSizer_run1_inside3.Add(self.m_panel_run1_check3, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run13.Add(bSizer_run1_inside3, 1, wx.EXPAND, 1)

        self.m_panel_upload4.SetSizer(sbSizer_run13)
        self.m_panel_upload4.Layout()
        sbSizer_run13.Fit(self.m_panel_upload4)
        bSizer_left.Add(self.m_panel_upload4, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_upload5 = wx.Panel(self.m_panel_left, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TAB_TRAVERSAL)
        sbSizer_run14 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel_upload5, wx.ID_ANY, u"Run 5"), wx.VERTICAL)

        bSizer_run1_inside4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_run1_file4 = wx.Panel(sbSizer_run14.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.TAB_TRAVERSAL)
        bSizer244 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel394 = wx.Panel(self.m_panel_run1_file4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer275 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run51 = wx.FilePickerCtrl(self.m_panel394, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run51.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run51.SetMaxSize(wx.Size(600, -1))

        bSizer275.Add(self.m_filePicker_run51, 0, wx.ALL, 1)

        self.m_panel394.SetSizer(bSizer275)
        self.m_panel394.Layout()
        bSizer275.Fit(self.m_panel394)
        bSizer244.Add(self.m_panel394, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel404 = wx.Panel(self.m_panel_run1_file4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer2714 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_filePicker_run52 = wx.FilePickerCtrl(self.m_panel404, wx.ID_ANY, wx.EmptyString, u"Select a file",
                                                    u"*.csv", wx.DefaultPosition, wx.Size(600, -1),
                                                    wx.FLP_DEFAULT_STYLE)
        self.m_filePicker_run52.SetMinSize(wx.Size(600, -1))
        self.m_filePicker_run52.SetMaxSize(wx.Size(600, -1))

        bSizer2714.Add(self.m_filePicker_run52, 0, wx.ALL, 1)

        self.m_panel404.SetSizer(bSizer2714)
        self.m_panel404.Layout()
        bSizer2714.Fit(self.m_panel404)
        bSizer244.Add(self.m_panel404, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file4.SetSizer(bSizer244)
        self.m_panel_run1_file4.Layout()
        bSizer244.Fit(self.m_panel_run1_file4)
        bSizer_run1_inside4.Add(self.m_panel_run1_file4, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check4 = wx.Panel(sbSizer_run14.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition,
                                            wx.Size(70, -1), wx.TAB_TRAVERSAL)
        self.m_panel_run1_check4.SetMinSize(wx.Size(70, -1))
        self.m_panel_run1_check4.SetMaxSize(wx.Size(70, -1))

        bSizer_run1_check4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run5 = wx.CheckBox(self.m_panel_run1_check4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(-1, -1), 0)
        bSizer_run1_check4.Add(self.m_checkBox_run5, 0, wx.ALL | wx.EXPAND, 15)

        self.m_panel_run1_check4.SetSizer(bSizer_run1_check4)
        self.m_panel_run1_check4.Layout()
        bSizer_run1_inside4.Add(self.m_panel_run1_check4, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer_run14.Add(bSizer_run1_inside4, 1, wx.EXPAND, 1)

        self.m_panel_upload5.SetSizer(sbSizer_run14)
        self.m_panel_upload5.Layout()
        sbSizer_run14.Fit(self.m_panel_upload5)
        bSizer_left.Add(self.m_panel_upload5, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_left.SetSizer(bSizer_left)
        self.m_panel_left.Layout()
        bSizer_main.Add(self.m_panel_left, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_right = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(400, -1), wx.TAB_TRAVERSAL)
        self.m_panel_right.SetMinSize(wx.Size(400, -1))
        self.m_panel_right.SetMaxSize(wx.Size(400, -1))

        bSizer_right = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_job_no = wx.Panel(self.m_panel_right, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 40),
                                       wx.TAB_TRAVERSAL)
        self.m_panel_job_no.SetMinSize(wx.Size(-1, 40))
        self.m_panel_job_no.SetMaxSize(wx.Size(-1, 40))

        bSizer57 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_job_no = wx.StaticText(self.m_panel_job_no, wx.ID_ANY, u"  Job number", wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.m_staticText_job_no.Wrap(-1)

        bSizer57.Add(self.m_staticText_job_no, 0, wx.ALIGN_CENTER | wx.ALL, 3)

        self.m_textCtrl_job_no = wx.TextCtrl(self.m_panel_job_no, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.Size(200, -1), wx.TE_READONLY)
        self.m_textCtrl_job_no.SetMinSize(wx.Size(200, -1))
        self.m_textCtrl_job_no.SetMaxSize(wx.Size(200, -1))

        bSizer57.Add(self.m_textCtrl_job_no, 0, wx.ALIGN_CENTER | wx.ALL, 3)

        self.m_button_job = wx.Button(self.m_panel_job_no, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize,0)
        bSizer57.Add(self.m_button_job, 0, wx.ALL, 5)

        self.m_panel_job_no.SetSizer(bSizer57)
        self.m_panel_job_no.Layout()
        bSizer_right.Add(self.m_panel_job_no, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel_equip_info = wx.Panel(self.m_panel_right, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.TAB_TRAVERSAL)
        sbSizer11 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel_equip_info, wx.ID_ANY, u"Equipment Information"),
                                      wx.VERTICAL)

        self.m_panel65 = wx.Panel(sbSizer11.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TAB_TRAVERSAL)
        bSizer58 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText6 = wx.StaticText(self.m_panel65, wx.ID_ANY, u"Chamber 1", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText6.Wrap(-1)

        bSizer58.Add(self.m_staticText6, 0, wx.ALL, 1)

        self.m_panel68 = wx.Panel(self.m_panel65, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer59 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText7 = wx.StaticText(self.m_panel68, wx.ID_ANY, u"       Model", wx.DefaultPosition,
                                           wx.Size(100, -1), 0)
        self.m_staticText7.Wrap(-1)

        self.m_staticText7.SetMinSize(wx.Size(100, -1))
        self.m_staticText7.SetMaxSize(wx.Size(100, -1))

        bSizer59.Add(self.m_staticText7, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_textCtrl_model1 = wx.TextCtrl(self.m_panel68, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1),
                                             wx.Size(200, -1), wx.TE_READONLY)
        self.m_textCtrl_model1.SetMinSize(wx.Size(200, -1))
        self.m_textCtrl_model1.SetMaxSize(wx.Size(200, -1))

        bSizer59.Add(self.m_textCtrl_model1, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel68.SetSizer(bSizer59)
        self.m_panel68.Layout()
        bSizer59.Fit(self.m_panel68)
        bSizer58.Add(self.m_panel68, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel69 = wx.Panel(self.m_panel65, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer591 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText71 = wx.StaticText(self.m_panel69, wx.ID_ANY, u"       Serial  ", wx.DefaultPosition,
                                            wx.Size(100, -1), 0)
        self.m_staticText71.Wrap(-1)

        self.m_staticText71.SetMinSize(wx.Size(100, -1))
        self.m_staticText71.SetMaxSize(wx.Size(100, -1))

        bSizer591.Add(self.m_staticText71, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_textCtrl_serial1 = wx.TextCtrl(self.m_panel69, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.Size(200, -1), wx.TE_READONLY)
        self.m_textCtrl_serial1.SetMinSize(wx.Size(200, -1))
        self.m_textCtrl_serial1.SetMaxSize(wx.Size(200, -1))

        bSizer591.Add(self.m_textCtrl_serial1, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.m_panel69.SetSizer(bSizer591)
        self.m_panel69.Layout()
        bSizer591.Fit(self.m_panel69)
        bSizer58.Add(self.m_panel69, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel65.SetSizer(bSizer58)
        self.m_panel65.Layout()
        bSizer58.Fit(self.m_panel65)
        sbSizer11.Add(self.m_panel65, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel66 = wx.Panel(sbSizer11.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TAB_TRAVERSAL)
        bSizer581 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText61 = wx.StaticText(self.m_panel66, wx.ID_ANY, u"Chamber 2", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText61.Wrap(-1)

        bSizer581.Add(self.m_staticText61, 0, wx.ALL, 1)

        self.m_panel681 = wx.Panel(self.m_panel66, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer592 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText72 = wx.StaticText(self.m_panel681, wx.ID_ANY, u"       Model", wx.DefaultPosition,
                                            wx.Size(100, -1), 0)
        self.m_staticText72.Wrap(-1)

        self.m_staticText72.SetMinSize(wx.Size(100, -1))
        self.m_staticText72.SetMaxSize(wx.Size(100, -1))

        bSizer592.Add(self.m_staticText72, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_textCtrl_model2 = wx.TextCtrl(self.m_panel681, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.Size(200, -1), wx.TE_READONLY)
        self.m_textCtrl_model2.SetMinSize(wx.Size(200, -1))
        self.m_textCtrl_model2.SetMaxSize(wx.Size(200, -1))

        bSizer592.Add(self.m_textCtrl_model2, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel681.SetSizer(bSizer592)
        self.m_panel681.Layout()
        bSizer592.Fit(self.m_panel681)
        bSizer581.Add(self.m_panel681, 1, wx.EXPAND | wx.ALL, 2)

        self.m_panel691 = wx.Panel(self.m_panel66, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer5911 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText711 = wx.StaticText(self.m_panel691, wx.ID_ANY, u"       Serial  ", wx.DefaultPosition,
                                             wx.Size(100, -1), 0)
        self.m_staticText711.Wrap(-1)

        self.m_staticText711.SetMinSize(wx.Size(100, -1))
        self.m_staticText711.SetMaxSize(wx.Size(100, -1))

        bSizer5911.Add(self.m_staticText711, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_textCtrl_serial2 = wx.TextCtrl(self.m_panel691, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.Size(200, -1), wx.TE_READONLY)
        self.m_textCtrl_serial2.SetMinSize(wx.Size(200, -1))
        self.m_textCtrl_serial2.SetMaxSize(wx.Size(200, -1))

        bSizer5911.Add(self.m_textCtrl_serial2, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel691.SetSizer(bSizer5911)
        self.m_panel691.Layout()
        bSizer5911.Fit(self.m_panel691)
        bSizer581.Add(self.m_panel691, 1, wx.EXPAND | wx.ALL, 2)

        self.m_panel66.SetSizer(bSizer581)
        self.m_panel66.Layout()
        bSizer581.Fit(self.m_panel66)
        sbSizer11.Add(self.m_panel66, 1, wx.EXPAND | wx.ALL, 5)

        self.m_button_read = wx.Button(sbSizer11.GetStaticBox(), wx.ID_ANY, u"Read Information", wx.DefaultPosition,
                                       wx.Size(300, 25), 0)
        self.m_button_read.SetMinSize(wx.Size(300, 25))
        self.m_button_read.SetMaxSize(wx.Size(300, 25))

        sbSizer11.Add(self.m_button_read, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel_equip_info.SetSizer(sbSizer11)
        self.m_panel_equip_info.Layout()
        sbSizer11.Fit(self.m_panel_equip_info)
        bSizer_right.Add(self.m_panel_equip_info, 1, wx.EXPAND | wx.ALL, 10)

        self.m_panel_client_info = wx.Panel(self.m_panel_right, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 200),
                                            wx.TAB_TRAVERSAL)
        self.m_panel_client_info.SetMinSize(wx.Size(-1, 200))
        self.m_panel_client_info.SetMaxSize(wx.Size(-1, 200))

        sbSizer12 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel_client_info, wx.ID_ANY, u"Client Information"),
                                      wx.VERTICAL)

        self.m_panel74 = wx.Panel(sbSizer12.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 50),
                                  wx.TAB_TRAVERSAL)
        self.m_panel74.SetMinSize(wx.Size(-1, 50))
        self.m_panel74.SetMaxSize(wx.Size(-1, 50))

        bSizer71 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText21 = wx.StaticText(self.m_panel74, wx.ID_ANY, u"Client Name", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText21.Wrap(-1)

        bSizer71.Add(self.m_staticText21, 0, wx.ALL, 2)

        self.m_textCtrl_client_name = wx.TextCtrl(self.m_panel74, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                  wx.Size(350, -1), 0)
        self.m_textCtrl_client_name.SetMinSize(wx.Size(350, -1))
        self.m_textCtrl_client_name.SetMaxSize(wx.Size(350, -1))

        bSizer71.Add(self.m_textCtrl_client_name, 0, wx.ALL, 2)

        self.m_panel74.SetSizer(bSizer71)
        self.m_panel74.Layout()
        sbSizer12.Add(self.m_panel74, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel75 = wx.Panel(sbSizer12.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 100),
                                  wx.TAB_TRAVERSAL)
        self.m_panel75.SetMinSize(wx.Size(-1, 100))
        self.m_panel75.SetMaxSize(wx.Size(-1, 100))

        bSizer711 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText211 = wx.StaticText(self.m_panel75, wx.ID_ANY, u"Client Address", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.m_staticText211.Wrap(-1)

        bSizer711.Add(self.m_staticText211, 0, wx.ALL, 1)

        self.m_textCtrl_client_address1 = wx.TextCtrl(self.m_panel75, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                      wx.Size(350, -1), 0)
        self.m_textCtrl_client_address1.SetMinSize(wx.Size(350, -1))
        self.m_textCtrl_client_address1.SetMaxSize(wx.Size(350, -1))

        bSizer711.Add(self.m_textCtrl_client_address1, 0, wx.ALL, 2)

        self.m_textCtrl_client_address2 = wx.TextCtrl(self.m_panel75, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                      wx.Size(350, -1), 0)
        self.m_textCtrl_client_address2.SetMinSize(wx.Size(350, -1))
        self.m_textCtrl_client_address2.SetMaxSize(wx.Size(350, -1))

        bSizer711.Add(self.m_textCtrl_client_address2, 0, wx.ALL, 2)

        self.m_panel75.SetSizer(bSizer711)
        self.m_panel75.Layout()
        sbSizer12.Add(self.m_panel75, 1, wx.EXPAND | wx.ALL, 2)

        self.m_button_update = wx.Button(sbSizer12.GetStaticBox(), wx.ID_ANY, u"Update Information", wx.DefaultPosition,
                                         wx.Size(300, 25), 0)
        self.m_button_update.SetMinSize(wx.Size(300, 25))
        self.m_button_update.SetMaxSize(wx.Size(300, 25))

        sbSizer12.Add(self.m_button_update, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel_client_info.SetSizer(sbSizer12)
        self.m_panel_client_info.Layout()
        bSizer_right.Add(self.m_panel_client_info, 1, wx.EXPAND | wx.ALL, 10)

        self.m_panel_pdf_dcc = wx.Panel(self.m_panel_right, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1),
                                        wx.TAB_TRAVERSAL)
        bSizer81 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_upload = wx.Button(self.m_panel_pdf_dcc, wx.ID_ANY, u"Upload Data", wx.DefaultPosition,
                                         wx.Size(200, 30), 0)
        self.m_button_upload.SetMinSize(wx.Size(200, 30))
        self.m_button_upload.SetMaxSize(wx.Size(200, 30))

        bSizer81.Add(self.m_button_upload, 0, wx.ALIGN_CENTER | wx.ALL, 6)

        self.m_button_pdf = wx.Button(self.m_panel_pdf_dcc, wx.ID_ANY, u"Generate PDF", wx.DefaultPosition,
                                      wx.Size(200, 30), 0)
        self.m_button_pdf.SetMinSize(wx.Size(200, 30))
        self.m_button_pdf.SetMaxSize(wx.Size(200, 30))

        bSizer81.Add(self.m_button_pdf, 0, wx.ALIGN_CENTER | wx.ALL, 6)

        self.m_button_dcc = wx.Button(self.m_panel_pdf_dcc, wx.ID_ANY, u"Generate DCC", wx.DefaultPosition,
                                      wx.Size(200, 30), 0)
        self.m_button_dcc.SetMinSize(wx.Size(200, 30))
        self.m_button_dcc.SetMaxSize(wx.Size(200, 30))

        bSizer81.Add(self.m_button_dcc, 0, wx.ALIGN_CENTER | wx.ALL, 6)

        self.m_panel_pdf_dcc.SetSizer(bSizer81)
        self.m_panel_pdf_dcc.Layout()
        bSizer81.Fit(self.m_panel_pdf_dcc)
        bSizer_right.Add(self.m_panel_pdf_dcc, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_right.SetSizer(bSizer_right)
        self.m_panel_right.Layout()
        bSizer_main.Add(self.m_panel_right, 1, wx.EXPAND | wx.ALL, 1)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

    def compare(self, event):
        frame = GraphFrame()
        frame.Show()

    def confirm(self, event):
        selected_run_num = 0
        total_run_num = 0

        if self.m_filePicker_run11.GetPath() != '' and self.m_filePicker_run12.GetPath() != '':
            total_run_num += 1
            if self.m_checkBox_run1.GetValue():
                selected_run_num += 1
        if self.m_filePicker_run21.GetPath() != '' and self.m_filePicker_run22.GetPath() != '':
            total_run_num += 1
            if self.m_checkBox_run2.GetValue():
                selected_run_num += 1
        if self.m_filePicker_run31.GetPath() != '' and self.m_filePicker_run32.GetPath() != '':
            total_run_num += 1
            if self.m_checkBox_run3.GetValue():
                selected_run_num += 1
        if self.m_filePicker_run41.GetPath() != '' and self.m_filePicker_run42.GetPath() != '':
            total_run_num += 1
            if self.m_checkBox_run4.GetValue():
                selected_run_num += 1
        if self.m_filePicker_run51.GetPath() != '' and self.m_filePicker_run52.GetPath() != '':
            total_run_num += 1
            if self.m_checkBox_run5.GetValue():
                selected_run_num += 1

        self.m_textCtrl_selected_run.SetValue(str(selected_run_num))
        self.m_textCtrl_total_run.SetValue(str(total_run_num))


class LeftPanelGraph(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.axes.set_xlabel("NK mGy / nC")
        self.axes.set_ylabel("E_eff / keV ")

    def draw(self):
        x = np.arange(0,100)
        y = np.arange(100,200)
        self.axes.plot(x,y)

class RightPanelGrid(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent=parent)

        self.mygrid =grid.Grid(self)
        self.mygrid.CreateGrid(30,9)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.mygrid,1,wx.EXPAND)
        self.SetSizer(self.sizer)
        ### update real-time data
        self.mygrid.SetColLabelValue(0, "Beam")
        self.mygrid.SetColLabelValue(1, "E_eff")
        self.mygrid.SetColLabelValue(2, "Run1_NK")
        self.mygrid.SetColLabelValue(3, "Run2_NK")
        self.mygrid.SetColLabelValue(4, "Run3_NK")
        self.mygrid.SetColLabelValue(5, "Average")
        self.mygrid.SetColLabelValue(6, "Run1/Avg")
        self.mygrid.SetColLabelValue(7, "Run2/Avg")
        self.mygrid.SetColLabelValue(8, "Run3/Avg")
        ####

class GraphFrame(wx.Frame):
    def __init__(self):

        wx.Frame.__init__(self, parent = None, title=u"Graphs Demonstration", size=wx.Size(1450, 600))
        self.SetMinSize(wx.Size(1450, 600))
        self.SetMaxSize(wx.Size(1450, 600))

        spliter = wx.SplitterWindow(self)
        leftgraph = LeftPanelGraph(spliter)
        rightgrid = RightPanelGrid(spliter)
        spliter.SplitVertically(leftgraph,rightgrid)
        spliter.SetMinimumPaneSize(600)

        leftgraph.draw()



if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()