/*
 Simple way to print N times this same character
 
 Python construction
       print('-' * 20)
 equivalent

*/
public class PrintNTimes
{
  public static void main(String[] args)
  {
	String repeatedHyphens = new String(new char[20]).replace('\0', '-');
	System.out.println(repeatedHyphens);
  }
}
