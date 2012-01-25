Write C code to reverse a string in place and to convert a base 10 integer to a string of different base (a base that is <= 10).  

    :::c++
    #include <stdio.h>
     
    //reverse a string in place
    void strrev(char* str)
    {
      int len = 0;
      for(len=0; str[len]; len++);
      int i;
      for(i=0; i&lt;len/2; i++) {
        char tmp = str[i];
        str[i] = str[len-i-1];
        str[len-i-1] = tmp;
      }
    }
     
    void my_itoa(int num, char* buf, int base)
    {
      int i = 0;
      while(num != 0)
      {
        int r = num % base;
        num -= r;
        num /= base;
        char c = r + 48; //convert the digit to char
        buf[i] = c;
        i++;
      }
      buf[i] = 0;
      strrev(buf);
    }
     
    int main(int argc, char** argv)
    {
      char a[50] = "hello world this";
      char b[50] = "stuff in the water";
      strrev(a);
      strrev(b);
      printf("%s\n%s\n", a, b);
      char c[100];
      my_itoa(12, c, 5);
      printf("%s\n", c);
     
      return 0;
    }
