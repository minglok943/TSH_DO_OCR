


def genRegex(text):
    
    rePattern = ''
    temp = text
    
    first_digit = False

    for char in temp:
        if char == ' ':
            rePattern += '\s*'
        elif char == 'a' or char == 'A':
            rePattern += '[a,A]*'
        elif char == 'b' or char == 'B':
            rePattern += '[b,B]*'
        elif char == 'c' or char == 'C':
            rePattern += '[c,C]*'
        elif char == 'd' or char == 'D':
            rePattern += '[d,D]*'
        elif char == 'e' or char == 'E':
            rePattern += '[e,E]*'
        elif char == 'f' or char == 'F':
            rePattern += '[f,F]*'
        elif char == 'g' or char == 'G':
            rePattern += '[g,G]*'
        elif char == 'h' or char == 'H':
            rePattern += '[h,H]*'
        elif char == 'j' or char == 'J':
            rePattern += '[j,J]*'
        elif char == 'l' or char == 'L':
            rePattern += '[l,L]*'
        elif char == 'm' or char == 'M':
            rePattern += '[m,M]*'
        elif char == 'n' or char == 'N':
            rePattern += '[n,N]*'
        elif char == 'q' or char == 'Q':
            rePattern += '[q,Q]*'
        elif char == 's' or char == 'S':
            rePattern += '[s,S]*'
        elif char == 't' or char == 'T':
            rePattern += '[t,T]*'
        elif char == 'u' or char == 'U':
            rePattern += '[u,U]*'
        elif char == 'v' or char == 'V':
            rePattern += '[v,V]*'
        elif char == 'w' or char == 'W':
            rePattern += '[w,W]*'
        elif char == 'x' or char == 'X':
            rePattern += '[x,X]*'
        elif char == 'y' or char == 'Y':
            rePattern += '[y,Y]*'
        elif char == 'z' or char == 'Z':
            rePattern += '[z,Z]*'
        elif char == 'I' or char == '/' or char == '1' or char == '\\' or char == '!' or char == 'i':
            rePattern += '[1,I,\/,\\\\,!,i]*'
        elif char == '-':
            rePattern += '-*'
        elif char == ',' or char == '.':
            rePattern += '[.,\,]*'
        elif char == '(':
            rePattern += '\('
        elif char == ')':
            rePattern += '\)'
        elif char == 'O' or char == 0 or char == 'o':
            rePattern += '[0,O,o]'
        elif char == 'R' or char == 'P' or char == 'K' or char =='p' or char =='r' or char =='k':
            rePattern += '[R,P,K,r,p,k]*'
        elif char == ':' or char == ';' or char == '+':
            rePattern += '[:,;,+]*'
        elif char == '\'':
            #rePattern += '\\\''
            rePattern += "'"
        else:
            rePattern += char
            rePattern += '*'

    return rePattern

def genRegexWithNum(text):

    rePattern = ''
    temp = text
    
    first_digit = False
    broken = False
    digit_end = True
    digit_count = 0
    for index, char in enumerate(temp):
        if ord(char) >= 48 and ord(char) <= 57:
            if first_digit == False:
                first_digit = True
                digit_count = 1
                if broken == True:
                    rePattern += '\d{'
                else:
                    rePattern += '(\d{'
            else:
                digit_count += 1
            if index == len(temp)-1:
                rePattern += str(digit_count)
                rePattern += '})'
        else:
            if first_digit == True:
                rePattern += str(digit_count)
                rePattern += '}'
                first_digit = False
                broken = True
                digit_count = 0

            if char == ' ':
                rePattern += '\s*'
            elif char == 'a' or char == 'A':
                rePattern += '[a,A]'
            elif char == 'b' or char == 'B':
                rePattern += '[b,B]'
            elif char == 'c' or char == 'C':
                rePattern += '[c,C]'
            elif char == 'd' or char == 'D':
                rePattern += '[d,D]'
            elif char == 'e' or char == 'E':
                rePattern += '[e,E]'
            elif char == 'f' or char == 'F':
                rePattern += '[f,F]'
            elif char == 'g' or char == 'G':
                rePattern += '[g,G]'
            elif char == 'h' or char == 'H':
                rePattern += '[h,H]'
            elif char == 'j' or char == 'J':
                rePattern += '[j,J]'
            elif char == 'l' or char == 'L':
                rePattern += '[l,L]'
            elif char == 'm' or char == 'M':
                rePattern += '[m,M]'
            elif char == 'n' or char == 'N':
                rePattern += '[n,N]'
            elif char == 'q' or char == 'Q':
                rePattern += '[q,Q]'
            elif char == 's' or char == 'S':
                rePattern += '[s,S]'
            elif char == 't' or char == 'T':
                rePattern += '[t,T]'
            elif char == 'u' or char == 'U':
                rePattern += '[u,U]'
            elif char == 'v' or char == 'V':
                rePattern += '[v,V]'
            elif char == 'w' or char == 'W':
                rePattern += '[w,W]'
            elif char == 'x' or char == 'X':
                rePattern += '[x,X]'
            elif char == 'y' or char == 'Y':
                rePattern += '[y,Y]'
            elif char == 'z' or char == 'Z':
                rePattern += '[z,Z]'
            elif char == 'I' or char == '/' or char == '\\' or char == '!' or char == 'i':
                rePattern += '[1,I,\/,\\,!,i]'
            elif char == '-':
                rePattern += '-*'
            elif char == ',' or char == '.':
                rePattern += '[.,\,]'
            elif char == '(':
                rePattern += '\('
            elif char == ')':
                rePattern += '\)'
            elif char == 'O' or char == 'o':
                rePattern += '[0,O,o]'
            elif char == 'R' or char == 'P' or char == 'K' or char =='p' or char =='r' or char =='k':
                rePattern += '[R,P,K,r,p,k]'
            elif char == ':' or char == ';' or char == '+':
                rePattern += '[:,;,+]*'
            else:
                rePattern += char
                rePattern += '*'

    return rePattern

