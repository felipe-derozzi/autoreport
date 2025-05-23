@echo off
echo Compilando o executavel do Relatorio de Expedicao...
echo.

pyinstaller --clean gui_relatorio.spec

echo.
if %ERRORLEVEL% EQU 0 (
    echo Compilacao concluida com sucesso! O executavel esta na pasta 'dist'.
    echo Pressione qualquer tecla para fechar.
) else (
    echo Compilacao falhou! Verifique os erros acima.
    echo Pressione qualquer tecla para fechar.
)

pause > nul 