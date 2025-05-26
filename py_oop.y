%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int class_found = 0;
int instantiation_found = 0;
int self_method_found = 0;

void yyerror(const char *s) {
    // suppress all syntax errors
}
int yylex(void);
%}

%token CLASS ASSIGN LPAREN RPAREN COLON EOL INVALID DEF COMMA SELF

%union {
    char* str;
}
%token <str> IDENTIFIER CLASS_NAME

%%

program:
    stmts
    ;

stmts:
      stmts stmt
    | stmt
    ;

stmt:
      class_def
    | method_self
    | instantiation
    | stray_line EOL
    | error EOL { yyerrok; }
    | EOL
    ;

class_def:
    CLASS CLASS_NAME COLON EOL {
        printf("[Parser] Found class definition: %s\n", $2);
        class_found = 1;
    }
    |CLASS CLASS_NAME LPAREN CLASS_NAME RPAREN COLON EOL
    ;

instantiation:
    IDENTIFIER ASSIGN CLASS_NAME LPAREN RPAREN EOL {
        printf("[Parser] Found instantiation: %s = %s()\n", $1, $3);
        instantiation_found = 1;
    }
    ;
method_self:
    DEF IDENTIFIER LPAREN arg_list RPAREN COLON EOL{
        printf("[Parser] Found method self");
        self_method_found=1;
    };

arg_list:
    SELF
    | SELF COMMA arg_rest;

arg_rest:
      IDENTIFIER
    | arg_rest COMMA IDENTIFIER
    ;
stray_line:
      tokens
    ;

tokens:
      tokens token
    | token
    ;

token:
      IDENTIFIER
    | CLASS_NAME
    | ASSIGN
    | LPAREN
    | RPAREN
    | COLON
    | INVALID
    ;

%%

int main(void) {
    yyparse();

    printf("\n[Result] Detection Summary:\n");
    printf("  Class Found: %s\n", class_found ? "YES" : "NO");
    printf("  Instantiation Found: %s\n", instantiation_found ? "YES" : "NO");
    printf("  Method with self Found: %s\n", self_method_found ? "YES" : "NO");

    if (class_found) {
        printf("✅ Code uses object-oriented programming.\n");
    } else {
        printf("⚠️ Not enough OOP patterns detected.\n");
    }

    return 0;
}