def genRegexCapitalInsensitive(text):
# capital insensitive     
    rePattern = ''
    temp = text
    
    first_digit = False

    for char in temp:
        if char == ' ':
            rePattern += '\s*'
        elif char == 'a' or char == 'A':
            rePattern += '[a,A]*'
        elif char == 'b' or char == 'B':
            rePattern += '[b,B]*'
        elif char == 'c' or char == 'C':
            rePattern += '[c,C]*'
        elif char == 'd' or char == 'D':
            rePattern += '[d,D]*'
        elif char == 'e' or char == 'E':
            rePattern += '[e,E]*'
        elif char == 'f' or char == 'F':
            rePattern += '[f,F]*'
        elif char == 'g' or char == 'G':
            rePattern += '[g,G]*'
        elif char == 'h' or char == 'H':
            rePattern += '[h,H]*'
        elif char == 'i' or char == 'I':
            rePattern += '[i,I]*'
        elif char == 'j' or char == 'J':
            rePattern += '[j,J]*'
        elif char == 'k' or char == 'K':
            rePattern += '[k,K]*'
        elif char == 'l' or char == 'L':
            rePattern += '[l,L]*'
        elif char == 'm' or char == 'M':
            rePattern += '[m,M]*'
        elif char == 'n' or char == 'N':
            rePattern += '[n,N]*'
        elif char == 'o' or char == 'O':
            rePattern += '[o,O]*'
        elif char == 'p' or char == 'P':
            rePattern += '[p,P]*'
        elif char == 'q' or char == 'Q':
            rePattern += '[q,Q]*'
        elif char == 'r' or char == 'R':
            rePattern += '[r,R]*'
        elif char == 's' or char == 'S':
            rePattern += '[s,S]*'
        elif char == 't' or char == 'T':
            rePattern += '[t,T]*'
        elif char == 'u' or char == 'U':
            rePattern += '[u,U]*'
        elif char == 'v' or char == 'V':
            rePattern += '[v,V]*'
        elif char == 'w' or char == 'W':
            rePattern += '[w,W]*'
        elif char == 'x' or char == 'X':
            rePattern += '[x,X]*'
        elif char == 'y' or char == 'Y':
            rePattern += '[y,Y]*'
        elif char == 'z' or char == 'Z':
            rePattern += '[z,Z]*'
        elif char == '-':
            rePattern += '-'
        elif char == '(':
            rePattern += '\('
        elif char == ')':
            rePattern += '\)'
        elif char == '\'':
            rePattern += '\\\''
        elif char == '/':
            rePattern += '\/'
        elif char == '\\':
            rePattern += '\\\\'
        else:
            rePattern += char
            if (ord(char) >= 48 and ord(char) <= 57)!=True:
                rePattern += '*'

    return rePattern

