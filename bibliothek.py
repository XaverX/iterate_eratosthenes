# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 21:56:41 2019

@author: Berthold
"""

import sys  # specials only

import itertools as IT
#        accumulate
#        chain
#        combinations
#        combinations_with_replacement
#        compress
#        count
#        cycle
#        dropwhile
#        filterfalse
#        groupby
#        islice
#        permutations
#        product
#        repeat
#        starmap
#        takewhile
#        tee
#        zip_longest

import operator as OP
#        abs
#        add
#        and_
#        attrgetter
#        concat
#        contains
#        countOf
#        delitem
#        eq
#        floordiv
#        ge
#        getitem
#        gt
#        iadd
#        iand
#        iconcat
#        ifloordiv
#        ilshift
#        imatmul
#        imod
#        imul
#        index
#        indexOf
#        inv
#        invert
#        ior
#        ipow
#        irshift
#        is_
#        is_not
#        isub
#        itemgetter
#        itruediv
#        ixor
#        le
#        length_hint
#        lshift
#        lt
#        matmul
#        methodcaller
#        mod
#        mul
#        ne
#        neg
#        not_
#        or_
#        pos
#        pow
#        rshift
#        setitem
#        sub
#        truediv
#        truth
#        xor

import functools as FT
#        RLock
#        WRAPPER_ASSIGNMENTS
#        WRAPPER_UPDATES
#        cmp_to_key
#        get_cache_token
#        lru_cache
#        namedtuple
#        partial
#        partialmethod
#        recursive_repr
#        reduce
#        singledispatch
#        total_ordering
#        update_wrapper
#        wraps

import datetime as DT
#        MAXYEAR
#        MINYEAR
#        date
#        datetime
#        datetime_CAPI
#        sys
#        time
#        timedelta
#        timezone
#        tzinfo

import collections as CL
#        ChainMap
#        Counter
#        Iterable
#        Mapping
#        MutableMapping
#        OrderedDict
#        UserDict
#        UserList
#        UserString
#        abc
#        defaultdict
#        deque
#        namedtuple

import json as JS
#        codecs
#        decoder
#        detect_encoding
#        dump
#        dumps
#        encoder
#        load
#        loads
#        scanner


dir(sys)
dir(IT)
dir(OP)
dir(FT)
dir(DT)
dir(CL)
dir(JS)

help('FORMATTING')
Format String Syntax
********************

The "str.format()" method and the "Formatter" class share the same
syntax for format strings (although in the case of "Formatter",
subclasses can define their own format string syntax).  The syntax is
related to that of formatted string literals, but there are
differences.

Format strings contain “replacement fields” surrounded by curly braces
"{}". Anything that is not contained in braces is considered literal
text, which is copied unchanged to the output.  If you need to include
a brace character in the literal text, it can be escaped by doubling:
"{{" and "}}".

The grammar for a replacement field is as follows:

      replacement_field ::= "{" [field_name] ["!" conversion] [":" format_spec] "}"
      field_name        ::= arg_name ("." attribute_name | "[" element_index "]")*
      arg_name          ::= [identifier | digit+]
      attribute_name    ::= identifier
      element_index     ::= digit+ | index_string
      index_string      ::= <any source character except "]"> +
      conversion        ::= "r" | "s" | "a"
      format_spec       ::= <described in the next section>

In less formal terms, the replacement field can start with a
*field_name* that specifies the object whose value is to be formatted
and inserted into the output instead of the replacement field. The
*field_name* is optionally followed by a  *conversion* field, which is
preceded by an exclamation point "'!'", and a *format_spec*, which is
preceded by a colon "':'".  These specify a non-default format for the
replacement value.

See also the Format Specification Mini-Language section.

The *field_name* itself begins with an *arg_name* that is either a
number or a keyword.  If it’s a number, it refers to a positional
argument, and if it’s a keyword, it refers to a named keyword
argument.  If the numerical arg_names in a format string are 0, 1, 2,
… in sequence, they can all be omitted (not just some) and the numbers
0, 1, 2, … will be automatically inserted in that order. Because
*arg_name* is not quote-delimited, it is not possible to specify
arbitrary dictionary keys (e.g., the strings "'10'" or "':-]'") within
a format string. The *arg_name* can be followed by any number of index
or attribute expressions. An expression of the form "'.name'" selects
the named attribute using "getattr()", while an expression of the form
"'[index]'" does an index lookup using "__getitem__()".

Changed in version 3.1: The positional argument specifiers can be
omitted for "str.format()", so "'{} {}'.format(a, b)" is equivalent to
"'{0} {1}'.format(a, b)".

Changed in version 3.4: The positional argument specifiers can be
omitted for "Formatter".

Some simple format string examples:

   "First, thou shalt count to {0}"  # References first positional argument
   "Bring me a {}"                   # Implicitly references the first positional argument
   "From {} to {}"                   # Same as "From {0} to {1}"
   "My quest is {name}"              # References keyword argument 'name'
   "Weight in tons {0.weight}"       # 'weight' attribute of first positional arg
   "Units destroyed: {players[0]}"   # First element of keyword argument 'players'.

The *conversion* field causes a type coercion before formatting.
Normally, the job of formatting a value is done by the "__format__()"
method of the value itself.  However, in some cases it is desirable to
force a type to be formatted as a string, overriding its own
definition of formatting.  By converting the value to a string before
calling "__format__()", the normal formatting logic is bypassed.

Three conversion flags are currently supported: "'!s'" which calls
"str()" on the value, "'!r'" which calls "repr()" and "'!a'" which
calls "ascii()".

Some examples:

   "Harold's a clever {0!s}"        # Calls str() on the argument first
   "Bring out the holy {name!r}"    # Calls repr() on the argument first
   "More {!a}"                      # Calls ascii() on the argument first

The *format_spec* field contains a specification of how the value
should be presented, including such details as field width, alignment,
padding, decimal precision and so on.  Each value type can define its
own “formatting mini-language” or interpretation of the *format_spec*.

Most built-in types support a common formatting mini-language, which
is described in the next section.

A *format_spec* field can also include nested replacement fields
within it. These nested replacement fields may contain a field name,
conversion flag and format specification, but deeper nesting is not
allowed.  The replacement fields within the format_spec are
substituted before the *format_spec* string is interpreted. This
allows the formatting of a value to be dynamically specified.

See the Format examples section for some examples.


Format Specification Mini-Language
==================================

“Format specifications” are used within replacement fields contained
within a format string to define how individual values are presented
(see Format String Syntax and Formatted string literals). They can
also be passed directly to the built-in "format()" function.  Each
formattable type may define how the format specification is to be
interpreted.

Most built-in types implement the following options for format
specifications, although some of the formatting options are only
supported by the numeric types.

A general convention is that an empty format string ("""") """ produces
the same result as if you had called "str()" on the value. A non-empty
format string typically modifies the result.

