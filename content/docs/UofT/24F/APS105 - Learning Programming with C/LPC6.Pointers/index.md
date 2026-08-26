---
title: "LPC 6. Pointers"
date: 2025-02-20
tags: ["Docs","LPC"]
math: mathjax
showWordCount: true
---
> Last Edit: 2/20/25

上一章中提到的所有有关于 Function 的内容都是关于一个函数的输入以及输出的，本章将讨论如何在不同函数间访问 Variables

# 6.1 Why Pointers ?

- 前面提到的所有有关 Function 的操作的返回值 `return` 都是唯一的，这是一个需要解决的问题

## 6.1.1 Communicate using return

``` c
bool isPerfectSquare(int x) {
  if ((int)sqrt(x) != sqrt(x)) {
    return false;
  } else {
    return true;
  }
}
```

- 以上是一段代码中的其中一个 Function，其存在了两个函数的输出，这使得 Function 可以提供多种不同的输出
- 但是这也成为了一个问题，就是当存在多个判断值 `if` 的时候，可能会导致错误，为了避免这个问题，可以通过将 `return` 的触发条件简化，如

``` c
bool isPerfectSquare(int x) {
    return ((int)sqrt(x) == sqrt(x));
}
```

- 确保了函数存在且只存在一个 `return` ，其具体的值将由具体Bool Value决定

### Calling by Value

- 在一个参数进入Function的时候，实际上传入的是其副本而不是变量本身，这代表了函数中对于变量进行的任何操作实际上不会改变外部定义的Variable本身

``` c
#include <stdio.h>
void simple(int);
int main(void) {
  int p = 12;
  simple(p);
  printf("The value of p is %d.\n", p);
  return 0;
}
void simple(int p) { 
  p = p / 2; 
}
-> The value of p is 12.
```

- 想要更改就需要首先从函数里 `return` ，其次再把值传给p，具体代码如下

``` c
#include <stdio.h>
int simple(int);
int main(void) {
  int p = 12;
  p = simple(p); //传入数值
  printf("The value of p is %d.\n", p);
  return 0;
}
int simple(int p) { 
  p = p / 2; 
  return p; //函数主动返回数值
}
```

## 6.1.2. Limitation of return

- 前面提到了 `return` 采取的本质是 Call by Value 按值传递的机制，具体来说，在调用函数的时候参数会接收变量的副本，这使得函数内部进行的更改不会影响外部

``` c
#include <stdio.h>
void swap(int, int);
int main(void) {
  int a = 9, b = 13;
  printf("Before swapping\nValue of a: %d\nValue 
of b: %d\n", a, b);
  swap(a, b);
  printf("After swapping\nValue of a: %d\nValue 
of b: %d\n", a, b);
  return 0;
}
void swap(int x, int y) {
  int temp = x;
  x = y;
  y = temp;
}
```

# 6.2 What are Pointers ?

Pointers 指针是存储变量地址的变量

- 现在有以下代码

``` c
#include <stdio.h>
int main(void) {
    int x = 7;   // x 是一个 int 变量
    int *p;      // p 是一个指向 int 的指针变量
    return 0;
}
```
 
- 可以说Declear p的过程就是为一个 `int` 变量预留了内存空间
- 前面提到过了 declaring a variable without initializing it 使得其变成一个 Garbage Value
- 这边 Declar 的一个 Piont 就是专门用来指向 Memory 的，但目前还没有指向具体目标

``` c
#include <stdio.h>
int main(void) {
    int x = 7;      // 声明一个整型变量 x 并初始化为 7
    int *p;         // 声明一个整型指针 p
    p = &x;         // 将 x 的地址赋给指针 p
    int y;          // 声明一个整型变量 y
    y = *p;         // 将指针 p 指向的地址（x 的地址）中的值赋给 y
    return 0;       // 函数返回 0
}
```

- 在上面的代码基础上，令 p 指向了 x的地址，之后再把 x的值赋给了 y
> 需要注意的是赋值之后 x 的值的改变将不再影响到 y

``` c
#include <stdio.h>
int main(void) {
  int x = 7;
  int *p;
  p = &x;
  int y;
  y = *p;
  printf("Address of x: %p\n Value of x: %d\n", 
&x, x);
  printf("Address of p: %p\n Value of p: %p\n", 
&p, p);
  printf("Address of y: %p\n Value of y: %d\n", 
&y, y);
  printf("Value stored in address %p is %d\n", p
, *p);
  return 0;
}
```

- 通过这段代码就可以看出 x，p 和 y 之间的关系

```
Address of x: 0x30e2af178
Value of x: 7
Address of p: 0x30e2af170
Value of p: 0x30e2af178
Address of y: 0x30e2af16c
Value of y: 7
Value stored in address 0x30e2af178 is 7
```

