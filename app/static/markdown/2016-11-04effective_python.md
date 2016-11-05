---
title: effective python 
subtitle: 一点小技巧
tags: 新建,模板,小书匠
meta: 2016-10-29
---


# 了解bytes、str与unicode的区别

**三者之间的关系：**
+ 字符串是独立于编码的抽象,是使用特定编码后的字节串
+ 字节经过编码之后就是字符串
+ unicode是一种具体编码方式

**举个例子：**
```python
    s = u"一个例子"
    b = u"一个例子".encode("UTF8")  #使用UTF对字符串进行编码
    print(type(s))
    print(type(b))
    print(s)
    print(b)        
```
上面代码输出如下:
```
<class 'str'>
<class 'bytes'>
一个例子
b'\xe4\xb8\x80\xe4\xb8\xaa\xe4\xbe\x8b\xe5\xad\x90'
```

**python2中的情况**：
在python2里面实际上同时存在str和unicode两种对象，其中str表示编码后的字符串，而unicode则表示未编码的unicode字符串。str可以通过`#-*- coding: UTFx -*-`声明默认的编码。下面看一个例子:
```python
#-*- coding: UTF8 -*-

if __name__ == "__main__":
    # unicode字符串
    u = unicode(u"一个例子")
    # 默认使用UTF8进行编码
    s = str("一个例子")
    # 使用UTF8对unicode字符串进行编码
    utf = u.encode("UTF8")
    print(type(s))
    print(type(u))
    print(type(utf))
    print(s)
    print(u)
    print(utf)
    print(s.__sizeof__())
    print(u.__sizeof__())
    print(utf.__sizeof__())
```		
上面例子输出：
```
<type 'str'>
<type 'unicode'>
<type 'str'>
一个例子
一个例子
一个例子
49
68
49
```

