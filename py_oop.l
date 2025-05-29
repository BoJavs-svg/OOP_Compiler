%{
#include "py_oop.tab.h"
#include <string.h>
#include <stdlib.h>

int line = 1;
%}

%option noyywrap

%%
[ \t]+                 ;  // Skip whitespace (space or tab)

\r\n                   { line++; return EOL; }  // Windows newline
\n                     { line++; return EOL; }  // Unix newline

"class"                return CLASS;
"def"                  return DEF;
"self"                 {printf("Found self\n");return SELF;}

"="                    return ASSIGN;
":"                    return COLON;
","                    return COMMA;
"("                    return LPAREN;
")"                    return RPAREN;

[a-z_][a-zA-Z0-9_]*   { yylval.str = strdup(yytext); return IDENTIFIER; }
[A-Z][a-zA-Z0-9_]*    { yylval.str = strdup(yytext); printf("Identifier '%s'\n",yytext);return CLASS_NAME; }

.                      {
                          fprintf(stderr, "Line %d: Invalid character '%s'\n", line, yytext);
                          return INVALID;
                      }

%%