- x 作为一个很正常的 Variable，地址是 `0x30e2af178` ，值是 7，而 p 作为Pointer，地址是一个新的内存，而值应该是 x 的地址 `0x30e2af178` ，而 y 也是一个独立的 Variable

# 6.3 Use Pointers to Communicate

- 既然解决了前面提到的 Call by Value 的问题，就能通过 Points 解决如 loop，function 内部 Variable 的问题了

``` c
#include <stdio.h>
void swap(int*, int*);
int main(void) {
  int a = 9, b = 13;
  printf("Before swapping\nValue of a: %d\nValue of b: %d\n", a, b);
  swap(&a, &b);
  printf("After swapping\nValue of a: %d\nValue of b: %d\n", a, b);
  return 0;
}
void swap(int* x, int* y) {
  int temp = *x;
  *x = *y;
  *y = temp;
}
```

- 当 Variable 本身已经是一个 Pointer 的时候，`*x` 则变成了解析值，也就是该内存下储存的值，上面的例子中，`swap` 中的 `int temp = *x;` 则是令 temp 等于 Pointer x 的值也就是 9
- `*x = *y;`，已知 `x` 是 `&a`，也就是变量 a 的地址，而 `*x`则就是变量 a 的 Value，对于 y 同理，那么这一行就代表了 `a = b`，将 b 的值赋值给 a，有

## 6.3.1 Size of pointer Variable

- 前面提到了以前的机器采用 32 bits 表示内存，而现今的采用 64 bits，

``` c
#include <stdbool.h>
#include <stdio.h>

int main(void) {
  printf("Size of pointer (int*) is %d.\n", sizeof(int*));
  printf("Size of pointer (double*) is %d.\n", sizeof(double*));
  printf("Size of pointer (bool*) is %d.\n", sizeof(bool*));
  printf("Size of pointer (char*) is %d.\n", sizeof(char*));
  return 0;
}
```

- 使用 `sizeof` 就可以知道一个变量的 Size，即在这里是 8 bytes (64 bits)

## 6.3.2 Can a pointer hold address of another pointer ?

- 一个 Pointer 确实可以指向另一个 Pointer 的地址，因为他们本质上都是 Address
- 一个 Int 的 Pointer 为 `int*` 而他的 Pointer 则是 `int**`，即每一次加一个 `*`

|**变量**|**存储的地址**|**存储的值**|
|---|---|---|
|`i`|`45`|`10`（整数值）|
|`pi`|`46`|`45`（即 `i` 的地址）|
|`ppi`|`47`|`46`（即 `pi` 的地址）|
## 6.3.3. Can a function return a pointer?

- 可以，以下 function 就是一个接收 Pointer，在函数内部使用 `*` 访问 Pointer 值，在比较大小后返回较大的值的 Pointer 的一个函数

```c 
#include <stdio.h>
double* largestValLoc(double*, double*);
double* largestValLoc(double* a, double* b) {
  double* temp;
  if (*a > *b) {
    temp = a;  // temp is double* and a is double*, so temp = a is permissible
  } else {
    temp = b;
  }
  return temp;  // temp is double*, and return type is double*
}
int main(void) {
  double x = 2.6, y = 7.3;
  double* p =
      largestValLoc(&x, &y);  // pass address of x to a, and address of y to b
  // p is (double*) and largestValLoc returns 
(double*)
  printf("Address of x: %p having value %.1lf.\n", &x, x);
  printf("Address of y: %p having value %.1lf.\n", &y, y);
  printf("Address of larger variable: %p.\n", p);
  return 0;
}
```

## 6.3.4. Initialization Vs. Declaration of a pointer variable

- Declaration 和 Initialization 也存在着区别

### Declaration 声明

- Declaration 告诉了编译器 Variable 的 Type，并为其分配了 Memory，在这时 Variable 仅被创造而未被赋值 （存储了不确定的“垃圾值”）

``` c
int x;       // 仅声明 x，x 里面的值是不确定的（垃圾值）
int *p;      // 仅声明指针 p，但 p 没有指向任何有效地址（垃圾指针）
```

- 上方代码只做了 Variable 的 Declaration 而未赋值，在运行时会报错

``` c
#include <stdio.h>
int main() {
    int* p;  // 仅声明指针 p，但未初始化
    *p = 5;  // 试图通过 p 访问地址并赋值
    return 0;
}
-> warning: variable 'p' is uninitialized when used here [-Wuninitialized]
    *p = 5;
     ^
```

### Initialization 初始化

- 在 Declare Variable 的同时赋予其一个值

```c
int x = 5;      // 声明并初始化 x，x 现在存储 5
int *p = &x;    // 声明并初始化指针 p，使其指向 x
```

- 这里给 x 赋值了 5，给 Pointer 赋值了 x 的 Address

## Null 

