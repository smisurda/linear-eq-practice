'''
	@author Samantha L. Misurda
	linear-eq-practice.py
'''

import streamlit as st
import numpy as np

# Generates a random linear equation from numbers in the range [-10,10]
def generate_equation():
	# Generate ax + b = c
	if "a" not in st.session_state:
		# a can be any integer in this range
	    st.session_state.a = np.random.randint(low=-10, high=10);
	    # but not 0.
	    while st.session_state.a == 0:
	    	st.session_state.a = np.random.randint(low=-10, high=10);
	    
	    # (c-b) should be a multiple of a
	    st.session_state.b = np.random.randint(low=-10, high=10);
	    st.session_state.c = np.random.randint(low=-10, high=10);
	    while (st.session_state.c-st.session_state.b) % st.session_state.a != 0:
	    	st.session_state.b = np.random.randint(low=-10, high=10);
	    	st.session_state.c = np.random.randint(low=-10, high=10);

def clear_text():
    st.session_state.number = st.session_state.widget
    st.session_state.widget = ""

def new_equation():
	st.session_state.number = ""
	number = ""
	del st.session_state.a 
	del st.session_state.b
	del st.session_state.c
	
	generate_equation()

def driver():
	# Setup the equation
	generate_equation()

	# Initialize the counter variable in session state if it doesn't exist
	if 'incorrect_count' not in st.session_state:
	    st.session_state.incorrect_count = 0

	# Determine how to format the equation in the form Ax +B = C 
	# When B is < 0, we want to print Ax - B = C, not Ax + - B = C
	if st.session_state.b < 0:
		sign = '-'
	else:
		sign = '+'
	b = abs(st.session_state.b)
	equation_string = f"{st.session_state.a} x {sign} {b} = {st.session_state.c}"
	st.title("Solve this linear equation:")
	st.latex(equation_string)
	left, right = st.columns([.04,.96],vertical_alignment="bottom")
	with left:
		st.write("X = ")
	with right:	
		st.text_input("",key='widget', on_change=clear_text)
		number = st.session_state.get('number', '')

	# Check if the user has input a response, and that the response is a valid 
	# character (number), and if the response is correct
	with st.empty():
		if len(number) > 0:
			# To determine how to print the help message based on operation
			operation = "add" if sign == '-' else "subtract"
			try: 
				if (int(number) * st.session_state.a + st.session_state.b) == st.session_state.c:
					st.write(f"<span style=\"color:green\"> 🥳 That's correct, great job! 🎉 \n {operation.capitalize()}ing {st.session_state.b} {'to' if operation == 'add' else 'from'} each side and dividing both sides by {st.session_state.a} gives x = {number}</span>",unsafe_allow_html=True)
				else:
					st.write(f"<span style=\"color:red\">⚠️ Sorry, {number} is not quite right. \n ",unsafe_allow_html=True)
					
					# Increment incorrect answer count
					st.session_state.incorrect_count += 1

					# Display a hint button if the user is continuing to struggle
					if(st.session_state.incorrect_count >= 2):
						st.write("Wrong :",st.session_state.incorrect_count)
						if st.button('🛟 I need some help!'):
							st.write(f"You should {operation} {st.session_state.b} {'to' if operation == 'add' else 'from'} both sides, and then divide {st.session_state.a} from both sides.")
			except ValueError:
				st.write("Invalid number. Please enter a positive or negative whole number.")


	st.button("Try another!", on_click=new_equation)

driver();
