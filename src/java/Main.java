import java.awt.*;
import javax.swing.JTextArea;
import javax.swing.JPanel;
import javax.swing.JFrame;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.JScrollPane;

public class Main
{
    public static void main(String[] args) {
        GridLayout lay = new GridLayout(1,2,5,5);
        
        JTextArea right = new JTextArea();
        right.setEditable(false);
        right.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 14));
        JScrollPane rightScroller = new JScrollPane(right);
        
        JTextArea left = new JTextArea();
        left.setEditable(true);
        left.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 14));
        left.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent de) {
                right.setText(format(left.getText()));
            }

            @Override
            public void removeUpdate(DocumentEvent de) {
                right.setText(format(left.getText()));
            }

            @Override
            public void changedUpdate(DocumentEvent de) {
                //Plain text components don't fire these events.
            }
        });
        JScrollPane leftScroller = new JScrollPane(left);
        JFrame frame = new JFrame("Escape Remover 2000");
        frame.setLayout(lay);
        frame.add(leftScroller);
        frame.add(rightScroller);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setPreferredSize(new Dimension(1280,600));
        frame.pack();
        frame.setVisible(true);
    }
    
    private static String format(String in) {
        int location = in.indexOf("&");
        while(location < in.length()) {
            location = in.indexOf("&");
            if(location != -1 && (location + 2) < in.length()) {
                location++;
                in = in.substring(0,location - 1) + in.substring(location+2);
            } else {
                location = in.length();
            }
        }
        return in;
    }
}
