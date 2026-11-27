---
title: "OOPC 2. Classes"
lang: en
date: 2025-09-27
tags: ["Docs","OOPC"]
math: mathjax
showWordCount: true
---
# OOPC2.Classes
> Last Edit: 9/28/25
> 

# 2.1 Structs and Classes

- Struct，通过一个大的模块，将众多 Data Types 储存到其中

```cpp
struct Student {
    string name;
    int ID;
};
```

- `struct`（结构体）：用于将多个不同类型的数据组合在一起
- `Student` 是结构体的名称（结构体名）
- `string name`（字符串类型的 name）：表示学生的名字
- `int ID`（整数类型的 ID）：表示学生的编号

> 这里只是**定义结构体，不会分配内存**
> 

## Create an instance

```cpp
struct Student x, y;
x.name = "Kenya";
x.ID = 8012;
y.name = "Cindy";
y.ID = 2023;
```

- 这里创建了两个 instance：`x` 和 `y`
- 用 `.` 操作符访问成员变量（dot operator）：
    - `x.name` 表示 x 的 name 字段
    - `x.ID` 表示 x 的 ID 字段
- 每个结构体实例都单独存储属于自己的数据

## Print struct data

- 赋值之后通过 `cout << "X, Name: " << x.name << endl << "ID: " << x.ID << endl;` 就可以得到以下输出

```
Name: Kenya
ID: 8012
```

## 2.1.1 What is a Class

- Class，是 Struct 的拓展版本，其可以把 Data Member 和 Functions 一起组成一个单元

## **2.1.2 Defining a class**

```cpp
class Student {
    string name;
    int ID;
    void print();
};
```

- 使用关键字 `class` 定义类，类名为 `Student`
- 有两个 data member：`name` 和 `ID`，还有一个成员函数 `print()`
- 类定义一般写在头文件里，比如 `Student.h`

> 函数 `print()` 这里只 declaration），还没有 implementation
> 

## **2.1.3 Access Control**

- 类成员默认是 `private` 的，意味着 `name`、`ID` 和 `print` 函数不能在类外访问，所以不能直接写 `x.name` 来访问类成员
- 简单来说，一个 Class 存在两种 Specifiers

| 访问权限 | 含义 |
| --- | --- |
| `private`（私有） | 只能在类的内部访问 |
| `public`（公开） | 可以在类的外部访问 |
- 于是如果想要 `print` 能被访问到，就可以通过

```cpp
class Student {
private:
    string name;
    int ID;
public:
    void print();
};
```

- 把 `name` 和 `ID` 放在 `private:` 后面，表示它们是私有的
- 把 `print()` 函数放在 `public:` 后面，表示它可以在类外访

## **2.1.4 Implementing functions in a class**

```cpp
void Student::print() {
    cout << "Name: " << name << endl << "ID: " << ID << endl;
}
```

- `Student::print()` 表示这是 `Student` 类的 `print` 方法（使用作用域解析符 `::`）
- 实现在 `.cpp` 文件中，有助于代码组织（编译更快、调试更方便）

## **2.1.5 Creating instances of a class**

```cpp
Student x;
x.name = "Cindy"; // ❌ 错误：name 是 private 成员
x.print();
```

- 类的成员默认是 `private`，不能直接在类外访问 `x.name`
- 虽然 `x.print()` 可以调用（因为 `print` 是 public），但输出是未初始化的内容

> 虽然是 `private` ，但 `x` 中的 `name` 和 `ID` 会占据内存，但没赋初值，会是垃圾值（`?`）
> 
- 想要访问 `Private` 的值当然也有办法， Solution 1：把 `name` 和 `ID` 改为 public，这个并不推荐，破坏封装性
- 于是就可以使用 Solution 2：使用 `setter` 和 `getter` 函数，更推荐，用函数来修改和访问私有数据

## **2.1.6 Getter and Setter Functions**

- 通过为 `name` 成员添加访问接口的方式实现，首先在 `Student.h` 中声明

```cpp
#include <string>
using namespace std;

class Student {
 private:
  string name;
  int ID;

 public:
  void print();
  void setName(string name);
  string getName();
};
```

- 然后`Student.cpp` 中定义

```cpp
#include <iostream>
#include "Student.h"
using namespace std;

void Student::print() {
  cout << "Name: " << name << endl << "ID: " << ID << endl;
}

void Student::setName(string n) {
  name = n;
}

string Student::getName() {
  return name;
}
```

- 最后 main 中有

```cpp
Student x;
x.setName("Cindy");
cout << x.getName() << endl;
x.print();  // ID 仍然未初始化
```

- 输出即为

```
Cindy
Name: Cindy
ID: -86764（未定义的随机值
```

> 这里 ID 就单纯一个 Class 中的 data
> 

- `getName()` 返回的是 **值（value）**，不是引用
- 所以不能写：`x.getName() = "Bob";`，因为无法对返回值赋值

