@echo off
set cho=0
%1 set /p cho=是否先卸载旧包？输入 1 卸载，留白或输入其它不卸载:
if %cho% equ 1 (echo 卸载旧包...
title 卸载旧包...
echo y | python -m pip uninstall pyinstaller
echo y | python -m pip uninstall requests 
echo y | python -m pip uninstall schedule 
echo y | python -m pip uninstall chardet 
echo y | python -m pip uninstall black )
echo 正在安装依赖模块...
title 正在安装依赖模块...
set URL=https://pypi.mirrors.ustc.edu.cn/simple/
python -m pip install pip --upgrade -i %URL%
python -m pip install pyinstaller -i %URL%
python -m pip install requests -i %URL%
python -m pip install black -i %URL%
python -m pip install schedule -i %URL%
python -m pip install chardet -i %URL%

echo y | python -m pip uninstall pathlib

echo 正在更新依赖模块...
title 正在更新依赖模块...
python -m pip install pip --upgrade -i %URL%
python -m pip install pyinstaller --upgrade -i %URL%
python -m pip install requests --upgrade -i %URL%
python -m pip install black --upgrade -i %URL%
python -m pip install schedule --upgrade -i %URL%
python -m pip install chardet --upgrade -i %URL%
%1 start mshta vbscript:Msgbox("依赖模块更新完毕",4096)(window.close)
exit