# notes

* typescript 是js的超级； typescript一般需要编译成js才能被浏览器使用，除非typescript文件中使用的都是js语法；
* 

# install

* npm install -g typescript

# 编译

* tsc.cmd test.ts

# 语法

## 模块

* 模块在其自身的作用域里执行，而不是在全局作用域里;这意味着定义在一个模块里的变量，函数，类等等在模块外部是不可见的，除非你明确地使用export形式之一导出它们。
* 相反，如果想使用其它模块导出的变量，函数，类，接口等的时候，你必须要导入它们，可以使用 import形式之一。
* 模块是自声明的；两个模块之间的关系是通过在文件级别上使用imports和exports建立的。

## 函数

* javascript 函数

```js
  // Named function
function add(x, y) {
    return x + y;
}

// Anonymous function
let myAdd = function(x, y) { return x + y; };
```

* 可选参数和默认参数
* 
```js
function buildName(firstName: string, lastName: string) {
    return firstName + " " + lastName;
}

let result1 = buildName("Bob");                  // error, too few parameters
let result2 = buildName("Bob", "Adams", "Sr.");  // error, too many parameters
let result3 = buildName("Bob", "Adams");         // ah, just right

function buildName(firstName: string, lastName?: string) {
    if (lastName)
        return firstName + " " + lastName;
    else
        return firstName;
}

let result1 = buildName("Bob");  // works correctly now
let result2 = buildName("Bob", "Adams", "Sr.");  // error, too many parameters
let result3 = buildName("Bob", "Adams");  // ah, just right
```

* 