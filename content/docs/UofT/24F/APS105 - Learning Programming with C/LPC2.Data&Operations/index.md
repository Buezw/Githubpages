---
title: "LPC 2. Data & Operations"
date: 2025-01-09
tags: ["Docs","LPC"]
math: mathjax
showWordCount: true
---
> Last Edit: 1/9/25

# 2.1 Double data type for real numbers

- 在程序中用分数代表数字

## 2.1.1 Convert Inches to Centimeters 

``` c
// Description: This program convert inches to centimeters
#include <stdio.h>

int main(void){
  // Declare variables
  const double InchesToCm = 2.54;
  double inputInches, outputCm;

  // Prompt user for input
  printf("Enter the number of inches to convert to cm: ");
  scanf("%lf", &inputInches);
  // Convert inches to centimeters
  outputCm = inputInches * InchesToCm;
 
  // Display output in 2 decimal places
  printf("The number of centimeters is %.2lf\n", outputCm);
  return 0;
}
```

- `const`是一个关键字，指示变量是常量。不能在整个代码中更改该变量

``` c
int main(void){
	const double InchesToCm = 2.54;
	InchesToCm = 2.51;
}
```

> 这样操作将会报错，因为`InchesToCm`是一个不可以更改的Constant

- `double` 是一种数据类型，指示变量是小数

> What would happen if a number with decimal is stored in an `int`?
> 	当赋值一个小数给`int`的时候，小数部分将被 Truncated 截断，只保留整数部分

- `%lf` 这是一个格式说明符，指示输入是小数
- `.2` 表示该值应以 2 位小数打印

## 2.1.2 Summary

- `int`：整数数据类型，Format Specifier是`%d`
- `double`：小数数据类型，Format Specifier是`%lf`

# 2.2 Data types and representation 

- 不同的数据类型在Memory中的储存方式都不同

## 2.2.1 Integers

- `int`使用32位存储，其中31位用于表示整数本身，一位为Sign Bit
- Sign bit为0是说明整数是正数，为1说明是负数
- 由于有整数可以有31位，其在正数的范围为0到$2^{31}-1$，在负数的范围为$-2^{31}$到-1

### Other Integers Representation

- `short`：16位整数
- `unsigned int`：使用32位，没有符号位，表示范围是0到$2^{32} - 1$
- `long`：通常使用64位（8个字节）
- `long long`：也是使用64位（8个字节）

## 2.2.2. Floating point or real numbers

- `float`的储存方法类似于科学计数法，其写成$m\times 10^e$的形式
- 其中m是尾数，是一个介于1到10的数字，e是指数，表示数字的大小

### Two float Representation

- `float`使用32位，即4bytes
- `double`使用64位，即8bytes，由于精度是float的两倍，也叫Double data type双精度

## 2.2.3. Characters

- 要表示一个字符（如字母、符号或数字），可以使用 `char` 数据类型。常见的字符包括 A, B, 1, 9, @, # 等

``` c
#include <stdio.h>

int main(void){
  char firstInitial = 'S';
  printf("My first initial is %c.\n", firstInitial);
  return 0;
}
```

- The format specifier for `char` is `%c`
- `char` 类型使用8bits（1bytes）来存储每个字符
- 其可以于ASCII编码对应范围是0到$2^7-1$
- **ASCII** 标准使用7位来表示字符，第8位是多余的，因此它被设置为0以兼容字节存储结构。这是因为ASCII最初设计时，只有7位用于字符表示，8位的字节结构是为了适应现代计算机的存储需求

## 2.2.4. Boolean

- 布尔类型用于表示逻辑值，即 `true` 或 `false`。在C语言中，`true` 被表示为 `1`，而 `false` 被表示为 `0`
- 尽管布尔类型只需要1个bit来表示其值，但由于内存的组织结构，每个内存单元（cell）通常存储1byte，因此布尔类型在内存中实际占用1byte

``` c
#include <stdbool.h>
#include <stdio.h>

int main(void){
  bool isRaining = true;
  printf("Is it raining? %d\n", isRaining);
  return 0;
}
```

