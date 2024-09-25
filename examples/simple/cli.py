import argparse
from textwrap import dedent
from code_generator.generators.cpp2 import Function, Header, Source, Variable

def increment_impl() -> str:
    return 'gCount++;'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--header-output', default='Count.h', help='File path to write the header.')
    parser.add_argument('--source-output', default='Count.cpp', help='File path to write the source.')
    parser.add_argument('-n', '--dryrun', action='store_true')
    args = parser.parse_args()

    # Create a header with a global variable to be used in a source file.
    header = Header(args.header_output).guard('COUNT_H')
    count_var = Variable('gCount', 'unsigned int').val(0)
    header.add(count_var)
    if args.dryrun:
        print(f'------------------- {header.filename}  START -------------------')
        print(str(header))
        print(f'------------------- {header.filename}  END   -------------------')
    else:
        with open(header.filename, 'w+') as f:
            f.write(header.decl_str())

    # Create a source file with a function to increment the global variable defined in the header.
    source = Source(args.source_output).include(header)
    source.add(Function('increment', 'void').impl(increment_impl))
    if args.dryrun:
        print(f'------------------- {source.filename}  START -------------------')
        print(str(source))
        print(f'------------------- {source.filename}  END   -------------------')
    else:
        with open(source.filename, 'w+') as f:
            f.write(source.def_str())

if __name__ == '__main__':
    main()