The general form of a *standard format specifier* is:

   format_spec     ::= [[fill]align][sign][#][0][width][grouping_option][.precision][type]
   fill            ::= <any character>
   align           ::= "<" | ">" | "=" | "^"
   sign            ::= "+" | "-" | " "
   width           ::= digit+
   grouping_option ::= "_" | ","
   precision       ::= digit+
   type            ::= "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"

If a valid *align* value is specified, it can be preceded by a *fill*
character that can be any character and defaults to a space if
omitted. It is not possible to use a literal curly brace (“"{"” or
“"}"”) as the *fill* character in a formatted string literal or when
using the "str.format()" method.  However, it is possible to insert a
curly brace with a nested replacement field.  This limitation doesn’t
affect the "format()" function.

The meaning of the various alignment options is as follows:

   +-----------+------------------------------------------------------------+
   | Option    | Meaning                                                    |
   +===========+============================================================+
   | "'<'"     | Forces the field to be left-aligned within the available   |
   |           | space (this is the default for most objects).              |
   +-----------+------------------------------------------------------------+
   | "'>'"     | Forces the field to be right-aligned within the available  |
   |           | space (this is the default for numbers).                   |
   +-----------+------------------------------------------------------------+
   | "'='"     | Forces the padding to be placed after the sign (if any)    |
   |           | but before the digits.  This is used for printing fields   |
   |           | in the form ‘+000000120’. This alignment option is only    |
   |           | valid for numeric types.  It becomes the default when ‘0’  |
   |           | immediately precedes the field width.                      |
   +-----------+------------------------------------------------------------+
   | "'^'"     | Forces the field to be centered within the available       |
   |           | space.                                                     |
   +-----------+------------------------------------------------------------+

Note that unless a minimum field width is defined, the field width
will always be the same size as the data to fill it, so that the
alignment option has no meaning in this case.

The *sign* option is only valid for number types, and can be one of
the following:

   +-----------+------------------------------------------------------------+
   | Option    | Meaning                                                    |
   +===========+============================================================+
   | "'+'"     | indicates that a sign should be used for both positive as  |
   |           | well as negative numbers.                                  |
   +-----------+------------------------------------------------------------+
   | "'-'"     | indicates that a sign should be used only for negative     |
   |           | numbers (this is the default behavior).                    |
   +-----------+------------------------------------------------------------+
   | space     | indicates that a leading space should be used on positive  |
   |           | numbers, and a minus sign on negative numbers.             |
   +-----------+------------------------------------------------------------+

The "'#'" option causes the “alternate form” to be used for the
conversion.  The alternate form is defined differently for different
types.  This option is only valid for integer, float, complex and
Decimal types. For integers, when binary, octal, or hexadecimal output
is used, this option adds the prefix respective "'0b'", "'0o'", or
"'0x'" to the output value. For floats, complex and Decimal the
alternate form causes the result of the conversion to always contain a
decimal-point character, even if no digits follow it. Normally, a
decimal-point character appears in the result of these conversions
only if a digit follows it. In addition, for "'g'" and "'G'"
conversions, trailing zeros are not removed from the result.

The "','" option signals the use of a comma for a thousands separator.
For a locale aware separator, use the "'n'" integer presentation type
instead.

Changed in version 3.1: Added the "','" option (see also **PEP 378**).

The "'_'" option signals the use of an underscore for a thousands
separator for floating point presentation types and for integer
presentation type "'d'".  For integer presentation types "'b'", "'o'",
"'x'", and "'X'", underscores will be inserted every 4 digits.  For
other presentation types, specifying this option is an error.

Changed in version 3.6: Added the "'_'" option (see also **PEP 515**).

*width* is a decimal integer defining the minimum field width.  If not
specified, then the field width will be determined by the content.

When no explicit alignment is given, preceding the *width* field by a
zero ("'0'") character enables sign-aware zero-padding for numeric
types.  This is equivalent to a *fill* character of "'0'" with an
*alignment* type of "'='".

The *precision* is a decimal number indicating how many digits should
be displayed after the decimal point for a floating point value
formatted with "'f'" and "'F'", or before and after the decimal point
for a floating point value formatted with "'g'" or "'G'".  For non-
number types the field indicates the maximum field size - in other
words, how many characters will be used from the field content. The
*precision* is not allowed for integer values.

Finally, the *type* determines how the data should be presented.

The available string presentation types are:

   +-----------+------------------------------------------------------------+
   | Type      | Meaning                                                    |
   +===========+============================================================+
   | "'s'"     | String format. This is the default type for strings and    |
   |           | may be omitted.                                            |
   +-----------+------------------------------------------------------------+
   | None      | The same as "'s'".                                         |
   +-----------+------------------------------------------------------------+

The available integer presentation types are:

   +-----------+------------------------------------------------------------+
   | Type      | Meaning                                                    |
   +===========+============================================================+
   | "'b'"     | Binary format. Outputs the number in base 2.               |
   +-----------+------------------------------------------------------------+
   | "'c'"     | Character. Converts the integer to the corresponding       |
   |           | unicode character before printing.                         |
   +-----------+------------------------------------------------------------+
   | "'d'"     | Decimal Integer. Outputs the number in base 10.            |
   +-----------+------------------------------------------------------------+
   | "'o'"     | Octal format. Outputs the number in base 8.                |
   +-----------+------------------------------------------------------------+
   | "'x'"     | Hex format. Outputs the number in base 16, using lower-    |
   |           | case letters for the digits above 9.                       |
   +-----------+------------------------------------------------------------+
   | "'X'"     | Hex format. Outputs the number in base 16, using upper-    |
   |           | case letters for the digits above 9.                       |
   +-----------+------------------------------------------------------------+
   | "'n'"     | Number. This is the same as "'d'", except that it uses the |
   |           | current locale setting to insert the appropriate number    |
   |           | separator characters.                                      |
   +-----------+------------------------------------------------------------+
   | None      | The same as "'d'".                                         |
   +-----------+------------------------------------------------------------+

In addition to the above presentation types, integers can be formatted
with the floating point presentation types listed below (except "'n'"
and "None"). When doing so, "float()" is used to convert the integer
to a floating point number before formatting.

The available presentation types for floating point and decimal values
are:

   +-----------+------------------------------------------------------------+
   | Type      | Meaning                                                    |
   +===========+============================================================+
   | "'e'"     | Exponent notation. Prints the number in scientific         |
   |           | notation using the letter ‘e’ to indicate the exponent.    |
   |           | The default precision is "6".                              |
   +-----------+------------------------------------------------------------+
   | "'E'"     | Exponent notation. Same as "'e'" except it uses an upper   |
   |           | case ‘E’ as the separator character.                       |
   +-----------+------------------------------------------------------------+
   | "'f'"     | Fixed-point notation. Displays the number as a fixed-point |
   |           | number. The default precision is "6".                      |
   +-----------+------------------------------------------------------------+
   | "'F'"     | Fixed-point notation. Same as "'f'", but converts "nan" to |
   |           | "NAN" and "inf" to "INF".                                  |
   +-----------+------------------------------------------------------------+
   | "'g'"     | General format.  For a given precision "p >= 1", this      |
   |           | rounds the number to "p" significant digits and then       |
   |           | formats the result in either fixed-point format or in      |
   |           | scientific notation, depending on its magnitude.  The      |
   |           | precise rules are as follows: suppose that the result      |
   |           | formatted with presentation type "'e'" and precision "p-1" |
   |           | would have exponent "exp".  Then if "-4 <= exp < p", the   |
   |           | number is formatted with presentation type "'f'" and       |
   |           | precision "p-1-exp".  Otherwise, the number is formatted   |
   |           | with presentation type "'e'" and precision "p-1". In both  |
   |           | cases insignificant trailing zeros are removed from the    |
   |           | significand, and the decimal point is also removed if      |
   |           | there are no remaining digits following it.  Positive and  |
   |           | negative infinity, positive and negative zero, and nans,   |
   |           | are formatted as "inf", "-inf", "0", "-0" and "nan"        |
   |           | respectively, regardless of the precision.  A precision of |
   |           | "0" is treated as equivalent to a precision of "1". The    |
   |           | default precision is "6".                                  |
   +-----------+------------------------------------------------------------+
   | "'G'"     | General format. Same as "'g'" except switches to "'E'" if  |
   |           | the number gets too large. The representations of infinity |
   |           | and NaN are uppercased, too.                               |
   +-----------+------------------------------------------------------------+
   | "'n'"     | Number. This is the same as "'g'", except that it uses the |
   |           | current locale setting to insert the appropriate number    |
   |           | separator characters.                                      |
   +-----------+------------------------------------------------------------+
   | "'%'"     | Percentage. Multiplies the number by 100 and displays in   |
   |           | fixed ("'f'") format, followed by a percent sign.          |
   +-----------+------------------------------------------------------------+
   | None      | Similar to "'g'", except that fixed-point notation, when   |
   |           | used, has at least one digit past the decimal point. The   |
   |           | default precision is as high as needed to represent the    |
   |           | particular value. The overall effect is to match the       |
   |           | output of "str()" as altered by the other format           |
   |           | modifiers.                                                 |
   +-----------+------------------------------------------------------------+


Format examples
===============

This section contains examples of the "str.format()" syntax and
comparison with the old "%"-formatting.

In most of the cases the syntax is similar to the old "%"-formatting,
with the addition of the "{}" and with ":" used instead of "%". For
example, "'%03.2f'" can be translated to "'{:03.2f}'".

The new format syntax also supports new and different options, shown
in the following examples.

Accessing arguments by position:

   >>> '{0}, {1}, {2}'.format('a', 'b', 'c')
   'a, b, c'
   >>> '{}, {}, {}'.format('a', 'b', 'c')  # 3.1+ only
   'a, b, c'
   >>> '{2}, {1}, {0}'.format('a', 'b', 'c')
   'c, b, a'
   >>> '{2}, {1}, {0}'.format(*'abc')      # unpacking argument sequence
   'c, b, a'
   >>> '{0}{1}{0}'.format('abra', 'cad')   # arguments' indices can be repeated
   'abracadabra'

Accessing arguments by name:

   >>> 'Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
   'Coordinates: 37.24N, -115.81W'
   >>> coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
   >>> 'Coordinates: {latitude}, {longitude}'.format(**coord)
   'Coordinates: 37.24N, -115.81W'

Accessing arguments’ attributes:

   >>> c = 3-5j
   >>> ('The complex number {0} is formed from the real part {0.real} '
   ...  'and the imaginary part {0.imag}.').format(c)
   'The complex number (3-5j) is formed from the real part 3.0 and the imaginary part -5.0.'
   >>> class Point:
   ...     def __init__(self, x, y):
   ...         self.x, self.y = x, y
   ...     def __str__(self):
   ...         return 'Point({self.x}, {self.y})'.format(self=self)
   ...
   >>> str(Point(4, 2))
   'Point(4, 2)'

Accessing arguments’ items:

   >>> coord = (3, 5)
   >>> 'X: {0[0]};  Y: {0[1]}'.format(coord)
   'X: 3;  Y: 5'

Replacing "%s" and "%r":

   >>> "repr() shows quotes: {!r}; str() doesn't: {!s}".format('test1', 'test2')
   "repr() shows quotes: 'test1'; str() doesn't: test2"

Aligning the text and specifying a width:

   >>> '{:<30}'.format('left aligned')
   'left aligned                  '
   >>> '{:>30}'.format('right aligned')
   '                 right aligned'
   >>> '{:^30}'.format('centered')
   '           centered           '
   >>> '{:*^30}'.format('centered')  # use '*' as a fill char
   '***********centered***********'

Replacing "%+f", "%-f", and "% f" and specifying a sign:

   >>> '{:+f}; {:+f}'.format(3.14, -3.14)  # show it always
   '+3.140000; -3.140000'
   >>> '{: f}; {: f}'.format(3.14, -3.14)  # show a space for positive numbers
   ' 3.140000; -3.140000'
   >>> '{:-f}; {:-f}'.format(3.14, -3.14)  # show only the minus -- same as '{:f}; {:f}'
   '3.140000; -3.140000'

Replacing "%x" and "%o" and converting the value to different bases:

   >>> # format also supports binary numbers
   >>> "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}".format(42)
   'int: 42;  hex: 2a;  oct: 52;  bin: 101010'
   >>> # with 0x, 0o, or 0b as prefix:
   >>> "int: {0:d};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}".format(42)
   'int: 42;  hex: 0x2a;  oct: 0o52;  bin: 0b101010'

Using the comma as a thousands separator:

   >>> '{:,}'.format(1234567890)
   '1,234,567,890'

Expressing a percentage:

   >>> points = 19
   >>> total = 22
   >>> 'Correct answers: {:.2%}'.format(points/total)
   'Correct answers: 86.36%'

Using type-specific formatting:

   >>> import datetime
   >>> d = datetime.datetime(2010, 7, 4, 12, 15, 58)
   >>> '{:%Y-%m-%d %H:%M:%S}'.format(d)
   '2010-07-04 12:15:58'

Nesting arguments and more complex examples:

   >>> for align, text in zip('<^>', ['left', 'center', 'right']):
   ...     '{0:{fill}{align}16}'.format(text, fill=align, align=align)
   ...
   'left<<<<<<<<<<<<'
   '^^^^^center^^^^^'
   '>>>>>>>>>>>right'
   >>>
   >>> octets = [192, 168, 0, 1]
   >>> '{:02X}{:02X}{:02X}{:02X}'.format(*octets)
   'C0A80001'
   >>> int(_, 16)
   3232235521
   >>>
   >>> width = 5
   >>> for num in range(5,12): 
   ...     for base in 'dXob':
   ...         print('{0:{width}{base}}'.format(num, base=base, width=width), end=' ')
   ...     print()
   ...
       5     5     5   101
       6     6     6   110
       7     7     7   111
       8     8    10  1000
       9     9    11  1001
      10     A    12  1010
      11     B    13  1011

Related help topics: OPERATORS

Operator precedence
*******************

The following table summarizes the operator precedence in Python, from
lowest precedence (least binding) to highest precedence (most
binding).  Operators in the same box have the same precedence.  Unless
the syntax is explicitly given, operators are binary.  Operators in
the same box group left to right (except for exponentiation, which
groups from right to left).

Note that comparisons, membership tests, and identity tests, all have
the same precedence and have a left-to-right chaining feature as
described in the Comparisons section.

+-------------------------------------------------+---------------------------------------+
| Operator                                        | Description                           |
+=================================================+=======================================+
| "lambda"                                        | Lambda expression                     |
+-------------------------------------------------+---------------------------------------+
| "if" – "else"                                   | Conditional expression                |
+-------------------------------------------------+---------------------------------------+
| "or"                                            | Boolean OR                            |
+-------------------------------------------------+---------------------------------------+
| "and"                                           | Boolean AND                           |
+-------------------------------------------------+---------------------------------------+
| "not" "x"                                       | Boolean NOT                           |
+-------------------------------------------------+---------------------------------------+
| "in", "not in", "is", "is not", "<", "<=", ">", | Comparisons, including membership     |
| ">=", "!=", "=="                                | tests and identity tests              |
+-------------------------------------------------+---------------------------------------+
| "|"                                             | Bitwise OR                            |
+-------------------------------------------------+---------------------------------------+
| "^"                                             | Bitwise XOR                           |
+-------------------------------------------------+---------------------------------------+
| "&"                                             | Bitwise AND                           |
+-------------------------------------------------+---------------------------------------+
| "<<", ">>"                                      | Shifts                                |
+-------------------------------------------------+---------------------------------------+
| "+", "-"                                        | Addition and subtraction              |
+-------------------------------------------------+---------------------------------------+
| "*", "@", "/", "//", "%"                        | Multiplication, matrix                |
|                                                 | multiplication, division, floor       |
|                                                 | division, remainder [5]               |
+-------------------------------------------------+---------------------------------------+
| "+x", "-x", "~x"                                | Positive, negative, bitwise NOT       |
+-------------------------------------------------+---------------------------------------+
| "**"                                            | Exponentiation [6]                    |
+-------------------------------------------------+---------------------------------------+
| "await" "x"                                     | Await expression                      |
+-------------------------------------------------+---------------------------------------+
| "x[index]", "x[index:index]",                   | Subscription, slicing, call,          |
| "x(arguments...)", "x.attribute"                | attribute reference                   |
+-------------------------------------------------+---------------------------------------+
| "(expressions...)", "[expressions...]", "{key:  | Binding or tuple display, list        |
| value...}", "{expressions...}"                  | display, dictionary display, set      |
|                                                 | display                               |
+-------------------------------------------------+---------------------------------------+