- Boolean没有专门针对的格式说明符，采用`%d`来打印值
- 使用布尔类型时，需要包含 `<stdbool.h>` 库。没有这个库，编译器无法识别 `bool` 类型

### ex.

- 假设n是正整数
```c
bool isPositive = n > 0;
> True
bool isPositive = n;
> True or False,any non-zero number is considered as `true`
bool isPositive = n > 0 != 0;
> True
bool isPositive = n <= 0 != 1;
> n<=0 is 0, 0 != 1 -> 1 or True

```

## 2.2.5. Declaring Vs. Initializing Variables

- Declaring Variables是告诉编译器使用某个变量。在C语言中，声明一个变量的语法是`int var;`
- 这样，编译器知道了一个类型为 `int` 的变量，名为 `var`。此时，编译器为变量保留了内存空间，但此变量尚未被赋值
- 变量声明后如果没有赋值，它就是Uninitialized Variables 未初始化变量，这意味着变量没有存储任何有效的值，只是占据了一块内存
- 如果你声明了一个变量 `var`，但没有给它赋值，那么它的值可能是一个随机值，例如 `174739296`（这只是一个示例值，实际结果因每次运行而异）。每次运行时，这个值可能会不同

``` c
#include <stdio.h>

int main(void) {
  int var;
  printf("Value of uninitialized variable \"var\": %d\n", var);
  int var2 = 0;
  printf("Value of initialized variable \"var\": %d\n", var2);
  return 0;
}
```

- 编译器会发出警告，指出未初始化的变量 `var` 在使用时可能会导致不确定的行为。警告信息类似于：`variable ‘var’ is uninitialized when used here [-Wuninitialized]`
- 为了避免这种警告，最佳做法是声明变量并初始化它，例如：`int var = 0;`

## 2.2.6. Taking in input from the user using `scanf`

### Mutiple Numbers in mutiple variables

``` c
#include <stdio.h>
 
int main(void) {
  int num1 = 0, num2 = 0;
  double dnum1 = 0, dnum2 = 0;
  printf("Enter a number: ");
  scanf("%d %lf %d %lf", &num1, &dnum1, &num2, &dnum2);
 
  printf("Numbers entered: %d %lf %d %lf\n", num1, dnum1, num2, dnum2);
 
  return 0;
}
> 1 1.2 3 3.4
> Enter a number: 1 1.2 3 3.4 Numbers entered: 1 1.200000 3 3.400000
```

- 可以使用 一个 `scanf` 来接收多个输入，并将它们分别存储在多个变量中。输入的各个数值通过分隔符（如空格、回车或制表符）分隔

### Numbers and Characters

``` c 
#include <stdio.h>
 
int main(void) {
  char idChar;
  int idNum;
  printf("Enter your ID: ");
  scanf("%c %d", &idChar, &idNum);
 
  printf("ID entered: %c%d\n", idChar, idNum);
 
  return 0;
}

> S1321234
> Enter your ID: S1321234 ID entered: S1321234
```

- 你可以在同一行中使用 **`scanf`** 接收字符和数字。比如，用户输入一个以字符开头，后面跟随数字的ID。
- 使用 **`%c`** 来接收字符，接着用 **`%d`** 来接收数字。`scanf` 会自动区分字符和数字，不需要在字符和数字之间添加分隔符

### Take in characters and ignoring leading spaces

``` c
#include <stdio.h>
 
int main(void) {
  char c1, c2, c3, c4, c5, c6, c7;
 
  printf("Enter license plate letters and numbers: ");
  scanf("%c %c %c %c %c %c %c", &c1, &c2, &c3, &c4, &c5, &c6, &c7);
   
  printf("Licence plate entered: %c%c%c%c-%c%c%c\n", c1, c2, c3, c4, c5, c6,c7);
   
  return 0;
}
```

- 在这段代码中，为了忽略输入字符之间的空格，使用了 `scanf` 函数中的 `%c` 格式说明符之间加入空格的方法。这样，`scanf` 在读取每个字符时会自动跳过空格

### Common mistake: Spaces after format specifiers