# 2.2 Constructors

- Constructors 是一种特殊的函数，它在创建 Class 的 Object 时自动被调用，用来初始化这个对象的成员

## 2.2.1 Default Constructor

- 同样使用一个完整的代码

```cpp
// Student.h
#include <string>
using namespace std;

class Student {
 private:
  string name;
  int ID;

 public:
  void print();
  void setName(string name);
  string getName();
};
```

```cpp
// Student.cpp
#include <iostream>
#include "Student.h"
using namespace std;

void Student::print() {
  cout << "Name: " << name << endl << "ID: " << ID << endl;
}

void Student::setName(string n) {
  name = n;
}

string Student::getName() {
  return name;
}
```

```cpp
// main.cpp
#include <iostream>
#include "Student.h"
using namespace std;

int main(void) {
  Student x;

  x.setName("Cindy");
  cout << x.getName() << endl;

  x.print(); // ID is not initialized
  return 0;
}
```

- 在打印时会有输出

```cpp
Name: Cindy
ID: 32767  // or -12345, or any random garbage value
```

- 这是因为 So far 只赋值了了 `name`，没设置 `ID`
- 想要这个 `ID` 有值，也可以通过一个 `x.setID(12345);` 来赋值，但有比这个更加好的解决方案
- 回到 `Student.h` 文件中

```cpp
class Student {
private:
    string name;
    int ID;
public:
    Student();  // Constructor
    void print();
    void setName(string name);
    string getName();
};
```

- 然后在 `Student.cpp` 中定义它：

```cpp
Student::Student() {
  ID = 0;
  name = "no name";
}
```

- 这段代码的意思是：每次创建 Student 对象时，自动把 `name` 设为 `"no name"`，`ID` 设为 `0`
- 这样的话，到了 `main` 函数中，通过 `Student x;`  和 `x.print();` 就可以得到

```
Name: no name
ID: 0
```

## 2.2.2 Other Constructors

- Default 的 Constructors 没有参数，所有值都必须写死（hardcoded）
- 但有时候我们想在创建对象时就设置好名字和 ID —— 这时就需要 **Parameterized constructors**
- 回到 `student.h` ，在 Constructors 中添加参数

```cpp
Student(int id);              // 第一个构造函数，只传 id
Student(int id, string n);    // 第二个构造函数，同时传 id 和 name
```

- 对应的 CPP 就是

```cpp
Student::Student(int id) {
    ID = id;
    name = "no name";
}

Student::Student(int id, string n) {
    ID = id;
    name = n;
}

```

- 如果只传一个 `int`，就只设置 ID，名字是 "no name"
- 如果传一个 `int` 和一个 `string`，两个都设置

```cpp
Student x;                   // Default constructor is called
Student y(20207);            // 1st constructor is called
Student z(20207, "Osiris");  // 2nd constructor is called
```

- 这样就会得到输出

```
Student x:
Name: no name
ID: 0

Student y:
Name: no name
ID: 20207

Student z:
Name: Osiris
ID: 20207
```

- 每种 Construct 都起了对应的初始化作用

## **2.2.3. How is it possible to have multiple constructors with the same name but different numbers of parameters?**

- 类似于 Function，只要 Parameter 个数，或者 Type 不一样，就可以定义多个版本
- 如果**一个构造函数都没写**，编译器会自动生成一个默认构造函数（`Student::Student()`）

> 默认的 Constructor 什么都干不了
> 
- 但**只要手动写了任何构造函数**，编译器就**不会**帮自动生成默认构造函数了
- 所以如果用 `Student x;` 这样无参数的方式创建对象，必须写上 `Student();` 默认构造函数

# 2.3 Lifecycle of an Object

- 有 Construct 的同时也存在 Destructor，用来在对象被销毁、释放内存时自动调用
- 在离开 Scope，Implicitly Deleted 的时候自动调用，定义为 `~`  加 Class

```cpp
class Student {
public:
    Student();        // Constructor
    ~Student();       // Destructor
};

//可以通过两个对 Constructor 和 Destructor 的定义来可视化 Lifecycle

Student::Student(){
	cont << "Constructor called" << endl;
}

Studeng::~Student(){
	cont << "Destructor called" << endl;
}
```

- 然后跑一个含有 Scope 的 main 就可以得到

```cpp
int main(void) {
    Student x;  // Define x, Constructor Called
    cout << "Inside main" << endl;

    if(true) {
        Student y;  // Define y, another Constructor called
        cout << "Inside if" << endl;
    }  // Leaving y's scope, Destructor called
    cout << "Outside if" << endl;
    return 0;  // Whole game end, Destructor called
}
```

- 跑完这个 main，预期会得到输出

```
Constructor called
Inside main
Constructor called
Inside if
Destructor called
Outside if
Destructor called
```