-[ Footnotes ]-

[1] While "abs(x%y) < abs(y)" is true mathematically, for floats
    it may not be true numerically due to roundoff.  For example, and
    assuming a platform on which a Python float is an IEEE 754 double-
    precision number, in order that "-1e-100 % 1e100" have the same
    sign as "1e100", the computed result is "-1e-100 + 1e100", which
    is numerically exactly equal to "1e100".  The function
    "math.fmod()" returns a result whose sign matches the sign of the
    first argument instead, and so returns "-1e-100" in this case.
    Which approach is more appropriate depends on the application.

[2] If x is very close to an exact integer multiple of y, it’s
    possible for "x//y" to be one larger than "(x-x%y)//y" due to
    rounding.  In such cases, Python returns the latter result, in
    order to preserve that "divmod(x,y)[0] * y + x % y" be very close
    to "x".

[3] The Unicode standard distinguishes between *code points* (e.g.
    U+0041) and *abstract characters* (e.g. “LATIN CAPITAL LETTER A”).
    While most abstract characters in Unicode are only represented
    using one code point, there is a number of abstract characters
    that can in addition be represented using a sequence of more than
    one code point.  For example, the abstract character “LATIN
    CAPITAL LETTER C WITH CEDILLA” can be represented as a single
    *precomposed character* at code position U+00C7, or as a sequence
    of a *base character* at code position U+0043 (LATIN CAPITAL
    LETTER C), followed by a *combining character* at code position
    U+0327 (COMBINING CEDILLA).

    The comparison operators on strings compare at the level of
    Unicode code points. This may be counter-intuitive to humans.  For
    example, ""\u00C7" == "\u0043\u0327"" is "False", even though both
    strings represent the same abstract character “LATIN CAPITAL
    LETTER C WITH CEDILLA”.

    To compare strings at the level of abstract characters (that is,
    in a way intuitive to humans), use "unicodedata.normalize()".

[4] Due to automatic garbage-collection, free lists, and the
    dynamic nature of descriptors, you may notice seemingly unusual
    behaviour in certain uses of the "is" operator, like those
    involving comparisons between instance methods, or constants.
    Check their documentation for more info.

[5] The "%" operator is also used for string formatting; the same
    precedence applies.

[6] The power operator "**" binds less tightly than an arithmetic
    or bitwise unary operator on its right, that is, "2**-1" is "0.5".

Related help topics: lambda, or, and, not, in, is, BOOLEAN, COMPARISON,
BITWISE, SHIFTING, BINARY, FORMATTING, POWER, UNARY, ATTRIBUTES,
SUBSCRIPTS, SLICINGS, CALLS, TUPLES, LISTS, DICTIONARIES


