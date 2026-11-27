---
title: "LPC 5. Functions"
lang: en
date: 2025-01-28
tags: ["Docs","LPC"]
math: mathjax
showWordCount: true
---
> Last Edit: 1/28/25

# 5.1 Functions

Function是用来执行特定任务的可重复调用恶的代码块，通过Modular Programming将复杂问题分解

``` c
void printStars(int numOfStars) {
    for (int star = 1; star <= numOfStars; star++) {
        printf("%c", '*');
    }
    printf("\n"); // to start a new line
}
```

- 这个函数包含了一下的属性
- 返回类型：`void`（不返回任何值）
- 函数名称：`printStars`
- 输入参数类型：`int`
- 输入参数的变量名：`numOfStars`
- 函数体：包含用于打印一行星号的指令

## 5.1.1 Void

- `void` 用于表示无类型或无值，`void` 指的是函数的返回类型，表示这个函数在执行完毕后不会返回任何值

# 5.1.2 Function Prototype

- 在C语言中，Function Prototype 是用来在函数实际定义前声明函数接口的代码，其包含了改函数的调用参数类型和数量，但不包含具体的执行内容

``` c
void printPattern(int numOfRows);
void printStars(int numOfStars);
```

- 这行就是两个Function的Prototype，表明了两个函数均需要整数作为输入

## 5.1.3 Order of execution

- 在C语言中，存在编译和执行的两个步骤，从编译来说，顺序是从上到下的，这就代表了下方是可以引用上方的定义，但是如果下方需要引用的东西在上方没有出现，则会报错因为找不到目标
- 具体来说所有函数和参数的**下方**就是 `main` 函数，因为C语言在**运行**的时候是从 `main` 函数开始的，也就是说所有在 `main` 中call到的function都应该在**上方**被定义，但为了[##5.1.4 Another way to write functions]中将要提到的问题，Funtion Prototype被定义用来优化代码
- 而C语言程序的执行始终从 `main` 函数开始，这时函数已经完成了编译，也就是已经编译完了整个代码，所以这时的 `main` 是可以找到任意位置上的 function 的，而不是从源文件的最上方向下逐行执行
- 通过在 `main` 函数中调用函数，其能找到任意函数，即编译器可以知道函数的存在以及他的接口是什么

## 5.1.4 Another way to write functions

- 如果不写 Function Prototype 的话，就需要把所有Function的定义放置在 `main` 函数的前方以确保在编译 `main` 的时候不会因为找不到而报错

``` c
# include <stdio.h>

void printStars(int numOfStars) {
  for (int star = 1; star <= numOfStars; star++) {
    printf("%c", '*');
  }
  printf("\n");  // to start a newline 
}

void printPattern(int numOfRows) {
  for (int row = 1; row <= numOfRows; row++) {
    printStars(row);
  }
}

int main(void) {
  int lines;
  printf("Enter the number of lines in the pattern:");
  scanf("%d", &lines);
  prinntPattern(lies);
  return 0;
}
```

- 但是这种写法使得代码的可读性降低了很多，这可能导致 `main` 函数远离文件的起始位置，使得跟踪程序流程更加困难
- 同时在多人开发环境中，团队成员通常需要清楚地知道可以调用哪些函数及其参数，而不必查看每个函数的实现。函数原型在头文件中提供了这样的信息，便于团队成员之间的协作

### 5.1.4.1 Error Case

- 如果代码如下

``` c
#include <stdio.h>

void printPattern(int numOfRows) {
    for (int row = 1; row <= numOfRows; row++) {
        printStars(row);
    }
}

void printStars(int numOfStars) {
    for (int star = 1; star <= numOfStars; star++) {
        printf("%c", '*');
    }
    printf("\n"); // to start a new line
}

int main(void) {
    int lines;
    printf("Enter the number of lines in the pattern: ");
    scanf("%d", &lines);
    printPattern(lines);
    return 0;
}

```

- 在上面的代码中，在，代码的`printPattern` function中调用了 `printStars(row)` ，但是这个函数的定义位于下方，如果在一个函数被调用之前，编译器没有遇到这个函数的声明或定义，它就不会知道这个函数的存在，导致编译错误

# 5.2. Communicate from a function

- 前面提到的 Functions 并没有任何返回值，这是因为定义 Function的时候采取的是 `void`

## 5.2.1 Return a non-void variable type

``` c
#include <stdio.h>
int factorial(int n);

int main(void) {
    int number = 4;
    int result = factorial(number);
    printf("Factorial of %d: %d.\n", number, result);
    return 0;
}

int factorial(int n) {
    int fact = 1;
    for (int i = 1; i <= n; i++) {
        fact = fact * i;
    }
    return fact;
}
```

- `factorial` 函数接收一个 `int` 参数 `n`，并返回 `n!`
- `return fact;` 语句将计算结果返回给调用者，即 `main` 函数
- `main` 通过 `result = factorial(number);` 获取返回值并存储
- `printf` 用于打印最终结果

## 5.2.2. Summary of syntax

``` c
#include <stdio.h>
// 函数原型（声明）
<return type> functionName(<type>);
int main(void) {
    // 调用有返回值的函数
    <type> variableName = functionName(<variable to pass>);
    // 调用无返回值的函数
    functionName(<variable to pass>);
    return 0;
}
// 函数实现（定义）
<return type> functionName(<type> <input parameter name>) {
    return <变量，类型与 <return type> 相同>;
}
```

# 5.3 Variable Scope

在前面的Loop单元中提到过 Variable Scope 的概念，即一个变量的定义范围，在前面提到的是loop中的variable只能作用在其循环当中，想要让其作用于循环外则需要在外部声明变量

``` c
int count;
for (count = 1; count <= n; count++) {
    printf("*");
}
count = 10;  // ✅ 正确，count 在整个函数内都可用
```

- 同样的，Function 中的变量也只能储存在 Function 中

``` c
#include <stdio.h>
// 函数声明
double divideByTwo(double);
int main(void) {
    double n = 4.2, result;
    result = divideByTwo(n);
    printf("%lf,%lf", n, result)
    return 0;
}
// 函数定义
double divideByTwo(double n) {
    n = n / 2;
    return n;
}
```

- 在这个程序中同时存在两个 `n` 其中函数中的独立于外部主程序存在
- 所以这个程序的返回值将会是 `4.2,2.1`

# 5.4. Pass more values to a function

- 一个函数可以指定接收多个 Variable

``` c
#include <stdio.h>
int median(int, int, int); // Prototype
int main(void) { // Main Function
  printf("The median of (%d, %d, %d) is %d\n", -105, -28, -73, median(-105, -28, -73));
  printf("The median of (%d, %d, %d) is %d\n", 0, -101, 98, median(0, -101, 98));
  printf("The median of (%d, %d, %d) is %d\n", -101, -67, 0, median(-101, -67, 0));
  return 0;
}
int median(int x, int y, int z) { // Function Body
  int result = 0;
  if ((x >= z && x <= y) || (x >= y && x <= z))
    result = x;
  else if ((y >= x && y <= z) || (y >= z && y <= x))
    result = y;
  else
    result = z;
  return result;
}
```