``` c
#include <stdio.h>
int main(void) {
  double dnum1 = 0;
  printf("Enter a number: ");
  scanf(" %lf ", &dnum1);
 
  printf("Number entered: %.2lf\n", dnum1);
  return 0;
}
```

- `scanf` 使用了一个格式说明符 `%lf` 后跟一个空格。这种情况下，程序会在接收到一个数字输入后继续等待，直到遇到非空格的输入。这是因为 `scanf` 的行为是读取输入直到满足格式要求，而空格在格式说明符之后会导致它等待下一个非空白字符

# 2.3 Operations

- 通过已知的四种data types，`int`, `double`, `char`, `bool`来进行运算

## 2.3.1 Basic Arithmetic Operations

- 基础的算术运算还是通过 `+` `-` `*` `/` `%` 实现的
- 其中运算优先级根据括号，幂，乘，除，取模，加减的顺序，如果没有优先级，则从左到右的顺序运算

``` c
int x = 10 / 5 * 2;
```

- 先10/5=2再*2=4

## 2.3.2. The more accurate data type is contagious

``` c
int x = 10 * 5 / 3;
```

- 在数学中，这个的答案很明显是$16\frac{2}{3}$，但是10，5和3都是int，所以他们运算的值也必须是一个int，也就是16在这个例子中

``` c
int x = 50 / 3.0;
```

- 在这个例子中，由于3.0是一个double，他们的结果将会是一个double，但是由于是储存在`int`中的，所以16后面的小数部分**将被抛弃**只剩下16

## 2.3.3. What happens when we divide by 0?

- 在程序中除以0可能导致奇怪的结果，如果是double运算的话也有可能是inf

## 2.3.4. Modulo operator

- 取得Remainder 余数的运算符
- 如 `10%3=1`，`10%4=2`

> `3 % 0` 的结果是什么？
> 	会表现出和`3/0`类似的行为

## 2.3.5. Assignment operators

- 赋值运算符，也就是 `=` ，其优先级小于所有Operations，确保了所有运算结束后才会赋值
- 赋值运算与其他运算不同，是从右往左结合的，如

``` c
x = y =z
```

- 先将z的值赋值给y，再将y的值给x

### Complex Assignment Operations

- 形如 `+=`, `-=`, `*=`, `/=`, `%=` 的为复合赋值运算符
- `x += 3` 等价于 `x = x + 3` ，剩下的同理

## 2.3.6. Increment and decrement operators

- 想表达一个值+1有很多种方法，包含了`i += 1;`, `i++;` and `i++;`
- 这第三个就是Increment Operator，其可以放在Variable前后，放在前面，如 `++i` 代表了先将变量加一再更新值，而 `i++` 则是先更新值再加一 ，等价于

```c 
j = i;
i = i + 1;
```

## 2.3.7. Type casting

- 想要强制将一个数据类型转换为另一个也有很多做法

``` c
double x = 3 / 2; // x 的值是 1.0
```

- 因为 `3` 和 `2` 都是整数（`int`），所以 `3 / 2` 会执行整数除法，结果是 `1`，然后被存储为 `1.0`
- 如果希望 `x` 的结果是 `1.5`，需要将操作数之一转换为浮点数

``` c
double x = 3.0 / 2; // 或者
double x = (double) 3 / 2; // x 的值是 1.5
```

- `(double)` 将整数 `3` 转换为浮点数 `3.0`，然后执行浮点除法
- 假设需要将 `2.9` 转换为整数

``` c
double x = 3 / (int) 2.9; // x 的值是 1.0
```

- `(int) 2.9` 将 `2.9` 转换为整数 `2`，然后执行整数除法 `3 / 2`，结果是 `1`

## 2.3.8. `sizeof()` operator

- `sizeof` 用来计算某种数据类型或变量在内存中占用的字节数
- `sizeof(int)`：返回 `int` 类型的大小（通常为 4 字节）
- `sizeof(double)`：返回 `double` 类型的大小（通常为 8 字节）
- `sizeof(char)`：返回 `char` 类型的大小（通常为 1 字节）

# 2.4. Math library

- 运算符不只限于 `+-*/`，还包含了如 $\sqrt{x}$ 等复杂运算，他们可以通过math librbary实现

