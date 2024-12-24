; Пример скрипта с отпусканием клавиш
Send, {LWin}
Sleep, 500 ; Задержка 100 мс

Send, {Tab}
Sleep, 100 ; Задержка 100 мс

Loop, 5
{
    Send, {PgDn}
    Sleep, 100 ; Задержка 100 мс между нажатиями
}


Send, {Enter}
Sleep, 1000 ; Задержка 100 мс
Send, {Enter}
