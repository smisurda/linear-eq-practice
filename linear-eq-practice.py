'''
	@author Samantha L. Misurda
	linear-eq-practice.py
'''

import streamlit as st
import numpy as np

# Help step descriptions
step_description = [ "Add {opp_b} to both sides" ,
					 "Combine terms",
					 "Divide both sides by {a}",
					 "Reduce",
					 "Done ✅"
					]

# LaTeX formatted steps for help
step_equation = [ "{a} x {sign} {b} = {c}",
				  "{a} x {sign} {b} {op_sign} {b} = {c} {op_sign} {b}",
				  "{a} x = {const}",
				  "\\frac{{{a}}}{{{a}}} x = \\frac{{{const}}}{{{a}}}",
				  "x = {result:g}"
				]

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
	if "step" not in st.session_state:
		st.session_state.step = 0

def show_steps():
	st.session_state.step=1

def clear_text():
    st.session_state.number = st.session_state.widget
    st.session_state.widget = ""

def new_equation():
	st.session_state.number = ""
	number = ""
	del st.session_state.a 
	del st.session_state.b
	del st.session_state.c
	del st.session_state.step
	del st.session_state.incorrect_count
	
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
		op_sign = "+"
	else:
		sign = '+'
		op_sign = "-"
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
					st.write(f"<span style=\"color:green\"> 🥳 That's correct, great job! 🎉 \n {operation.capitalize()}ing {b} {'to' if operation == 'add' else 'from'} each side and dividing both sides by {st.session_state.a} gives x = {number}</span>",unsafe_allow_html=True)
				else:
					st.write(f"<span style=\"color:red\">⚠️ Sorry, {number} is not quite right. \n ",unsafe_allow_html=True)
					
					# Increment incorrect answer count
					st.session_state.incorrect_count += 1

					# Display a hint button if the user is continuing to struggle
					if(st.session_state.incorrect_count >= 2):
						st.write("Wrong :",st.session_state.incorrect_count)
						st.button('🛟 I need some help!', on_click=show_steps)

			except ValueError:
				st.write("Invalid number. Please enter a positive or negative whole number.")


	st.button("Try another!", on_click=new_equation)

	# If the user requests it after two or more wrong answers
	# Show step by step solving instructions
	if st.session_state.step >= 1:
		st.header("Step " + str(st.session_state.step))

		# The step_equation list has placeholders for all of these values
		st.latex(step_equation[st.session_state.step-1].format(a=st.session_state.a, 
																	b=b,sign=sign, 
																	c=st.session_state.c, 
																	op_sign=op_sign,
																	opp_b=-st.session_state.b,
																	const = (st.session_state.c-st.session_state.b),
																	result=int((st.session_state.c-st.session_state.b)/st.session_state.a)))
		st.write(step_description[st.session_state.step-1].format(a=st.session_state.a, 
																	b=b,sign=sign, 
																	c=st.session_state.c,
																	opp_b=-st.session_state.b,
																	op_sign=op_sign,
																	const = (st.session_state.c-st.session_state.b),
																	result=int((st.session_state.c-st.session_state.b)/st.session_state.a)))
		# As long as there are more steps, show the next button
		if st.session_state.step < len(step_description):
			if st.button("Next>"):
				st.session_state.step += 1

driver();