``` c
#include <math.h>
#include <stdio.h>
int main(void) {
  double a = 0, b = 0, c = 0;
  printf("Enter the lengths of the sides: ");
  scanf("%lf %lf", &a, &b);

  c = sqrt(a * a + b * b);
  printf("The length of the hypotenuse is %.2lf\n", c);
  return 0;
}
```

## 2.4.2. You can still use integer values

- 前面没提到的是，sqrt要求的输入实际上是 `double` 但是其实输入 `int` 也可以，系统会自动将其转换成 `double`
- 想要输出变成 `int` 也可以通过前面提到的 type casting

# 2.5. Random numbers

## 2.5.1. Generating a random number

- 需要先导入一个新的库叫做  `stdlib.h`，然后就可以用 `int rand();` 生成随机数了，由于类型是一个 `int` 这使得生成的范围将再 $[0,2^{31}-1]$ 内取值

``` c
#include <stdio.h>
#include <stdlib.h>
int main(void) {
  printf("Random number 1: %d\n", rand());
  printf("Random number 2: %d\n", rand());
  printf("Random number 3: %d\n", rand());
  return 0;
}
```

- 上述代码很简单，输出就是三个随机数，但是问题是当再一次运行这个程序的时候，会输出三个一样的随机值，这是因为C语言生成的是 Pseudo-random Numebrs 伪随机数，是通过某种算法得出的值，这就导致如果使用的是相同的随机种子时，每次运行程序都将得到一样的随机数
- 通过调用 `srand(unsigned int seed)` 可以设置伪随机数的种子，而这个种子会生成一个随机数的Sequence，调用了几次rand就会用到序列中的第几个数
- 这就导致了如果一个代码中重复的初始化了两次随机种子，随机数就会重置，下一次调用将从Sequence的第一个重新开始
 
## 2.5.2. Are we generating random numbers?

- 如果想得到一个真正的随机数，可以采用时间当作种子，调用 `time.h` 库便可以获取当前时间
 
### Time overflow Problem

- 使用 `time(NULL)` 可以返回自 **1970年1月1日**（Unix 纪元）以来的秒数
- 但是time这个东西本身是一个 `int` ，这使得他的上限为 $2^{31}-1$， 也就是2038年1月19日03:14:07（UTC）后，这个值将会溢出，所以许多现代系统通过将int改为double解决了这个问题，使溢出的时间来到了2920亿年后

## Nested rand

如果用 **`srand(rand())`** 替代 **`srand(time(NULL))`**，是否会让种子变得随机？
- 如果调用 `srand(rand())`，`rand()` 的结果依赖于之前的种子。
- 如果没有明确设置种子，`rand()` 使用默认种子（通常是 1）。
- 这意味着每次运行程序时，`rand()` 的第一个结果是固定的，例如可能是 `16807`。
- 因此，`srand(rand())` 实际上等效于设置一个固定的种子（例如 `16807`）

## 2.5.3. Random numbers within a range

- 默认情况下，`rand()` 生成的伪随机数范围是从 `0` 到 `RAND_MAX`，其中 `RAND_MAX` 是一个常量
- 如果需要生成一个更小范围内的随机数（例如 `0` 和 `1` 之间的随机数），可以结合取模运算符 `%` 使用
- 不像其他语言可以更改这个上线，C语言采取的是取模的办法生成指定范围内的随机数
- 如果要生成 `0` 到 `5` 的随机数，有

``` c
int random_number = rand() % 6; // 结果范围是 [0, 5]
```

- 这是因为观察取模操作，他的输出将会是

``` c
0 % 5 = 0
1 % 5 = 1
2 % 5 = 2
3 % 5 = 3
4 % 5 = 4
5 % 5 = 0 (循环重复)
```

- 那么如果范围是1到6，则是

``` c
int random_number = (rand() % 6) + 1; // 结果范围是 [1, 6]
```

- 总结得出，要生成一个范围在 `[MIN, MAX]`（包括上下限）的随机数，可以使用公式

```c
int random_number = rand() % (MAX - MIN + 1) + MIN;
```

