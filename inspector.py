import ast
import sys
import traceback
import time
import io
import contextlib
import inspect
import re
from typing import Any, Dict, List, Optional, Type

class AdvancedErrorHandler:
    """
    Comprehensive error handling and classification system
    """
    ERROR_TYPES = {
        # Comprehensive dictionary of Python built-in errors
        'SyntaxError': {
            'category': 'Syntax',
            'severity': 'critical',
            'general_advice': 'Check code syntax, indentation, and language-specific constructs.'
        },
        'IndentationError': {
            'category': 'Syntax',
            'severity': 'critical',
            'general_advice': 'Ensure consistent indentation. Use spaces or tabs consistently.'
        },
        'TypeError': {
            'category': 'Type Mismatch',
            'severity': 'high',
            'general_advice': 'Verify type compatibility and type conversions.'
        },
        'ValueError': {
            'category': 'Value Error',
            'severity': 'high', 
            'general_advice': 'Check input values and their constraints.'
        },
        'NameError': {
            'category': 'Reference',
            'severity': 'high',
            'general_advice': 'Ensure all variables are defined before use.'
        },
        'AttributeError': {
            'category': 'Attribute',
            'severity': 'medium',
            'general_advice': 'Verify object attributes and method calls.'
        },
        'IndexError': {
            'category': 'Indexing',
            'severity': 'high',
            'general_advice': 'Check array/list indexing and bounds.'
        },
        'KeyError': {
            'category': 'Dictionary',
            'severity': 'high',
            'general_advice': 'Verify dictionary key existence before access.'
        },
        'ZeroDivisionError': {
            'category': 'Arithmetic',
            'severity': 'high',
            'general_advice': 'Add checks to prevent division by zero.'
        },
        'FileNotFoundError': {
            'category': 'File System',
            'severity': 'high',
            'general_advice': 'Verify file paths and permissions.'
        },
        'MemoryError': {
            'category': 'Resource',
            'severity': 'critical',
            'general_advice': 'Optimize memory usage, handle large data more efficiently.'
        }
    }

    @classmethod
    def classify_error(cls, error: Exception) -> Dict[str, Any]:
        """
        Classify and provide detailed information about an error
        
        :param error: Exception instance
        :return: Detailed error classification
        """
        error_type = type(error).__name__
        error_info = cls.ERROR_TYPES.get(error_type, {
            'category': 'Unknown',
            'severity': 'low',
            'general_advice': 'Unexpected error occurred.'
        })

        # Enhanced error details
        return {
            'type': error_type,
            'message': str(error),
            'category': error_info['category'],
            'severity': error_info['severity'],
            'general_advice': error_info['general_advice'],
            'traceback': traceback.format_exc()
        }

