What does this mystery function do?

    int mystery(int input)
    {
        long long n = (long long)input * (long long)0x55555556;
        long long top = n >> 32;
        int edx = (int)top;
        edx *= 3;
        int answer = input - edx;
        return answer;
    }
     
    int mystery_one_liner(int input)
    {
      return (input-(((int)(((long long)input * (long long)0x55555556)>>32)) * 3));
    }

What it does is simple. How it does it is not. Or at least it's not obvious at
first. I still need to figure out the "magic" behind it. I think this site 
might be a good start: <http://wall.riscom.net/books/proc/ppc/cwg/code2.html>.

Anyway, in my Theoretical Computer Science class we were tasked with writing a 
DFA which determined if a number was evenly divisible by 3. I knew that %2 you 
could simply look at the last bit. But what about %3? I wrote the code for 
"argc % 3" and looked at how gcc with the "-O3" flag compiled it down. It's 
just magic. Multiply by 0x55555556? I'll figure out the "why" later.

For some reason more than two years after taking that class I decided to start 
figuring out the "why" to this particular compiler optimization I first ran 
into back then.

**Note**: What I have written above only works for positive integers.
