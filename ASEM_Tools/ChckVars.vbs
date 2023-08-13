Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")
Set xmlDOM = CreateObject("MSXML2.DOMDocument.6.0")

' Obtener variables definidas
Dim VarDefinidas
Set VarDefinidas = CreateObject("Scripting.Dictionary")

' Obtener archivo de variables
extension = ".hmirealtimedb"
Set archivos = objFSO.GetFolder(".").Files

For Each archivo In archivos
    If LCase(objFSO.GetExtensionName(archivo.Name)) = LCase(Mid(extension, 2)) Then
        RutaArchivoVar = archivo.Path
        Exit For
    End If
Next

' Definir la propiedad que queremos buscar
NombreProp = "Variable"

' Analizar el archivo XML y encontrar todas las propiedades
xmlDOM.async = False
xmlDOM.load RutaArchivoVar

If xmlDOM.parseError.errorCode = 0 Then
    Set root = xmlDOM.documentElement
    For Each variable In root.getElementsByTagName(NombreProp)
        VarDefinidas(variable.selectSingleNode("Name").Text) = True
    Next
End If

' Obtener lista de archivos .hmiscr
output = objShell.Exec("cmd /c dir *.hmiscr /b /s /A-D ").StdOut.ReadAll
Pdls = Split(output, vbCrLf)

For Each Pdl In Pdls
    On Error Resume Next
    
    Set file = objFSO.OpenTextFile(Pdl, 1, False, -1)
    If Err = 0 Then
        XML_Pdl = file.ReadAll
        file.Close
        
        Set re = New RegExp
        re.Global = True
        re.Pattern = ".*?Var.*?=""(.*?)"""
        
        Set VarFoundRaw = re.Execute(XML_Pdl)
        
        For Each match In VarFoundRaw
            Variable = match.SubMatches(0)
            On Error Resume Next
            IsNumericVariable = IsNumeric(Variable)
            On Error Goto 0
            
            If Not IsNumericVariable Then
                Variable = Replace(Variable, " ", "")
                If Len(Variable) > 1 And Not VarDefinidas.Exists(Variable) Then
                    XML_Pdl = Replace(XML_Pdl, Variable, "ToDo")
                End If
            End If
        Next
        
        Set file = objFSO.OpenTextFile(Pdl, 2, True, -1)
        file.Write XML_Pdl
        file.Close
    End If
    
    On Error Goto 0
Next