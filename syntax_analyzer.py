# The logic for the syntax analyzer is removing a token from the list of lexemes if there's no error until it is empty.

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens  # List of tokens

        # Define the classes of tokens.
        self.arithmetic_class = ["EXPR_SUM", "EXPR_DIFF", "EXPR_PRODUKT", "EXPR_QUOSHUNT", "EXPR_MOD", "EXPR_BIGGR", "EXPR_SMALLR"]
        self.literal_class = ["VARIABLE_IDENTIFIER", "NUMBR_LITERAL", "NUMBAR_LITERAL", "TROOF_LITERAL", "YARN_LITERAL"]

    def program_start(self):
        # Check for "HAI" at the start of the program
        if self.syntax("CODE_DELIMITER", "HAI"):
            self.tokens.pop(0)  # Remove the "HAI" token
        else:
            self.call_error("CODE_DELIMITER", "HAI")
        
        # Process other tokens until the end or "KTHXBYE"
        while self.tokens:
            # After the program starts, we can have variable declarations.
            self.variable_declaration()

            # Check if print statement.
            if self.syntax("OUTPUT_KEYWORD", "VISIBLE"):
                self.output_syntax()
            # Check if assignment statement.
            elif self.syntax("VARIABLE_IDENTIFIER", self.tokens[0][1]):
                self.assignment_syntax()
            # Check if input statement.
                self.input_syntax()
            # Check if arithmetic expression.
            elif self.tokens[0][0] in self.arithmetic_class:
                self.arithmetic_expression()
            # Check if control flow.
            elif self.tokens[0][0] in ["IF_START", "SWITCH_START", "LOOP_START"]:
                self.control_flow_syntax()
            # Check if function definition.
            elif self.syntax("FUNCTION_DEF", "HOW IZ I"):
                self.function_definition()
            # Check if comparison.
            elif self.syntax("COMPARE_EQUALS", "BOTH SAEM") or self.syntax("COMPARE_DIFF", "DIFFRINT"):
                self.comparison_syntax()
            # Check for function call.
            elif self.syntax("FUNCTION_CALL", "I IZ"):
                self.function_call_syntax()
            # Check for loop.
            elif self.syntax("LOOP_START", "IM IN YR"):
                self.loop_syntax()
            # Check for the end of the program
            if self.syntax("CODE_DELIMITER", "KTHXBYE"):
                self.tokens.pop(0)
                return self.get_analysis_result()
        
        return self.get_analysis_result()


    def syntax(self, classification, value):
        if not self.tokens:
            self.call_error("Unexpected end of input", "")

        # Directly get the first token from the list
        token_class, token_value = self.tokens[0]

        # Check if the current token matches the expected type and value
        if token_class == classification and (token_value == value):
            return True

        # Return False instead of calling error immediately
        return False


    def variable_declaration(self):
        # Check if we encounter "WAZZUP" as a declaration start (this could be another keyword)
        if self.syntax("DECLARATION_START", "WAZZUP"):
            self.tokens.pop(0)
            # Get the variable identifier after "WAZZUP"
            while self.tokens[0] != ("DECLARATION_END", "BUHBYE"):
                # Look for variable declarations inside the block
                if self.syntax("VARIABLE_DECLARATION", "I HAS A"):
                    self.tokens.pop(0)
                    if self.syntax("VARIABLE_IDENTIFIER", self.tokens[0][1]):
                        self.tokens.pop(0)
                        if self.syntax("VARIABLE_ASSIGNMENT", "ITZ"):
                            self.tokens.pop(0)
                            # Handle the yarn literal.
                            if self.syntax('STRING_DELIMITER', '"'):
                                self.tokens.pop(0)
                                self.tokens.pop(0) # Remove the yarn literal.
                                if self.syntax('STRING_DELIMITER','"'):
                                    self.tokens.pop(0)
                                else:
                                    self.call_error("STRING_DELIMITER", '"')
                            # Handle other literal type.
                            elif self.tokens[0][0] in ["NUMBR_LITERAL", "NUMBAR_LITERAL", "TROOF_LITERAL", "TYPE_LITERAL"]:
                                self.tokens.pop(0)
                            # Handle the case where the value is an arithmetic expression.
                            elif self.tokens[0][0] in self.arithmetic_class:
                                self.tokens.pop(0)
                                self.arithmetic_expression()
                else:
                    # Handle the case where neither "BUHBYE" was not found but next token is not a declaration.
                    self.call_error("DECLARATION_END", "BUHBYE")

            self.tokens.pop(0)  # Remove the "BUHBYE" token
            return

    #IMPLEMENT NESTED OPERATIONS.
    def arithmetic_expression(self):
        '''
        The token for arithmetic expression is already removed. Check for the first operand.
        '''
        if self.tokens[0][0] in ["NUMBR_LITERAL", "NUMBAR_LITERAL", "VARIABLE_IDENTIFIER"]:
            self.tokens.pop(0)
            while self.tokens and self.syntax("OPERATOR_SEPARATOR", "AN"):
                self.tokens.pop(0)  # Pop the "AN" operator
                if self.tokens[0][0] in ["NUMBR_LITERAL", "NUMBAR_LITERAL", "VARIABLE_IDENTIFIER"]:
                    self.tokens.pop(0)  # Pop the next operand
                else:
                    self.call_error("NUMBR_LITERAL or NUMBAR_LITERAL", self.tokens[0][1])
        else:
            self.call_error("NUMBR_LITERAL or NUMBAR_LITERAL", self.tokens[0][1])

                

    def call_error(self, classification, value):
        error = f"Syntax Error: Expected {classification}: '{value}'"
        print(error)

    def get_analysis_result(self):
        if self.tokens == []:
            return("Program successfully parsed.")
        else:
            return("Syntax Error: Unexpected end of input")
