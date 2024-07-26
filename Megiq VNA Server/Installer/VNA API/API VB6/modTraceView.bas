Attribute VB_Name = "modTraceView"
Option Explicit

' modTraceView.bas:
' Show a TraceSet in a Treeview

Public Sub ViewTraceSet(Tvw As TreeView, TraceSet As mvnaTraceSet, Name As String)
  Dim N1 As Node
  Dim N2 As Node
  Dim N3 As Node
  Dim N4 As Node
  
  Dim Trace As mvnaTrace
  Dim Channel As mvnaTraceChannel
  Dim DataSet As mvnaTraceDataSet
  Dim Data As mvnaIQData
  Dim Par As mvnaParameter
  
  Tvw.Visible = False
  
  Call Tvw.Nodes.Clear
  
  Set N1 = Tvw.Nodes.Add(, , , "TraceSet " & Name)
  Call ViewTraceParameters(Tvw, N1, TraceSet.Parameters)
  
  For Each Trace In TraceSet.Traces
    Set N2 = Tvw.Nodes.Add(N1, tvwChild, , "Trace " & Format(Trace.TraceNumber))
    N2.Expanded = True
    
    Call ViewTraceParameters(Tvw, N2, Trace.Parameters)
    
    For Each Channel In Trace.Channels
      Set N3 = Tvw.Nodes.Add(N2, tvwChild, , "Channel " & Channel.Name)
      N3.Expanded = True
      
      For Each Data In Channel.DataSet
        Set N4 = Tvw.Nodes.Add(N3, tvwChild, , "Data " & Data.Name & ": " & Format(Data.Size) & " Points")
        N4.Expanded = True
      Next Data
    Next Channel
  Next Trace
  
  N1.Expanded = True
  Call N1.EnsureVisible
  
  Tvw.Visible = True
End Sub

Private Sub ViewTraceParameters(Tvw As TreeView, N As Node, Parameters As mvnaParameters)
  Dim N2 As Node
  Dim Par As mvnaParameter
  Dim i As Long
  Dim ValueList() As Double
  Dim S As String
  
  For Each Par In Parameters
    Set N2 = Tvw.Nodes.Add(N, tvwChild, , Par.Name & ": ")
    If (InStr(Par.Name, "FREQUENCY")) Then
      If (Par.IsSweep = True) Then
        If (Par.SweepType = mvnaSWT_List) Then
          ValueList = Par.SweepValueList
          S = ""
          For i = 0 To Par.Steps
            If (S <> "") Then S = S & " "
            S = S & Format(ValueList(i) / 1000000)
          Next i
          N2.Text = N2.Text & S & " M" & Par.Dimension
        Else
          N2.Text = N2.Text & Format(Par.StartValue / 1000000) & " > " & Format(Par.StopValue / 1000000) & " M" & Par.Dimension
        End If
      Else
        N2.Text = N2.Text & Format(Par.CurrentValue / 1000000) & " M" & Par.Dimension
      End If
    Else
      If (Par.IsSweep = True) Then
        If (Par.SweepType = mvnaSWT_List) Then
          ValueList = Par.SweepValueList
          S = ""
          For i = 0 To Par.Steps
            If (S <> "") Then S = S & " "
            S = S & Format(ValueList(i))
          Next i
          N2.Text = N2.Text & S & " " & Par.Dimension
        Else
          N2.Text = N2.Text & Format(Par.StartValue) & " > " & Format(Par.StopValue) & " " & Par.Dimension
        End If
      Else
        N2.Text = N2.Text & Format(Par.CurrentValue) & " " & Par.Dimension
      End If
    End If
  Next Par
End Sub