def genRegexYaml(text):
    
    rePattern = ''
    temp = text
    
    first_digit = False

    for char in temp:
        if char == ' ':
            rePattern += '\s*'
        elif char == 'a' or char == 'A':
            rePattern += '[a,A]'
        elif char == 'b' or char == 'B':
            rePattern += '[b,B]'
        elif char == 'c' or char == 'C':
            rePattern += '[c,C]'
        elif char == 'd' or char == 'D':
            rePattern += '[d,D]'
        elif char == 'e' or char == 'E':
            rePattern += '[e,E]'
        elif char == 'f' or char == 'F':
            rePattern += '[f,F]'
        elif char == 'g' or char == 'G':
            rePattern += '[g,G]'
        elif char == 'h' or char == 'H':
            rePattern += '[h,H]'
        elif char == 'j' or char == 'J':
            rePattern += '[j,J]'
        elif char == 'l' or char == 'L':
            rePattern += '[l,L]'
        elif char == 'm' or char == 'M':
            rePattern += '[m,M]'
        elif char == 'n' or char == 'N':
            rePattern += '[n,N]'
        elif char == 'q' or char == 'Q':
            rePattern += '[q,Q]'
        elif char == 's' or char == 'S':
            rePattern += '[s,S]'
        elif char == 't' or char == 'T':
            rePattern += '[t,T]'
        elif char == 'u' or char == 'U':
            rePattern += '[u,U]'
        elif char == 'v' or char == 'V':
            rePattern += '[v,V]'
        elif char == 'w' or char == 'W':
            rePattern += '[w,W]'
        elif char == 'x' or char == 'X':
            rePattern += '[x,X]'
        elif char == 'y' or char == 'Y':
            rePattern += '[y,Y]'
        elif char == 'z' or char == 'Z':
            rePattern += '[z,Z]'
        elif char == 'I' or char == '/' or char == '1' or char == '\\' or char == '!' or char == 'i':
            rePattern += '[1,I,\/,\\\\,!,i]*'
        elif char == '-':
            rePattern += '-*'
        elif char == ',' or char == '.':
            rePattern += '[.,\,]*'
        elif char == '(':
            rePattern += '\('
        elif char == ')':
            rePattern += '\)'
        elif char == 'O' or char == 0 or char == 'o':
            rePattern += '[0,O,o]'
        elif char == 'R' or char == 'P' or char == 'K' or char =='p' or char =='r' or char =='k':
            rePattern += '[R,P,K,r,p,k]*'
        elif char == ':' or char == ';' or char == '+':
            rePattern += '[:,;,+]*'
        elif char == "'":
            rePattern += "''"
        else:
            rePattern += char
            rePattern += '*'

    return rePattern

def genRegexCapitalInsensitiveAccurate(text):
# capital insensitive     
    rePattern = ''
    temp = text
    
    first_digit = False

    for char in temp:
        if char == ' ':
            rePattern += '\s*'
        elif char == 'a' or char == 'A':
            rePattern += '[a,A]'
        elif char == 'b' or char == 'B':
            rePattern += '[b,B]'
        elif char == 'c' or char == 'C':
            rePattern += '[c,C]'
        elif char == 'd' or char == 'D':
            rePattern += '[d,D]'
        elif char == 'e' or char == 'E':
            rePattern += '[e,E]'
        elif char == 'f' or char == 'F':
            rePattern += '[f,F]'
        elif char == 'g' or char == 'G':
            rePattern += '[g,G]'
        elif char == 'h' or char == 'H':
            rePattern += '[h,H]'
        elif char == 'i' or char == 'I':
            rePattern += '[i,I]'
        elif char == 'j' or char == 'J':
            rePattern += '[j,J]'
        elif char == 'k' or char == 'K':
            rePattern += '[k,K]'
        elif char == 'l' or char == 'L':
            rePattern += '[l,L]'
        elif char == 'm' or char == 'M':
            rePattern += '[m,M]'
        elif char == 'n' or char == 'N':
            rePattern += '[n,N]'
        elif char == 'o' or char == 'O':
            rePattern += '[o,O]'
        elif char == 'p' or char == 'P':
            rePattern += '[p,P]'
        elif char == 'q' or char == 'Q':
            rePattern += '[q,Q]'
        elif char == 'r' or char == 'R':
            rePattern += '[r,R]'
        elif char == 's' or char == 'S':
            rePattern += '[s,S]'
        elif char == 't' or char == 'T':
            rePattern += '[t,T]'
        elif char == 'u' or char == 'U':
            rePattern += '[u,U]'
        elif char == 'v' or char == 'V':
            rePattern += '[v,V]'
        elif char == 'w' or char == 'W':
            rePattern += '[w,W]'
        elif char == 'x' or char == 'X':
            rePattern += '[x,X]'
        elif char == 'y' or char == 'Y':
            rePattern += '[y,Y]'
        elif char == 'z' or char == 'Z':
            rePattern += '[z,Z]'
        elif char == '-':
            rePattern += '-'
        elif char == '(':
            rePattern += '\('
        elif char == ')':
            rePattern += '\)'
        elif char == '\'':
            rePattern += '\\\''
        elif char == '/':
            rePattern += '\/'
        elif char == '\\':
            rePattern += '\\\\'
        else:
            rePattern += char
            if (ord(char) >= 48 and ord(char) <= 57)!=True:
                rePattern += '*'

    return rePattern
