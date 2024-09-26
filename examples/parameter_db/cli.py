import argparse
from code_generator.generators.cpp2 import Variable

def main():
    header = []
    count_var = Variable('count', 'unsigned int').val(0)
    header.append('#include <iostream>')
    header.append(count_var.def_str())
    # print(count_var.decl_str())
    print('\n'.join(header))

if __name__ == '__main__':
    main()
