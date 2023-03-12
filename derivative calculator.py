# -*- coding: utf-8 -*-
"""

Symbolic differentiation of prefix expressions
This code calculates derivatives in prefix notation
This code only accepts strings of expressions in prefix notation with proper spacing and nested parenthesis indicating the order of operations
Expression operators, functions and arguments must all be lowercase
The expressions must have balanced parentesis and with spaces between list items
Expressions are single variable expressions using x as the variable
This code calculates the correct derivative but does not simplify the result
This code is built to manage any combination of these operators and functions (+ - * / ^ cos sin tan exp ln)
Examples
5(x+3) -> ('(* (+ x 3) 5)') returns 5
5cos(x^2) -> ('(* 5 (cos (^ x 2)))') returns (* 5 (* (* 2 x) (* -1 (sin (^ x 2))))) -> -10sin(x^2)
"""


def main():
    expression = input("Enter the expression of x here in prefix notation: ")
    print(diff(expression))
    
    

def parse_f(s):
    op = s[1]
    if op in ("+", "-", "*", "/", "^"):
        p = -1
        sep = []
        for i in range(len(s)):
            if s[i] == "(":
                p += 1
            if s[i] == ")":
                p -= 1
            if s[i] == " " and p == 0:
                sep.append(i)
        arg1 = s[sep[0]+1: sep[1]]
        arg2 = s[sep[1]+1: -1]
        return[op, arg1, arg2]
    else:
        for i in range(len(s)):
            if s[i] == " ":
                arg = s[i+1: -1]
                return [op, arg]
            elif i>1:
                op = op + s[i]
               

def type_f(arg):
    if "(" in arg:
        return "ex"
    if arg.isnumeric():
        return "nm"
    else:
        return "vr"
       
   
def addition(tup):
    for i in range(len(tup)):
        if type_f(tup[i]) == "ex":
            tup[i] = diff(tup[i])
        elif type_f(tup[i]) == "nm":
            tup[i] = "0"
        elif type_f(tup[i]) == "vr":
            tup[i] = "1"
    return "(+ " + tup[0] + " " + tup[1] + ")"
   
def subtraction(tup):
    for i in range(len(tup)):
        if type_f(tup[i]) == "ex":
            tup[i] = diff(tup[i])
        elif type_f(tup[i]) == "nm":
            tup[i] = "0"
        elif type_f(tup[i]) == "vr":
            tup[i] = "1"
    return "(- " + tup[0] + " " + tup[1] + ")"
   
def cosine(tup):
    if type_f(tup[0]) == "vr":
        return "(* -1 (sin " + tup[0] + "))"
    elif type_f(tup[0]) == "nm":
        return "0"
    else:
        return "(* " + diff(tup[0]) + " (* -1 (sin " + tup[0] + ")))"
def sine(tup):
    if type_f(tup[0]) == "vr":
        return "(cos " + tup[0] + ")"
    elif type_f(tup[0]) == "nm":
        return "0"
    else:
        return "(* " + diff(tup[0]) + " (cos " + tup[0] + "))"
def tangent(tup):
    if type_f(tup[0]) == "vr":
        return "(/ 1 (^ (cos " + tup[0] + ") 2))"
    elif type_f(tup[0]) == "nm":
        return "0"
    else:
        return "(* " + diff(tup[0]) + " (^ (cos " + tup[0] + ") -2))"
       
def nat_log(tup):
    if type_f(tup[0]) == "vr":
        return "(/ 1 " + tup[0] + ")"
    elif type_f(tup[0]) == "nm":
        return "0"
    else:
        return "(/ " + diff(tup[0]) + " " + tup[0] + ")"
def e_to_the(tup):
    if type_f(tup[0]) == "vr":
        return "(exp " + tup[0] + ")"
    elif type_f(tup[0]) == "nm":
        return "0"
    else:
        return "(* " + diff(tup[0]) + " (exp " + tup[0] + "))"
def multiplication(tup):
    if type_f(tup[0]) == "ex" and type_f(tup[1]) == "ex":
        return "(+ (* " + tup[0] + " " + diff(tup[1]) + ") (* " + diff(tup[0]) + " " + tup[1] + "))"
    if type_f(tup[0]) == "nm" and type_f(tup[1]) == "vr":
        return tup[0]
    if type_f(tup[0]) == "vr" and type_f(tup[1]) == "nm":
        return tup[1]
    if type_f(tup[0]) == "nm" and type_f(tup[1]) == "nm":
        return "0"
    if type_f(tup[0]) == "vr" and type_f(tup[1]) == "vr":
        return "(* 2 " + tup[0] + ")"
    if type_f(tup[0]) == "ex" and type_f(tup[1]) == "nm":
        return "(* " + tup[1] + " " + diff(tup[0]) + ")"
    if type_f(tup[0]) == "nm" and type_f(tup[1]) == "ex":
        return "(* " + tup[0] + " " + diff(tup[1]) + ")"
    if type_f(tup[0]) == "ex" and type_f(tup[1]) == "vr":
        return "(+ " + tup[0] + " (* " + tup[1] + " " + diff(tup[0]) + "))"
    if type_f(tup[0]) == "vr" and type_f(tup[1]) == "ex":
            return "(+ " + tup[1] + " (* " + tup[0] + " " + diff(tup[1]) + "))"
           
