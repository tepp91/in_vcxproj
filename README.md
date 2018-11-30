in_vcxproj.py
==============

in_vcxproj.pyはvcxprojファイル(Visual StudioのC++プロジェクトファイル)に定義されているファイルを取得するコマンドです。

使い方
-------

### ファイルを出力します

```
python in_vcxproj.py Foo.vcxproj
```

### 存在しないファイルを出力します

```
python in_vcxproj.py -ne Foo.vcxproj
```

### 指定ディレクトリ内にあるC++ファイルのうち、定義されていないファイルを出力します

```
python in_vcxproj.py -dir Foo/Source Foo.vcxproj
```
