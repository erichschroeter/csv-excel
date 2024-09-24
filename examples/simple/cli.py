import argparse
from code_generator.generators.cpp2 import Header, Variable

def main():
    header = Header('Count.h')
    count_var = Variable('count', 'unsigned int').val(0)
    header.include('iostream')
    header.append(count_var)
    print(header)

if __name__ == '__main__':
    main()
