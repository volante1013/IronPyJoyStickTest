# IronPyJoyStickTest
IronPythonでJoyStickの入力を検知するための検証プロジェクト  
winmm.dll内にあるjoyGetNumDevs(), joyGetDevCaps(), joyGetPosEx()のAPIを使用すればJoyStickの入力が検知できる。

## 方法1(未実現)
ctypesモジュールを使用して、winmm.dllから上記APIを呼ぶ方法。  
通常のPython3系や2系では動作することは確認したが、
IronPythonでは動作しなかった。  
ctypesモジュールを使って生成する配列の型がIronPythonの型で生成されてしまうのが問題っぽいが、  
それが正しいのかも不明で、回避策も不明のまま。

ファイル：IronPyJoyStickTest1.py

## 方法2(実現)
上記のAPIを利用したC#コードを文字列で記述して、それを動的コンパイルすることでIronPython側で検知した結果だけ得る方法。
joyGetPosEx()を呼んでPython側で結果を処理しようとするとなぜか入力が検知されなかったので、  
C#側で入力の検知まで行ってPython側ではその結果だけを受け取る方式にすれば正常に動作した。

ファイル：IronPyJoyStickTest2.py, generate.py  
参考サイト：  
http://www.voidspace.org.uk/ironpython/dynamically_compiling.shtml  
https://gist.github.com/mfakane/1176549