- 在 C 语言中，`Null` 是一个特殊的值，当用作值时为 0，而代表地址的时候表示 “不指向任何有效地址”，他的主要作用时防止未初始化的指针指向随机地址导致程序崩溃

``` c
int *p;  // ❌ 未初始化的指针
*p = 5;  // 可能会崩溃（指向垃圾地址）
```

- 上述代码中，由于 pointer 未被 Initialize，则会产生 Segmentation Fault 问题，修正的办法则是通过 `Null`

``` c
int *p = NULL;  // ✅ 初始化为 NULL
if (p != NULL) {
    *p = 5;  // 只有当 p 指向有效地址时才执行
}
```

- 这就提供了一种安全的检查指针是否有效的办法

## ex. 

``` c
#include <stdio.h>
int *confuse(int *x, int *y) {
  (*y)++;
  y = x;
  *y = 10;
  return (y);
}
int main(void) {
  int a = 6, b = 7;
  int *f = &b;
  f = confuse(&a, &b);
  (*f)++;
  printf("a = %d and b = %d\n", a, b);
  return 0;
}
```

|**步骤**|**变量 `a`**|**变量 `b`**|**指针 `f`**|
|---|---|---|---|
|初始化|6|7|`&b`|
|`(*y)++` (`b++`)|6|8|`&b`|
|`y = x`（y 指向 `a`）|6|8|`&b`|
|`*y = 10`（修改 `a`）|10|8|`&b`|
|`return y;`（返回 `&a`，即 `f = &a`）|10|8|`&a`|
|`(*f)++`（`a++`）|11|8|`&a`|
- 所以最后的结果为 a = 11, b = 8

# 6.4. Rules defining scope of variables

- Scope 代表了在编译器中，Variable 应该出现在哪些位置才能被正确的使用

## 6.4.1. Variables can only be used after they are declared

- 必须要先 Declare Varibale 后才能赋值

``` c
int main() {
  i = 0;
  int i;
  return 0;
}
```

- 这就会报错 compile-time error

### Local Variables

- 在 Function 内部声明的变量称为 Local Variables，它的 Scope 从被 Declare 开始到 Function 结束时结束

## 6.4.2. Use a variable declared in a compound statement

- 在 C 语言中，Variable Scope 受 `{}` 所限制，即其只能在它被 Declare 的 Compound Statement 内部可见，在 `{}` 外部的调用会导致 Undeclared Identifier

``` c
#include <stdio.h>
int main() {
    int i = 0;  // 变量 i 在 main() 作用域内有效
    {  // 复合语句（新的作用域）
        int x = 5;  
        printf("Inside compound statement: x = %d.\n", x);  // ✅ 正确，x 在作用域内
    }
    // ❌ 错误：x 作用域结束，无法访问
    printf("Outside compound statement: x = %d.\n", x);  

    return 0;
}
```

- 对于上面的这种情况，解决方案就是分离 Declaration 和 Initialization

``` c
#include <stdio.h>
int main() {
    int i = 0;
    int x;  // 声明 x 在整个 main() 内有效
    { 
        x = 5;  
        printf("Inside compound statement: x = %d.\n", x);
    }
    printf("Outside compound statement: x = %d.\n", x);  // ✅ 正确
    return 0;
}
```

- 通过在 Compound Statement 外部的声明使得其 Scope 变化至整个 `main()` 中

## 6.4.3. External identifiers/global variables

- 在 C 语言中，Global Varibale 在整个程序中都是可见的

``` c
#include <stdio.h>
int i = 0;  // ✅ 全局变量 i，所有函数都可以访问
void func();  // 函数声明
int main(void) {
    printf("In main: Global variable i = %d.\n", i);  // 输出 i = 0
    func();  // 调用 func()
    printf("In main after calling func: Global variable i = %d.\n", i);  // 输出 i = 5
    return 0;
}
void func() {
    printf("In func: Global variable i = %d.\n", i);  // 输出 i = 0
    i = 5;  // ✅ 修改全局变量 i
}
```

- 在 C 语言中，External Identifier 通常指的是 在函数外部声明的变量、函数或其他可被多个文件访问的实体，其主要特性是 Scope 覆盖整个程序

## 6.4.4. Overlapping scope

- 不同 Scope 下可以 Declare 具有相同名称的同名变量，由于这一个 Scope 的 Overlap，可能会导致变量的 Shadowing

``` c
#include <stdio.h>
int main(void) {
    int i = 1;  // ✅ 作用域：整个 main() 函数
    printf("Outer i = %d.\n", i); // 输出 1
    {
        int i = 2;  // ✅ 作用域：仅限于这个 `{}` 块
        printf("Inner i = %d.\n", i); // 输出 2
    }
    printf("Outer i = %d.\n", i); // 输出 1
    return 0;
}
```

