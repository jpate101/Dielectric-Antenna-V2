Attribute VB_Name = "modPlot"
Option Explicit

Public Sub PlotData(Pic As PictureBox, Data() As Double, PData() As Double, ScaleMin As Double, ScaleMax As Double, Optional Caption As String)
  Dim i As Long
  Dim NrSamples As Long
  Dim X As Double
  Dim XLast As Double
  Dim XStep As Double
  Dim XScale As Double
  Dim Y As Double
  Dim YLast As Double
  Dim YStep As Double
  Dim YScale As Double
  
  On Error Resume Next
  NrSamples = UBound(PData) + 1
  If (NrSamples <= 1) Then Exit Sub   ' Need at least 2 samples to plot
  
  ' Put Gridlines
  Pic.ForeColor = RGB(&H80, &H80, &H80) ' Gray
  
  X = 0
  XStep = (Pic.ScaleWidth - 15) / 10
  For i = 0 To 10
    Pic.Line (X, 0)-(X, Pic.ScaleHeight)
    X = X + XStep
  Next i
  
  Y = 0
  YStep = (Pic.ScaleHeight - 15) / 5
  For i = 0 To 5
    Pic.Line (0, Y)-(Pic.ScaleWidth, Y)
    Y = Y + YStep
  Next i
  
  ' Put Scale
  Pic.ForeColor = vbWhite
  
  Pic.CurrentX = 0
  Pic.CurrentY = 0
  Pic.Print (Format(ScaleMax)) & " dB"
  
  Pic.CurrentX = 0
  Pic.CurrentY = Pic.ScaleHeight - Pic.TextHeight("A")
  Pic.Print (Format(ScaleMin)) & " dB"
  
  ' We assume that the X-axis contains frequency data
  ' This is only correct for frequency sweeps
  
  Pic.CurrentX = 0
  Pic.CurrentY = (Pic.ScaleHeight - Pic.TextHeight("A")) / 2
  Pic.Print (Format(PData(0) / 1000000) & " MHz")
  
  Pic.CurrentX = Pic.ScaleWidth - Pic.TextWidth(Format(PData(NrSamples - 1) / 1000000) & " MHz")
  Pic.CurrentY = (Pic.ScaleHeight - Pic.TextHeight("A")) / 2
  Pic.Print (Format(PData(NrSamples - 1) / 1000000) & " MHz")
  
  ' Put Caption
  If (Len(Caption) > 0) Then
    Pic.CurrentX = Pic.ScaleWidth - Pic.TextWidth(Caption)
    Pic.CurrentY = 0
    Pic.Print (Caption)
  End If
  
  ' Plot Data
  Pic.ForeColor = vbYellow
  
  X = 0
  XLast = X
  XScale = Pic.ScaleWidth / (PData(NrSamples - 1) - PData(0))
'  XStep = Pic.ScaleWidth / (NrSamples - 1)
  YScale = Pic.ScaleHeight / (ScaleMax - ScaleMin)
  YLast = Pic.ScaleHeight - (Data(0) - ScaleMin) * YScale
  
  For i = 0 To NrSamples - 1
    X = (PData(i) - PData(0)) * XScale
    Y = Pic.ScaleHeight - (Data(i) - ScaleMin) * YScale
    Pic.Line (XLast, YLast)-(X, Y)
    If (NrSamples <= 20) Then
      Pic.Circle (X, Y), 45
    End If
    XLast = X
    YLast = Y
    
'    X = X + XStep
  Next i
  
End Sub
