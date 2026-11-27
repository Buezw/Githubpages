---
title: "LPC 4. Repetition"
lang: en
date: 2025-01-20
tags: ["Docs","LPC"]
math: mathjax
showWordCount: true
---
> Last Edit: 1/20/25

Loops帮助程序节省空间，提高编写效率并减少错误，常见的Loop存在两种，while loop和for loop

# 4.1 While Loop

``` c
while (<condition>) {
  <statements>;
}
<other statements>;
```

- while loop会重复循环直到while内的`condition`不再成立，也就是说当`<condition>`为True时，程序将会不断重复执行`<statement>`

``` python
#include <stdio.h>
int main(void) {
  int i = 1;
  while (i <= 10) {
    printf("%d ", i);
    i++;
  }
  return 0;
}
```

- 这就是一个很简单的累加器的例子，程序依次打印1到10后跳出循环

## 4.1.2 Infinite Loops

- 如果永远跳不出Loop，就叫做Infinite Loops

# 4.2 Do-while Loop

- 与While最大的区别就在于，Do-while Loop会至少执行`<statement>`一次，之后根据Condition判断是否循环

``` c
do {
  <statements>;
} while (<condition>);
```

- 可以看出，无论`<condition>`为True or False，都将先做一遍statement的

## 4.2.2 Do-While vs. while

``` c
#include <stdio.h>
int main(void) {
  int num;
  do {
    printf("Please enter a number between 1 
and 10 (inclusive): ");
    scanf("%d", &num);
  } while (num < 1 || num > 10);
  printf("The number entered is %d.\n", num);
  return 0;
}
```

# For loops

`for` 循环的本质是为了解决重复执行一定次数的任务的问题，尤其是在**已知迭代次数**或需要**遍历某个范围或集合**的场景下

## 4.3.1 Forming for loop

``` c
for (<initialization>;<condition>;<increment>) {
  <statements>;
}
<other statements>;
```

- 可以看到相比于while，for更像是while的下层应用，将问题具体到了已知范围的事件下

``` c
#include <stdio.h>
int main(void) {
  for (int i = 1; i <= 10; i++) {
    printf("%d ", i);
  }
  return 0;
}
```

- 对比上方的while，他们干了相同的事件不过用了更加简介的API

## 4.3.2 Scope of the loop variable

- 对于For loop来说一般都会存在一个变量充当累加器的作用，其Scope 作用域将在Loop结束后不再可用

``` c
#include <stdio.h>
int main(void) {
  for (int i = 1; i <= 10; i++) {  // declare & 
initialize the loop variable inside the loop
    printf("%d ", i);
  }
    
  printf("\nWe exited the loop with i = %d \n", i);
  return 0;
}
```

- 上述代码展示了Loop内部的i和外部的i的访问，由于`printf("\nWe exited the loop with i = %d \n", i);`调用的是out of scope的，所以将会报错
- 其解决方案就是在执行循环前先定义Variable，也就是在外面加一句`int i = 0;`

## 4.3.3 Variations in for loop

- 实际上，for loop存在许多变体使得他可以省略一些参数

``` c

#include <stdio.h>  
int main(void) {
  for (int i = 1, j = 7; i <= 10; printf("7 * %d = %d\n", i, j), i += 1, j += 7);
  return 0;
}
```

- 这本质和以下代码是一样的

``` c
#include <stdio.h>  
int main(void) {
  for (int i = 1, j = 7; i <= 10;)
    printf("7 * %d = %d\n", i, j);
    i += 1;
    j += 7;
    
return 0;
}
```

- 变体使得代码在可能略微减少大小的情况下使得整体可读性，是一种非常不健康的写法

# 4.4 Nested Loop

Loop中套Loop，复杂度变成多项式复杂度

## 4.4.1 Print 2D pattern

- 如果想要打印出以下图案

``` text
*
**
***
****
*****
```

- 可以通过设计外层loop构建层，内层loop确定单层打印个数的方式完成

``` c
#include <stdio.h>
int main(void) {
    for (int line = 1; line <= 5; line += 1) {  // 外层循环控制行数
        for (int star = 1; star <= line; star += 1) {  // 内层循环控制每行星号的数量
            printf("*");
        }
        printf("\n");  // 每行结束后换行
    }
    return 0;
}

```

## 4.4.2 Tweak a little

- 现在要打印这个

``` 
    *
   **
  ***
 ****
*****
```

- * 前的部分为空格

``` c
#include <stdio.h>
int main(void) {
  int n = 0;
  printf("Enter the number of rows:");
  scanf("%d", &n);
  for (int row = 1; row <= n; row += 1) {
    for (int col = 1; col <= n; col += 1) {
      if (col <= n - row) {
        printf(" ");
      } else {
        printf("*");
      }
    }
    printf("\n");
  }
  return 0;
}
```

# 4.5 Debugging for loops

- 本节将会给出一个loop的错误，需要发现该错误并修正，想要打印一个

``` 
Enter the number of rows: **5**
    *
   ***
  *****
 *******
*********
```

``` c
#include <stdio.h>
int main(void) {
  int n = 0;
  printf("Enter the number of rows: ");
  scanf("%d", &n);
  for (int row = 1; row <= n; row += 1) {
    for (int col = 1; col < n; col += 1) {
      if (col <= n - row) {
        printf(" ");
      } else if (col >= n - row || col <= n - 1 
+ row) {
        printf("*");
      }
    }
    printf("\n");
  }
  return 0;
}
```