> 可以发现，Variable 是否会被修改取决于是否出现了多个 Declarations，对于 6.4.3 中的代码来说，全局只有一个 Declaration，即 `int i = 0` ，而在 6.4.4 中存在两个 Declarations，`int i = 1`，`int i = 2`，这就导致了 Cpmpound Statement 内部的修改不会影响到外部

# 6.5. Goldbach conjecture

- 写一个程序来检查给定偶数是否符合 Goldbach Conjecture 哥德巴赫猜想

## 6.5.1 Problem Statement 

- 他的猜想如下，所有大于 2 的偶数都可以表示为两个质数的和

## 6.5.2 Divide Problem into sub-problems

- **获取用户输入** —— 读取用户输入的偶数
- **验证输入是否合法** —— 确保输入是大于 2 的偶数
- **验证哥德巴赫猜想** —— 查找是否存在两个质数相加等于该数
- **输出结果** —— 打印该数是否符合哥德巴赫猜想

### 6.5.2.1. Take input from the user

- 首先要确保 Input 大于 2，有

``` c
void getUserInput(int *number) {
  // Get user input from the keyboard
  // and validates it is even and greater than 2
  do {
    printf("Enter a number to test the Goldbach conjecture: ");
    scanf("%d", number);
  } while (*number <= 2 || *number % 2 != 0);
}
```

- 优化代码如下 

```c
#include <stdbool.h>
#include <stdio.h>

void getUserInput(int*);

int main(void) {
    int num;
    getUserInput(&num);
    return 0;
}

void getUserInput(int *number) {
    // 获取用户输入，并验证其是否为大于 2 的偶数
    bool firstEntry = true;  // 标记是否是第一次输入

    do {
        if (firstEntry) {
            printf("Enter a number to test the Goldbach conjecture: ");
            firstEntry = false;
        } else {
            printf("Your input was invalid, please enter another even number > 2: ");
        }
        scanf("%d", number);
    } while (*number <= 2 || *number % 2 != 0);
}

```

### 6.5.2.2. Test the Goldbach

- 现在要验证猜想，给定一个偶数，遍历小于它的一半的质数，依次将他们从偶数上减去，判断差是否为质数，后重复过程
- 几个需要用到的函数有 `bool isPrime(int);` ，`void nextPrimeNumber(int*);`

``` c
bool testGoldbach(int N) {
    // 测试哥德巴赫猜想
    // 如果验证成功返回 true，否则返回 false
    int x = 2, y;
    bool rejected = false;
    bool verified = false;

    while (!rejected && !verified) {
        y = N - x;

        if (isPrime(y)) {
            verified = true;  // 找到了 x + y = N 的质数对
        } else if (y < x) {
            rejected = true;  // 当 x > y 时，仍未找到符合条件的 x, y
        } else {
            nextPrimeNumber(&x);  // 递增 x 到下一个质数
        }
    }

    return verified;  // 如果找到了两个质数，则返回 true，否则返回 false
}
```

### 6.5.2.3. Get the Next Prime Number

- 获取下一个质数的函数需要自己定义，逻辑就是在当前值上 + 1，并判断是否是 Prime Number，若是则返回，不是则循环

```c
void nextPrimeNumber(int *px) {
  // We will look for the numbers after *pFrist one by one 
  // until we find the next prime number
  int value = *px + 1;
  while (!isPrime(value)) {
    value += 1;
  }
  *px = value;
}
```

### 6.5.2.4. Find If a Number Is Prime or Not

- 判断 Prime Number 的函数也需要实现，有

```c
bool isPrime(int num) {
  // check if num is prime, by checking the remainder of num / all numbers from
  // 2 to num - 1
  bool prime = true;
  if (num < 2) {
    prime = false;
  } else {
    for (int denom = 2; denom <= num - 1 && prime; denom++) {
      if (num % denom == 0) {
        prime = false;
      }
    }
  }
  return prime;
}
```

- 逻辑就是遍历比它小的所有大于 2 的数，挨个除过去看余数是否为 0 ，若皆不为 0 ，则是 Prime Number

### 6.5.2.5. Print If the Conjecture Is Verified

- 还需要一个输出函数

> 完全不需要这个

``` c
void printConjResult(int number){
    //Call a function to verify the conjecture and prints the result
    bool verified = testGoldbach(number);
    if(verified){
        printf("Goldbach conjecture is verified.\n");
    }
    else{
        printf("Goldbach conjecture not verified.\n");
    }
}
```

## 6.5.3. Integrate all pieces/functions

- 完成了所有函数的实现后，整合所有函数实现完整流程

```c
int main(void){
    int number;
    getUserInput(&number);
    printConjResult(number);
    return 0;
}
-> Enter a number to test the Goldbach conjecture: **9**
Your input was invalid, please enter another number > 2: **8**
Goldbach conjecture is verified.
```


