//
// Fronts assignment
// Mark Beswetherick 12/10/20

class Node{
    constructor(value){
        this.value = value;
        this.next = null;
    }
} 

class SLL {
    constructor(){
        this.head = null;
    }

    addFront(value) {                   // add a node to the front of the list
        var a_node = new Node(value);
        // if the list is empty, put the new node at the head
        if(this.head == null) {
            this.head = a_node;
            return this;
        }
        // otherwise, put the new node at the head and have it point to the previous head.
        a_node.next = this.head;
        this.head = a_node;
        return this;
    }

    removeFront() {                     // remove a node from the front of the list
        if (this.head != null) {
            this.head = this.head.next;
            return this;
        }
        return null;
    }

    front() {                           // return the VALUE at the front of the list
        if (this.head != null) {
            return this.head.value;
        }
        return null;
    }
    
    contains(value) {
        var runner = this.head;
        while (runner != null) {
            if (runner.value == value)
                return true;
            runner = runner.next;
        }
        // if we get here, we hit end of list without finding value
        return false;
    }

    length() {                      // return length of list. Keep a counter as we run...
        var l_len = 0;
        var runner = this.head;
        while (runner != null) {
            l_len++;
            runner = runner.next;
        }
        return l_len;
    }
}

// test it out
var a_list = new SLL();
a_list.addFront("1st");
a_list.addFront("2nd");
a_list.addFront("3rd");
console.log(`list length: ${a_list.length()}`);

a_list.addFront(1).addFront(333);
console.log(`list length: ${a_list.length()}`);