class CodeInspector:
    def __init__(self, verbose: bool = False):
        """
        Advanced Code Inspector with comprehensive error handling
        
        :param verbose: Enable detailed logging
        """
        self.verbose = verbose
        self.error_handler = AdvancedErrorHandler()
    
    def static_analysis(self, code: str) -> Dict[str, Any]:
        """
        Perform static code analysis using AST parsing.
        
        :param code: Source code to analyze
        :return: Dictionary of static analysis findings
        """
        try:
            tree = ast.parse(code)
            
            # Collect static analysis insights
            analysis_results = {
                'syntax_valid': True,
                'function_count': len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
                'class_count': len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
                'import_count': len([node for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]),
                'complexity_score': self._calculate_complexity(tree)
            }
            
            return analysis_results
        
        except SyntaxError as e:
            return {
                'syntax_valid': False,
                'syntax_error': {
                    'message': str(e),
                    'line': e.lineno,
                    'offset': e.offset
                }
            }
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """
        Calculate cyclomatic complexity of the code.
        
        :param tree: Abstract Syntax Tree
        :return: Complexity score
        """
        complexity = 1  # Base complexity
        
        # Increment complexity for control flow statements
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.ExceptHandler, 
                                  ast.AsyncFor, ast.AsyncWith, ast.Match)):
                complexity += 1
            
            # Additional complexity for boolean operations
            if isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def runtime_execution(self, code: str, timeout: float = 5.0) -> Dict[str, Any]:
        """
        Execute code with runtime tracking and error capturing.
        
        :param code: Source code to execute
        :param timeout: Maximum execution time in seconds
        :return: Dictionary with execution details
        """
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        start_time = time.time()
        execution_result = {
            'success': False,
            'output': None,
            'runtime': None,
            'error': None
        }
        
        try:
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):
                
                # Set up execution context
                local_vars = {}
                
                # Execute the code
                exec(code, {}, local_vars)
                
                # Capture execution time
                execution_time = time.time() - start_time
                
                execution_result.update({
                    'success': True,
                    'output': stdout_capture.getvalue(),
                    'runtime': execution_time,
                })
        
        except Exception as e:
            execution_result.update({
                'error': {
                    'type': type(e).__name__,
                    'message': str(e),
                    'traceback': traceback.format_exc()
                },
                'runtime': time.time() - start_time
            })
        
        return execution_result
    
    def analyze_and_suggest_fix(self, code: str, error_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate specific fix suggestions based on error type
        
        :param code: Source code
        :param error_info: Error information dictionary
        :return: List of suggested fixes
        """
        suggestions = []
        error_type = error_info['type']
        
        # Type-specific fix suggestions
        if error_type == 'TypeError':
            suggestions.append({
                'fix': 'Add type conversion or type checking',
                'example': 'Ensure consistent types or use explicit type conversion',
                'code_hint': 'if not isinstance(value, expected_type): value = type_conversion(value)'
            })
        
        elif error_type == 'ValueError':
            suggestions.append({
                'fix': 'Validate input values',
                'example': 'Add input validation before processing',
                'code_hint': 'if not validate_condition(value): raise ValueError("Invalid input")'
            })
        
        elif error_type == 'IndexError':
            suggestions.append({
                'fix': 'Add bounds checking',
                'example': 'Check list length before indexing',
                'code_hint': 'if index < len(my_list): value = my_list[index]'
            })
        
        elif error_type == 'KeyError':
            suggestions.append({
                'fix': 'Use .get() method or check key existence',
                'example': 'my_dict.get(key, default_value)',
                'code_hint': 'value = my_dict.get(key, default_value)'
            })
        
        elif error_type == 'ZeroDivisionError':
            suggestions.append({
                'fix': 'Add zero division check',
                'example': 'if denominator != 0: result = numerator / denominator',
                'code_hint': 'if denominator != 0: result = numerator / denominator else: handle_zero_division()'
            })
        
        # Generic fallback suggestion
        if not suggestions:
            suggestions.append({
                'fix': 'Review and debug code',
                'example': 'Carefully examine the code context and error message',
                'code_hint': '# Requires manual inspection'
            })
        
        return suggestions

    def comprehensive_inspection(self, code: str) -> Dict[str, Any]:
        """
        Perform comprehensive code inspection with advanced error handling
        
        :param code: Source code to inspect
        :return: Comprehensive analysis report
        """
        # Static analysis
        try:
            static_analysis = self.static_analysis(code)
        except Exception as static_error:
            static_analysis = {
                'error': self.error_handler.classify_error(static_error)
            }
        
        # Runtime execution
        try:
            runtime_result = self.runtime_execution(code)
            
            # Check for runtime errors
            if not runtime_result['success'] and 'error' in runtime_result:
                error_info = runtime_result['error']
                error_classification = self.error_handler.classify_error(
                    type(error_info['type'])(error_info['message'])
                )
                
                # Generate fix suggestions
                fix_suggestions = self.analyze_and_suggest_fix(code, error_classification)
                
                runtime_result['error_details'] = {
                    'classification': error_classification,
                    'suggested_fixes': fix_suggestions
                }
        
        except Exception as runtime_error:
            runtime_result = {
                'error': self.error_handler.classify_error(runtime_error)
            }
        
        return {
            'static_analysis': static_analysis,
            'runtime_analysis': runtime_result
        }

def main():
    """
    Demonstrate comprehensive code inspection with various error scenarios
    """
    inspector = CodeInspector(verbose=True)
    
    # Error Scenarios
    error_scenarios = [
        # 1. Type Error
        """
def process_data(value):
    return value + '5'  # Attempting to add string to non-string

process_data(10)
""",
        # 2. Index Error
        """
numbers = [1, 2, 3]
print(numbers[5])  # Accessing out-of-bounds index
""",
        # 3. Zero Division
        """
def divide_numbers(a, b):
    return a / b

print(divide_numbers(10, 0))  # Division by zero
""",
        # 4. Key Error
        """
my_dict = {'a': 1, 'b': 2}
print(my_dict['c'])  # Accessing non-existent key
""",
        # 5. Syntax Error
        """
def broken_function()
    print("This function has a syntax error")
""",
        # 6. Successful Code
        """
def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(factorial(5))
"""
    ]
    
    # Inspect each scenario
    for i, scenario in enumerate(error_scenarios, 1):
        print(f"\n--- Code Scenario {i} ---")
        print("Code:")
        print(scenario)
        print("\nInspection Result:")
        
        # Perform comprehensive inspection
        result = inspector.comprehensive_inspection(scenario)
        
        # Pretty print the result
        import json
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
    
'''
references 
McCabe, T. J. (1976). "A Complexity Measure." IEEE Transactions on Software Engineering, SE-2(4), 308-320.
Halstead, M. H. (1977). "Elements of Software Science." Elsevier North-Holland.
Python Software Foundation. (2024). "Python Language Reference Manual."
Martin, R. C. (2008). "Clean Code: A Handbook of Agile Software Craftsmanship."
'''