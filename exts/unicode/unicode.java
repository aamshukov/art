class UnicodeJava
{
    public static void main(String[] args)
    {
        System.out.println("START of Character.isJavaIdentifierStart");

        int k = 0;
        for(; k < 0x0010FFFF; k++)
        {
            if(Character.isJavaIdentifierStart(k))
            {
                System.out.println(String.format("0x%1$08X", k));
            }
        }

        System.out.println(String.format("%d", k));
        System.out.println("END of Character.isJavaIdentifierStart");
        System.out.println("");

        System.out.println("START of Character.isJavaIdentifierPart");

        for(k = 0; k < 0x0010FFFF; k++)
        {
            if(Character.isJavaIdentifierPart(k))
            {
                System.out.println(String.format("0x%1$08X",k));
            }
        }

        System.out.println(String.format("%d", k));
        System.out.println("END of Character.isJavaIdentifierPart");
        System.out.println("");
    }
}

// cd D:/Projects/art/exts/unicode>
// java unicode.java
