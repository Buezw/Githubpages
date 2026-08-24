---
title: "LPC 8. Dynamic Memory Allocation "
date: 2025-03-07
tags: ["Docs","LPC"]
math: mathjax
showWordCount: true
---
> Last Edit: 3/7/25


前面提到过了 Array 中的 Memory 的分配方式是固定的连续内存，而想要修改 Array 的大小则变得困难，这时候就需要通过 Dynamic Memory Allocation 来动态的分布内存

# 8.1 Dynamic Memory Allocation

- Dynamic Memory Allocation 的核心就是在 Runtime 即时分配内存空间的过程，分配的内存量在编译时不需要预先知道

## 8.1.1 Different Options when array size is unknown

- 一种可以采取的方法就是直接给一个非常大的 Array size，但这不可避免的会造成浪费
- 一般来说，一个程序的 Main Memory 主要会被分成四个主要部分

### Code

- 代码段负责储存代码

### Const + Global

- 所有的程序常量和变量都会被存储在这

### Heap

- 储存动态分配的内存

### Stack

- 储存 function 的局部变量，如果一个函数调用另一个函数，他的局部变量会被储存于此

### Stack Overflow 栈溢出

- 当 Stack 部分的 Memory 被耗尽的情况下，没有更多空间的时候会报的错

### Variable Size Array

- Array 的大小可以被用一个 Variable 决定，这是一种灵活的分配方式，根据需要分配实际大小，以下是一种示例

```c
#include <stdio.h>
int main(void) {
  int size;
  printf("Enter size of array: ");
  scanf("%d", &size);
  int arr[size];
  printf("Array allocated from %p to %p", arr, arr+size);
  return 0;
}
```

- 使用这种方式，即使使用了 Variable 决定 Array 的 Size，其本质上还是在 Array 上分配的，如果 Stack 的空间不足后，还是会报错

### Dynamically Allocate Memory

- 通过将 Memory 放置到 heap 上，这需要 `stdlib.h`: `malloc` 库里的内容
- `malloc(size_t size)`会分配指定字节数的内存块，并返回指向该内存块首地址的指针。如果分配失败，返回NUL
- 当使用`malloc`为数组分配内存时，需要指定分配的总字节数，通常是数组元素的数量乘以单个元素的大小
- 例如，要为5个 int 分配内存，可以使用表达式`malloc(5 * sizeof(int))`

### Memory Leak

- 在 Dynamic 分配完了 Memory 后，临时放置在 Stack 中的储存 malloc 中第一个 Element 的 Pointer 也会消失，而这时候如果没有收回之前分配的 Memory，会导致 Memory Leak

```c
#include <stdio.h>
#include <stdlib.h>

double getAverage(int);

int main(void) {
  int size;
  printf("Enter size of array:");
  scanf("%d", &size);
  double avg = getAverage(size);
  printf("Average is %.2lf\n", avg);
  return 0;
}

double getAverage(int size) {
  int* myArray = (int*)malloc(size * sizeof(int));

  printf("Enter grades:");
  for (int index = 0; index < size; index++) {
    scanf("%d", &myArray[index]);
  }
  int sum = 0;
  for (int index = 0; index < size; index++) {
    sum += myArray[index];
  }
  return (double)sum / size;
}
```

- 简单来说，由于 Pointer 的丢失，已经无法再次访问这个 Array，但是其还在那个地方，会导致 1. 无法再次访问，2. 空间仍然被占用
- 一个合理的解决方案就是在 return 之前将已有的空间收回，也就是 `free`
- free 的 Prototype 为 `void free(void *pointer);`
- `free`函数用于释放 `malloc` 分配的内存，它接受一个指向要释放内存的 Pointer，并释放该内存块，但是一旦 Memory 被释放，原有的指针变量仍然存在，但其指向的是一个不再有效的内存区域，这时候需要将 Pointer 设置为 Null

```c
#include <stdio.h>
  #include <stdlib.h>
  
  double getAverage(int);
  
  int main(void) {
    int size;
    printf("Enter size of array:");
    scanf("%d", &size);
    double avg = getAverage(size);
    printf("Average is %.2lf\n", avg);
    return 0;
  }
  
  double getAverage(int size) {
    int* myArray = (int*)malloc(size * sizeof(int));
    
    printf("Enter grades:");
    for (int index = 0; index < size; index++) {
      scanf("%d", &myArray[index]);
    }
    int sum = 0;
    for (int index = 0; index < size; index++) {
      sum += myArray[index];
    }
    free(myArray);
    myArray = NULL;
    return (double)sum / size;
  }
```