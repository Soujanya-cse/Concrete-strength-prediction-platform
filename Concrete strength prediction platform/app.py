from flask import Flask, request, render_template
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Load the model and transformers
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
power_transformer = pickle.load(open('power_transformer.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', name=request.args.get('name'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Capture form data
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            # Simulated message handling
            print(f"Message received from {name} ({email}): {message}")

            # Render success message
            return render_template('contact.html', success="Your message has been sent successfully!")

        except Exception as e:
            # Handle errors
            error_message = f"An error occurred: {str(e)}"
            return render_template('contact.html', error=error_message)

    return render_template('contact.html')

# Route for Building with Renewable Resources
@app.route('/building_renewable')
def building_renewable():
    return render_template('building_renewable.html')

# Route for Strengthening Construction
@app.route('/strengthening_construction')
def strengthening_construction():
    return render_template('strengthening_construction.html')

# Route for Custom Inputs
@app.route('/custom_inputs')
def custom_inputs():
    return render_template('custom_inputs.html')



@app.route('/get-started', methods=['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        try:
            # Collect inputs from the form
            inputs = [float(request.form[field]) for field in 
                      ['cement', 'blastFurnace', 'flyAsh', 'water', 
                       'superplasticizer', 'courseAggregate', 'fineaggregate', 'age']]

            # Transform and scale input
            transformed_inputs = power_transformer.transform([inputs])
            scaled_inputs = scaler.transform(transformed_inputs)

            # Predict strength
            prediction = model.predict(scaled_inputs)[0]  # Predicted compressive strength in MPa

            # Categorize and provide advice
            if prediction >= 40:
                strength_category = "Good"
                advice = "The concrete strength is sufficient for high-load structural applications."
            elif 20 <= prediction < 40:
                strength_category = "Average"
                advice = ("The concrete strength is moderate. Consider improving the mix design by optimizing the "
                          "cement content, reducing the water-cement ratio, or adding suitable admixtures like superplasticizers.")
            else:
                strength_category = "Bad"
                advice = ("The concrete strength is low. Check for errors in mix proportions or quality of materials. "
                          "Consider revising the design mix and ensuring proper curing conditions.")

            # Pass results to the template
            return render_template('get-started.html', 
                                   predicted_strength=f"{prediction:.2f} MPa", 
                                   strength_category=strength_category, 
                                   advice=advice)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('get-started.html', error=error_message)

    return render_template('get-started.html')

if __name__ == '__main__':
    app.run(debug=True)
