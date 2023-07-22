package budgetanalysis;
import javax.swing.JOptionPane;


public class budgetAnalysis {

    
    public static void main(String[] args) {
        String userInput;
        double inputBudget;
        double houseExpense;
        double TravelExpense;
        double MessExpenses;
        double extraExpense;
        double totalExpense = 0;   
        int moreExpenses = 0;  
        
        userInput = JOptionPane.showInputDialog("What is your monthly budget?");
        inputBudget = Double.parseDouble(userInput);
        
        userInput = JOptionPane.showInputDialog("Enter housing expenses: ");
        houseExpense = Double.parseDouble(userInput);
        
        userInput = JOptionPane.showInputDialog("Enter Travel expenses: ");
        TravelExpense = Double.parseDouble(userInput);
        
        userInput = JOptionPane.showInputDialog("Enter Mess expenses: ");
        MessExpenses = Double.parseDouble(userInput);
        
        totalExpense = (totalExpense + houseExpense + TravelExpense + MessExpenses);
        
        while(moreExpenses == JOptionPane.YES_OPTION) {
            userInput = JOptionPane.showInputDialog("Enter an extra expense: ");
            extraExpense = Double.parseDouble(userInput);
            totalExpense = (totalExpense + extraExpense); 
            moreExpenses = JOptionPane.showConfirmDialog(null,"Do you have additional expenses?", "Budet Analysis App", JOptionPane.YES_NO_OPTION);
        }
        
        if(totalExpense < inputBudget){
            JOptionPane.showMessageDialog(null, "You are under budget by $" + (inputBudget - totalExpense) + "\nTotal monthly expenses = $" + totalExpense);
        }
        else if(totalExpense > inputBudget){
            JOptionPane.showMessageDialog(null, "You are over budget by $" + (totalExpense - inputBudget) + "\nTotal monthly expenses = $" + totalExpense);
        }
        else{
            JOptionPane.showMessageDialog(null, "You are on budget. Total expenses = $" + totalExpense );
        }
        
        System.exit(0);
    }}