def quotient(tup):
    return "(/ (- (* " + diff(tup[0]) + " " + tup[1] + ") (* " + diff(tup[1]) + " " + tup[0] + ")) (^ " + tup[1] + " 2))"
       
def power(tup):
    if type_f(tup[0]) == "vr" and type_f(tup[1]) == "nm":
        return "(* " + tup[1] + " (^ " + tup[0] + " " + dec(tup[1]) + "))"
    else:
        print("(exp (* " + tup[1] + "(ln " + tup[0] + ")))")
        return diff("(exp (* " + tup[1] + " (ln " + tup[0] + ")))")
def dec(s):
    i = int(s)
    i -= 1
    s = str(i)
    return s
   
def comb(s):
    open_p = []
    close_p = []
    combos = []
    for i in range(len(s)):
        if s[i] == "(":
            open_p.append(i)
        elif s[i] == ")":
            close_p.append(i)
    open_p.reverse()
    for o in open_p:
        for c in close_p:
            if c > o:
                combos.append((o, c))
                close_p.remove(c)
                break
    return combos

def simplify(s):
    combos = comb(s)
    temp_s = s + " "
    for c in combos:
        t = parse_f(temp_s[c[0]: c[1]+1])
        if t[0] == "+":
            if type_f(t[1]) == "nm" and type_f(t[2]) == "nm":
                v = int(t[1]) + int(t[2])
                new_s = temp_s[:c[0]] + str(v) + temp_s[c[1]+1:-1]
                return simplify(new_s)
        if t[0] == "*":
            if type_f(t[1]) == "nm" and type_f(t[2]) == "nm":
                v = int(t[1]) * int(t[2])
                new_s = temp_s[:c[0]] + str(v) + temp_s[c[1]+1:-1]
                return simplify(new_s)
            if t[1] == "0" or t[2] == "0":
                new_s = temp_s[:c[0]] + "0" + temp_s[c[1]+1:-1]
                return simplify(new_s)
            if t[1] == "1":
                new_s = temp_s[:c[0]] + t[2] + temp_s[c[1]+1:-1]
                return simplify(new_s)
            elif t[2] == "1":
                new_s = temp_s[:c[0]] + t[1] + temp_s[c[1]+1:-1]
                return simplify(new_s)
        if t[0] == "-":
            if type_f(t[1]) == "nm" and type_f(t[2]) == "nm":
                v = int(t[1]) - int(t[2])
                new_s = temp_s[:c[0]] + str(v) + temp_s[c[1]+1:-1]
                return simplify(new_s)
        if t[0] == "^":
            if type_f(t[1]) == "vr" and t[2] == "1":
                new_s = temp_s[:c[0]] + t[1] + temp_s[c[1]+1:-1]
                return simplify(new_s)
            if t[2] == "0":
                new_s = temp_s[:c[0]] + "1" + temp_s[c[1]+1:-1]
                return simplify(new_s)
            if type_f(t[1]) == "nm" and type_f(t[2]) == "nm":
                v = int(t[1]) ** int(t[2])
                new_s = temp_s[:c[0]] + str(v) + temp_s[c[1]+1:-1]
                return simplify(new_s)
        if t[0] == "/":
             if type_f(t[1]) == "nm" and type_f(t[2]) == "nm":
                v = int(t[1]) / int(t[2])
                new_s = temp_s[:c[0]] + str(v) + temp_s[c[1]+1:-1]
                return simplify(new_s)           
    return s
       
       

def diff(s):
    if s.isnumeric():
        return "0"
    elif len(s) == 1:
        return "1"
    tup = parse_f(s)
    # All 10 functions
    if tup[0] == "+":
        s = addition(tup[1:])
    if tup[0] == "-":
        s = subtraction(tup[1:])
    if tup[0] == "cos":
        s = cosine(tup[1:])
    if tup[0] == "sin":
        s = sine(tup[1:])
    if tup[0] == "tan":
        s = tangent(tup[1:])
    if tup[0] == "ln":
        s = nat_log(tup[1:])
    if tup[0] == "exp":
        s = e_to_the(tup[1:])
    if tup[0] == "*":
        s = multiplication(tup[1:])
    if tup[0] == "/":
        s = quotient(tup[1:])
    if tup[0] == "^":
        s = power(tup[1:])
    new_s = simplify(s)
    while new_s != s:
        s = new_s
        new_s = simplify(s)
    return new_s




if __name__=="__main__":
    main()