import wx
import wx.xrc

class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt = True)
        frame = MyFrame()
        frame.Show()

class MyFrame(wx.Frame):
    def __init__(self, title = 'App', pos = wx.DefaultPosition, size = wx.Size( 1200,864 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL):
        super().__init__(None, title = title)
        self.InitFrame()

    def InitFrame(self):

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer_main = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel_left = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(800, -1), wx.TAB_TRAVERSAL)
        self.m_panel_left.SetMinSize(wx.Size(800, -1))
        self.m_panel_left.SetMaxSize(wx.Size(800, -1))

        bSizer_left = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_show_run = wx.Panel(self.m_panel_left, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 70),
                                         wx.TAB_TRAVERSAL)
        self.m_panel_show_run.SetMinSize(wx.Size(-1, 70))
        self.m_panel_show_run.SetMaxSize(wx.Size(-1, 70))

        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel28 = wx.Panel(self.m_panel_show_run, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TAB_TRAVERSAL)
        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self.m_panel28, wx.ID_ANY, u"Total Runs", wx.Point(-1, -1), wx.DefaultSize,
                                           0)
        self.m_staticText1.Wrap(-1)
        bSizer15.Add(self.m_staticText1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.m_textCtrl1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel28.SetSizer(bSizer15)
        self.m_panel28.Layout()
        bSizer15.Fit(self.m_panel28)
        bSizer14.Add(self.m_panel28, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel281 = wx.Panel(self.m_panel_show_run, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText4 = wx.StaticText(self.m_panel281, wx.ID_ANY, u"Selected Runs", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        bSizer16.Add(self.m_staticText4, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self.m_panel281, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       0)
        bSizer16.Add(self.m_textCtrl2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel281.SetSizer(bSizer16)
        self.m_panel281.Layout()
        bSizer16.Fit(self.m_panel281)
        bSizer14.Add(self.m_panel281, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel282 = wx.Panel(self.m_panel_show_run, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer17 = wx.BoxSizer(wx.VERTICAL)

        self.m_button11 = wx.Button(self.m_panel282, wx.ID_ANY, u"Compare", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer17.Add(self.m_button11, 0, wx.ALIGN_CENTER | wx.ALL, 12)

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

        self.m_gauge1 = wx.Gauge(self.m_panel_pbar, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(500, -1),
                                 wx.GA_HORIZONTAL)
        self.m_gauge1.SetValue(30)
        bSizer18.Add(self.m_gauge1, 0, wx.ALL | wx.EXPAND, 5)

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

        self.m_textCtrl3 = wx.TextCtrl(self.m_panel39, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(530, -1),
                                       0)
        self.m_textCtrl3.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl3.SetMaxSize(wx.Size(530, -1))

        bSizer27.Add(self.m_textCtrl3, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button12 = wx.Button(self.m_panel39, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer27.Add(self.m_button12, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel39.SetSizer(bSizer27)
        self.m_panel39.Layout()
        bSizer27.Fit(self.m_panel39)
        bSizer24.Add(self.m_panel39, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel40 = wx.Panel(self.m_panel_run1_file, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                  wx.TAB_TRAVERSAL)
        bSizer271 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_textCtrl31 = wx.TextCtrl(self.m_panel40, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(530, -1),
                                        0)
        self.m_textCtrl31.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl31.SetMaxSize(wx.Size(530, -1))

        bSizer271.Add(self.m_textCtrl31, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button121 = wx.Button(self.m_panel40, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer271.Add(self.m_button121, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel40.SetSizer(bSizer271)
        self.m_panel40.Layout()
        bSizer271.Fit(self.m_panel40)
        bSizer24.Add(self.m_panel40, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_file.SetSizer(bSizer24)
        self.m_panel_run1_file.Layout()
        bSizer24.Fit(self.m_panel_run1_file)
        bSizer_run1_inside.Add(self.m_panel_run1_file, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel_run1_check = wx.Panel(sbSizer_run1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(70, -1),
                                           wx.TAB_TRAVERSAL)
        self.m_panel_run1_check.SetMinSize(wx.Size(70, -1))
        self.m_panel_run1_check.SetMaxSize(wx.Size(70, -1))

        bSizer_run1_check = wx.BoxSizer(wx.HORIZONTAL)

        self.m_checkBox_run1 = wx.CheckBox(self.m_panel_run1_check, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(-1, -1), 0)
        self.m_checkBox_run1.SetValue(True)
        bSizer_run1_check.Add(self.m_checkBox_run1, 0, wx.ALL, 25)

        self.m_panel_run1_check.SetSizer(bSizer_run1_check)
        self.m_panel_run1_check.Layout()
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

        self.m_textCtrl32 = wx.TextCtrl(self.m_panel391, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.Size(530, -1), 0)
        self.m_textCtrl32.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl32.SetMaxSize(wx.Size(530, -1))

        bSizer272.Add(self.m_textCtrl32, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button122 = wx.Button(self.m_panel391, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer272.Add(self.m_button122, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel391.SetSizer(bSizer272)
        self.m_panel391.Layout()
        bSizer272.Fit(self.m_panel391)
        bSizer241.Add(self.m_panel391, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel401 = wx.Panel(self.m_panel_run1_file1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer2711 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_textCtrl311 = wx.TextCtrl(self.m_panel401, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.Size(530, -1), 0)
        self.m_textCtrl311.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl311.SetMaxSize(wx.Size(530, -1))

        bSizer2711.Add(self.m_textCtrl311, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button1211 = wx.Button(self.m_panel401, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2711.Add(self.m_button1211, 0, wx.ALIGN_CENTER | wx.ALL, 1)

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

        self.m_checkBox_run11 = wx.CheckBox(self.m_panel_run1_check1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.Size(-1, -1), 0)
        self.m_checkBox_run11.SetValue(True)
        bSizer_run1_check1.Add(self.m_checkBox_run11, 0, wx.ALL, 25)

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

        self.m_textCtrl33 = wx.TextCtrl(self.m_panel392, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.Size(530, -1), 0)
        self.m_textCtrl33.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl33.SetMaxSize(wx.Size(530, -1))

        bSizer273.Add(self.m_textCtrl33, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button123 = wx.Button(self.m_panel392, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer273.Add(self.m_button123, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel392.SetSizer(bSizer273)
        self.m_panel392.Layout()
        bSizer273.Fit(self.m_panel392)
        bSizer242.Add(self.m_panel392, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel402 = wx.Panel(self.m_panel_run1_file2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer2712 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_textCtrl312 = wx.TextCtrl(self.m_panel402, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.Size(530, -1), 0)
        self.m_textCtrl312.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl312.SetMaxSize(wx.Size(530, -1))

        bSizer2712.Add(self.m_textCtrl312, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button1212 = wx.Button(self.m_panel402, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2712.Add(self.m_button1212, 0, wx.ALIGN_CENTER | wx.ALL, 1)

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

        self.m_checkBox_run12 = wx.CheckBox(self.m_panel_run1_check2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.Size(-1, -1), 0)
        self.m_checkBox_run12.SetValue(True)
        bSizer_run1_check2.Add(self.m_checkBox_run12, 0, wx.ALL, 25)

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

        self.m_textCtrl34 = wx.TextCtrl(self.m_panel393, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.Size(530, -1), 0)
        self.m_textCtrl34.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl34.SetMaxSize(wx.Size(530, -1))

        bSizer274.Add(self.m_textCtrl34, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button124 = wx.Button(self.m_panel393, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer274.Add(self.m_button124, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel393.SetSizer(bSizer274)
        self.m_panel393.Layout()
        bSizer274.Fit(self.m_panel393)
        bSizer243.Add(self.m_panel393, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel403 = wx.Panel(self.m_panel_run1_file3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer2713 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_textCtrl313 = wx.TextCtrl(self.m_panel403, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.Size(530, -1), 0)
        self.m_textCtrl313.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl313.SetMaxSize(wx.Size(530, -1))

        bSizer2713.Add(self.m_textCtrl313, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button1213 = wx.Button(self.m_panel403, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2713.Add(self.m_button1213, 0, wx.ALIGN_CENTER | wx.ALL, 1)

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

        self.m_checkBox_run13 = wx.CheckBox(self.m_panel_run1_check3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.Size(-1, -1), 0)
        self.m_checkBox_run13.SetValue(True)
        bSizer_run1_check3.Add(self.m_checkBox_run13, 0, wx.ALL, 25)

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

        self.m_textCtrl35 = wx.TextCtrl(self.m_panel394, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.Size(530, -1), 0)
        self.m_textCtrl35.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl35.SetMaxSize(wx.Size(530, -1))

        bSizer275.Add(self.m_textCtrl35, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button125 = wx.Button(self.m_panel394, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer275.Add(self.m_button125, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_panel394.SetSizer(bSizer275)
        self.m_panel394.Layout()
        bSizer275.Fit(self.m_panel394)
        bSizer244.Add(self.m_panel394, 1, wx.EXPAND | wx.ALL, 1)

        self.m_panel404 = wx.Panel(self.m_panel_run1_file4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        bSizer2714 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_textCtrl314 = wx.TextCtrl(self.m_panel404, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.Size(530, -1), 0)
        self.m_textCtrl314.SetMinSize(wx.Size(530, -1))
        self.m_textCtrl314.SetMaxSize(wx.Size(530, -1))

        bSizer2714.Add(self.m_textCtrl314, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button1214 = wx.Button(self.m_panel404, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2714.Add(self.m_button1214, 0, wx.ALIGN_CENTER | wx.ALL, 1)

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

        self.m_checkBox_run14 = wx.CheckBox(self.m_panel_run1_check4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.Size(-1, -1), 0)
        self.m_checkBox_run14.SetValue(True)
        bSizer_run1_check4.Add(self.m_checkBox_run14, 0, wx.ALL, 25)

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
        #######################################################################################
        self.m_panel_right = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(400, -1), wx.TAB_TRAVERSAL)
        self.m_panel_right.SetMinSize(wx.Size(400, -1))
        self.m_panel_right.SetMaxSize(wx.Size(400, -1))

        right_sizer = wx.GridBagSizer(5, 5)

        txt_job_number = wx.StaticText(self.m_panel_right, label="Job number")
        right_sizer.Add(txt_job_number, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=15)
        self.ipt_job_number = wx.TextCtrl(self.m_panel_right)
        right_sizer.Add(self.ipt_job_number, pos=(0, 2),span=(0, 5), flag=wx.TOP | wx.CENTER | wx.BOTTOM, border=15)

        ###Equipment Info form
        EIbox = wx.StaticBox(self.m_panel_right, label="Equipment Info")
        EIboxsizer = wx.StaticBoxSizer(EIbox, wx.VERTICAL)
        font = wx.Font(11, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        txt_chamber1 = wx.StaticText(self.m_panel_right, label="Chamber1")
        txt_chamber1.SetFont(font)
        EIboxsizer.Add(txt_chamber1, flag=wx.ALL, border=5)

        Chamber1SizerModel = wx.BoxSizer()
        Chamber1SizerSerial = wx.BoxSizer()
        txt_model1 = wx.StaticText(self.m_panel_right, label="model")
        txt_serial1 = wx.StaticText(self.m_panel_right, label="serial")
        self.ipt_model1 = wx.TextCtrl(self.m_panel_right)
        self.ipt_serial1 = wx.TextCtrl(self.m_panel_right)
        Chamber1SizerModel.Add(txt_model1, flag=wx.ALL| wx.CENTER, border=5)
        Chamber1SizerModel.Add(self.ipt_model1, flag=wx.ALL | wx.EXPAND, border=5)
        Chamber1SizerSerial.Add(txt_serial1, flag=wx.ALL, border=5)
        Chamber1SizerSerial.Add(self.ipt_serial1, flag=wx.ALL | wx.EXPAND, border=5)
        EIboxsizer.Add(Chamber1SizerModel, 0, wx.LEFT, 5)
        EIboxsizer.Add(Chamber1SizerSerial, 0, wx.LEFT, 5)

        txt_chamber2 = wx.StaticText(self.m_panel_right, label="Chamber2")
        txt_chamber2.SetFont(font)
        EIboxsizer.Add(txt_chamber2, flag=wx.LEFT | wx.TOP, border=5)

        Chamber2SizerModel = wx.BoxSizer()
        Chamber2SizerSerial = wx.BoxSizer()
        txt_model2 = wx.StaticText(self.m_panel_right, label="model")
        txt_serial2 = wx.StaticText(self.m_panel_right, label="serial")
        self.ipt_model2 = wx.TextCtrl(self.m_panel_right)
        self.ipt_serial2 = wx.TextCtrl(self.m_panel_right)
        Chamber2SizerModel.Add(txt_model2, flag=wx.ALL, border=5)
        Chamber2SizerModel.Add(self.ipt_model2, flag=wx.ALL | wx.EXPAND, border=5)
        Chamber2SizerSerial.Add(txt_serial2, flag=wx.ALL, border=5)
        Chamber2SizerSerial.Add(self.ipt_serial2, flag=wx.ALL | wx.EXPAND, border=5)
        EIboxsizer.Add(Chamber2SizerModel, 0, wx.LEFT, 5)
        EIboxsizer.Add(Chamber2SizerSerial, 0, wx.LEFT, 5)

        right_sizer.Add(EIboxsizer, pos=(1, 0), span=(1, 5), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=15)

        ### Client Info form
        CIbox = wx.StaticBox(self.m_panel_right, label="Client Info")
        CIboxsizer = wx.StaticBoxSizer(CIbox, wx.VERTICAL)

        txt_name = wx.StaticText(self.m_panel_right, label="client name")
        txt_name.SetFont(font)
        CIboxsizer.Add(txt_name, flag=wx.LEFT | wx.TOP, border=5)
        clientNameSizer = wx.BoxSizer()
        self.cname = wx.TextCtrl(self.m_panel_right)
        btn_update_1 = wx.Button(self.m_panel_right, wx.ID_ANY, label='update')
        clientNameSizer.Add(self.cname, proportion=0, flag=wx.ALL, border=5)
        clientNameSizer.Add(btn_update_1, proportion=0, flag=wx.ALL, border=5)
        CIboxsizer.Add(clientNameSizer, flag=wx.ALL | wx.TOP, border=5)

        txt_Addre = wx.StaticText(self.m_panel_right, label="client address")
        txt_Addre.SetFont(font)
        CIboxsizer.Add(txt_Addre, flag=wx.LEFT | wx.TOP, border=5)
        clientAddreSizer = wx.BoxSizer()
        self.cAddre = wx.TextCtrl(self.m_panel_right)
        btn_update_2 = wx.Button(self.m_panel_right, wx.ID_ANY, label='update')
        clientAddreSizer.Add(self.cAddre, proportion=0, flag=wx.ALL, border=5)
        clientAddreSizer.Add(btn_update_2, proportion=0, flag=wx.ALL, border=5)
        CIboxsizer.Add(clientAddreSizer, flag=wx.ALL | wx.TOP, border=5)

        right_sizer.Add(CIboxsizer, pos=(2, 0), span=(1, 5), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=15)

        ### button for pdf dcc
        btn_pdf = wx.Button(self.m_panel_right, wx.CENTER, label='Generate PDF')
        btn_dcc = wx.Button(self.m_panel_right, wx.ALL, label='Generate DCC')

        right_sizer.Add(btn_pdf, pos=(4, 0), flag=wx.ALL, border=15)
        right_sizer.Add(btn_dcc, pos=(5, 0), flag=wx.ALL, border=15)

        self.m_panel_right.SetSizer(right_sizer)
        right_sizer.Fit(self.m_panel_right)

        bSizer_main.Add(self.m_panel_right, 1, wx.EXPAND | wx.ALL, 1)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()