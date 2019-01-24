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
	// example #1
	String repeatedHyphens = new String(new char[20]).replace('\0', '-');
	System.out.println(repeatedHyphens);
	
	// example #2
	repeatedHyphens = String.format("%0" + 20 + "d", 0).replace("0", "-");
	System.out.println(repeatedHyphens);
	
	// example #3 - Java 8 stream api usage
	repeatedHyphens = String.join("", java.util.Collections.nCopies(20, "-"));
	System.out.println(repeatedHyphens);
  }
}
