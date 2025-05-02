import java.util.Stack;
class main{
    static boolean isStackPermutation(int arr[], int target[]){
        Stack<Integer> st = new Stack();
        int i=0;
        
        for (int ele: arr){
            if (!st.isEmpty() && st.peek()==target[i]){
                st.pop();
                i++;
            }
        }
        
        return st.isEmpty();
    }
    
    public static void main(String args[]){
      int[] original = {1, 2, 3};
        int[] target = {2, 1, 3};
        System.out.println("Is it a stack permutation " + isStackPermutation(original, target));
    }
}